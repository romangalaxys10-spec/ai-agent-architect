"""
The Real Agent Loop (v2.0).

This is the heart the framework was missing: an actual LLM-in-the-loop
executor implementing the 2024-2025 consensus architecture:

    perceive -> [guardrail] -> LLM call -> tool calls (parallel capable)
      -> HITL gates -> results as messages -> loop detection -> budget check
      -> stop when: model says stop | success predicate | budget | guard

Features:
- ReAct-style cycle with real provider calls (or offline Echo/Scripted).
- Errors are messages: tool failures flow back to the model with hints.
- Parallel tool execution in a single turn (asyncio-free thread fan-out).
- HITL interrupts for approval-gated tools, with checkpoint+resume.
- Loop detector injections (inform/constrain/escalate).
- Three-currency budget portfolio with advertised fragment in the prompt.
- Context engine: compaction + structured note recitation each step.
- Tracer spans for every LLM/tool call with correlation IDs.
- Deterministic offline mode by default (EchoProvider) — zero keys needed.
"""

from __future__ import annotations

import json
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Sequence

from .context_engineering import ContextEngine
from .hitl import Decision, HumanApprovalFlow, Interrupt
from .llm.providers import EchoProvider, LLMProvider, LLMResponse, Message, Role
from .observability import TelemetryTracer
from .reliability import BudgetExceededError, BudgetPortfolio, LoopDetector, TerminationCriteria
from .tool_registry import ToolExecutionResult, ToolRegistry


class StopReason(str, Enum):
    MODEL_STOP = "model_stop"                # model produced a final answer
    SUCCESS_PREDICATE = "success_predicate"  # externally checkable goal met
    BUDGET_EXHAUSTED = "budget_exhausted"
    LOOP_DETECTED = "loop_detected"
    GUARD_TRIPPED = "guard_tripped"
    MAX_STEPS = "max_steps"


@dataclass
class TurnRecord:
    step: int
    assistant_text: Optional[str]
    tool_calls: List[Dict[str, Any]]
    tool_results: List[Dict[str, Any]]
    finish_reason: str
    tokens: int
    cost_usd: float
    latency_ms: float


@dataclass
class AgentRunResult:
    run_id: str
    final_answer: Optional[str]
    stop_reason: StopReason
    steps: int
    turns: List[TurnRecord]
    total_tokens: int
    total_cost_usd: float
    wallclock_ms: float
    transcript: List[Message]
    artifacts: Dict[str, Any] = field(default_factory=dict)

    @property
    def success(self) -> bool:
        return self.stop_reason in (StopReason.MODEL_STOP, StopReason.SUCCESS_PREDICATE)


class AgentLoop:
    """Production agent executor. Composable: bring your own provider/registry/policy."""

    def __init__(
        self,
        name: str = "agent",
        system_prompt: str = "You are a precise autonomous agent. Verify outputs before responding.",
        provider: Optional[LLMProvider] = None,
        model: str = "echo-local",
        registry: Optional[ToolRegistry] = None,
        context_engine: Optional[ContextEngine] = None,
        budgets: Optional[BudgetPortfolio] = None,
        loop_detector: Optional[LoopDetector] = None,
        approval_flow: Optional[HumanApprovalFlow] = None,
        termination: Optional[TerminationCriteria] = None,
        tracer: Optional[TelemetryTracer] = None,
        max_parallel_tool_calls: int = 4,
        max_steps: int = 25,
        on_step: Optional[Callable[[TurnRecord], None]] = None,
    ):
        self.name = name
        self.system_prompt = system_prompt
        self.provider = provider or EchoProvider()
        self.model = model
        self.registry = registry or ToolRegistry()
        self.context_engine = context_engine or ContextEngine()
        self.budgets = budgets or BudgetPortfolio(max_steps=max_steps)
        self.loop_detector = loop_detector or LoopDetector()
        self.approval_flow = approval_flow
        self.termination = termination or TerminationCriteria()
        self.tracer = tracer or TelemetryTracer(f"loop:{name}")
        self.max_parallel_tool_calls = max_parallel_tool_calls
        self.on_step = on_step

    # ------------------------------------------------------------------

    def run(self, task: str, history: Optional[List[Message]] = None) -> AgentRunResult:
        run_id = f"run_{uuid.uuid4().hex[:12]}"
        started = time.time()
        conversation: List[Message] = list(history or []) + [Message.user(task)]
        turns: List[TurnRecord] = []
        total_tokens = 0
        total_cost = 0.0
        final_answer: Optional[str] = None
        stop_reason = StopReason.MAX_STEPS
        artifacts: Dict[str, Any] = {}

        # Advertise the budget so the model paces itself (advertised < enforced).
        system = f"{self.system_prompt}\n\n{self.budgets.advertised_prompt_fragment()}"

        try:
            for step in range(int(self.budgets._budgets["steps"].enforced)):
                self.budgets.tick_step()
                self.budgets.check()

                # --- Context assembly: notes recitation + compaction -------------
                tools_digest = "\n".join(
                    f"- {d['name']}: {d['description']}" for d in self.registry.export_mcp_declarations()
                )
                window = self.context_engine.step(system, conversation, tools_digest)

                # --- LLM call -----------------------------------------------------
                span = self.tracer.start_span("llm.call", attributes={"step": step, "model": self.model})
                t0 = time.time()
                response: LLMResponse = self.provider.complete(
                    window, model=self.model,
                    tools=self.registry.export_mcp_declarations() if self.registry.list_tools() else None,
                )
                llm_ms = (time.time() - t0) * 1000
                self.tracer.end_span(span, extra_attributes={
                    "finish_reason": response.finish_reason, "tokens": response.usage.total_tokens,
                })

                self.budgets.tick_tokens(response.usage.total_tokens)
                total_tokens += response.usage.total_tokens
                total_cost += response.usage.cost_usd

                conversation.append(
                    Message(role=Role.ASSISTANT, content=response.content, tool_calls=response.tool_calls or None)
                )

                turn = TurnRecord(
                    step=step, assistant_text=response.content,
                    tool_calls=list(response.tool_calls or []),
                    tool_results=[], finish_reason=response.finish_reason,
                    tokens=response.usage.total_tokens, cost_usd=response.usage.cost_usd,
                    latency_ms=llm_ms,
                )

                # --- No tool calls: model is done ----------------------------------
                if not response.tool_calls:
                    turns.append(turn)
                    if self.on_step:
                        self.on_step(turn)
                    final_answer = response.content
                    stop_reason = StopReason.MODEL_STOP
                    break

                # --- Execute tool calls (parallel fan-out) --------------------------
                results = self._execute_tool_calls(response.tool_calls, conversation, run_id, step)
                turn.tool_results = [
                    {"tool": r["tool"], "success": r["result"].success, "cached": r["result"].cached}
                    for r in results
                ]
                turns.append(turn)
                if self.on_step:
                    self.on_step(turn)

                # --- Loop detection + graduated response ----------------------------
                escalation = self.loop_detector.verdict()
                if escalation:
                    level = escalation["level"]
                    if level == "escalate":
                        stop_reason = StopReason.LOOP_DETECTED
                        final_answer = final_answer or (
                            f"Run terminated: {escalation['reason']}"
                        )
                        break
                    # inform / constrain: inject guidance as a system nudge
                    conversation.append(
                        Message(role=Role.SYSTEM, content=f"[LOOP-GUARD:{level}] {escalation['reason']}")
                    )

                # --- Externally checkable success predicate -------------------------
                ended = self.termination.evaluate()
                if ended == "success":
                    stop_reason = StopReason.SUCCESS_PREDICATE
                    final_answer = final_answer or response.content
                    break

        except BudgetExceededError as exc:
            stop_reason = StopReason.BUDGET_EXHAUSTED
            final_answer = final_answer or f"Run stopped: {exc}"
        except PermissionError as exc:
            stop_reason = StopReason.GUARD_TRIPPED
            final_answer = final_answer or f"Run stopped by policy: {exc}"
        else:
            # For-range exhausted without the model stopping: if we spent the
            # advertised step budget, that is budget exhaustion, not a clean end.
            if stop_reason == StopReason.MAX_STEPS and any(
                b.near_limit for b in self.budgets._budgets.values()
            ):
                stop_reason = StopReason.BUDGET_EXHAUSTED
                final_answer = final_answer or "Run stopped: step budget exhausted before the model finished."

        artifacts["budgets"] = self.budgets.summary()
        artifacts["loop_detector"] = {
            "recent_fingerprints": len(self.loop_detector._recent),
            "progress_updates": self.loop_detector._progress_updates,
        }
        artifacts["tool_health"] = self.registry.health_summary()

        return AgentRunResult(
            run_id=run_id,
            final_answer=final_answer,
            stop_reason=stop_reason,
            steps=len(turns),
            turns=turns,
            total_tokens=total_tokens,
            total_cost_usd=round(total_cost, 6),
            wallclock_ms=(time.time() - started) * 1000,
            transcript=conversation,
            artifacts=artifacts,
        )

    # ------------------------------------------------------------------

    def _execute_tool_calls(
        self, tool_calls: Sequence[Dict[str, Any]], conversation: List[Message],
        run_id: str, step: int,
    ) -> List[Dict[str, Any]]:
        """Execute the turn's tool calls; append tool messages; return records."""
        outcomes: List[Dict[str, Any]] = []

        def _one(call: Dict[str, Any]) -> Dict[str, Any]:
            name = call.get("name", "")
            try:
                arguments = json.loads(call.get("arguments") or "{}")
                if not isinstance(arguments, dict):
                    arguments = {"value": arguments}
            except json.JSONDecodeError:
                arguments = {}
                result = ToolExecutionResult(
                    tool_name=name, success=False, output=None,
                    error="model produced unparseable tool arguments",
                )
                return {"tool": name, "result": result, "call_id": call.get("id")}

            # HITL gate -------------------------------------------------------
            if self.approval_flow and self.registry.requires_approval(name):
                interrupt = self.approval_flow.check(name, arguments)
                if interrupt is not None:
                    self.approval_flow.checkpoint(
                        run_id, step, {"pending_tool": name, "arguments": arguments}, interrupt=interrupt
                    )
                    resolved = self.approval_flow.auto_resolve(interrupt)
                    if resolved.decision == Decision.REJECT:
                        return {
                            "tool": name, "call_id": call.get("id"),
                            "result": ToolExecutionResult(
                                tool_name=name, success=False, output=None,
                                error=f"human rejected execution: {resolved.human_response or 'no reason given'}",
                            ),
                        }
                    if resolved.decision == Decision.EDIT and resolved.edited_arguments is not None:
                        arguments = resolved.edited_arguments
                    if resolved.decision == Decision.RESPOND:
                        return {
                            "tool": name, "call_id": call.get("id"),
                            "result": ToolExecutionResult(
                                tool_name=name, success=True,
                                output=resolved.human_response or "(no human response)",
                            ),
                        }
                    # APPROVE falls through to execution

            # Loop detector observes the canonical fingerprint ------------------
            self.loop_detector.observe(name, arguments)

            span = self.tracer.start_span("tool.call", attributes={"tool": name, "step": step})
            result = self.registry.execute(name, **arguments)
            self.tracer.end_span(span, extra_attributes={"success": result.success, "ms": result.execution_time_ms})
            return {"tool": name, "call_id": call.get("id"), "result": result}

        calls = list(tool_calls)
        if len(calls) > 1:
            with ThreadPoolExecutor(max_workers=self.max_parallel_tool_calls) as pool:
                outcomes = list(pool.map(_one, calls))
        else:
            outcomes = [_one(c) for c in calls]

        for out in outcomes:
            conversation.append(
                Message(
                    role=Role.TOOL,
                    content=out["result"].to_tool_message_text(),
                    tool_call_id=out.get("call_id"),
                    name=out["tool"],
                )
            )
        return outcomes
