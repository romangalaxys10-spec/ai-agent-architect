"""
Human-in-the-Loop subsystem.

Canonical mechanics (LangGraph/OpenAI-SDK doctrine):
- interrupt() pauses the run at a step boundary; a checkpoint captures full state.
- Human decisions: APPROVE (execute as proposed) / EDIT (modify arguments) /
  REJECT (skip + refusal feedback so the agent learns) / RESPOND (human answers
  directly as a synthetic tool result).
- Approval scopes: per-tool, conditional predicates, subagent inheritance.
- Approvals are an audit trail (who/what/when/decision).
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class Decision(str, Enum):
    APPROVE = "approve"
    EDIT = "edit"
    REJECT = "reject"
    RESPOND = "respond"


@dataclass
class Interrupt:
    """A paused run awaiting human input."""
    interrupt_id: str
    tool_name: str
    arguments: Dict[str, Any]
    reason: str = "approval required"
    created_at: float = field(default_factory=time.time)
    resolved: bool = False
    decision: Optional[Decision] = None
    edited_arguments: Optional[Dict[str, Any]] = None
    human_response: Optional[str] = None

    def resolve(
        self,
        decision: Decision,
        edited_arguments: Optional[Dict[str, Any]] = None,
        human_response: Optional[str] = None,
    ) -> "Interrupt":
        self.decision = decision
        self.edited_arguments = edited_arguments
        self.human_response = human_response
        self.resolved = True
        return self


@dataclass
class ApprovalRule:
    """allow / ask / deny ruleset (bryanyzhu Ch.12) with optional predicate."""
    tool_name: str
    mode: str  # "allow" | "ask" | "deny"
    when: Optional[Callable[[Dict[str, Any]], bool]] = None  # conditional (e.g. writes outside workspace)
    description: str = ""


class ApprovalPolicy:
    """
    Ruleset engine: most specific rule wins; default mode configurable.
    Subagent approval inheritance: same policy object can be shared with
    children (they inherit the parent's ask/deny gates).
    """

    def __init__(self, default_mode: str = "ask", share_with_subagents: bool = True):
        self.default_mode = default_mode
        self.share_with_subagents = share_with_subagents
        self._rules: Dict[str, List[ApprovalRule]] = {}

    def add_rule(self, rule: ApprovalRule) -> None:
        self._rules.setdefault(rule.tool_name, []).append(rule)

    def mode_for(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        for rule in reversed(self._rules.get(tool_name, [])):  # later rules are more specific
            if rule.when is None or rule.when(arguments):
                return rule.mode
        return self.default_mode


@dataclass
class Checkpoint:
    """Full serializable run state at a step boundary (the resume button)."""
    checkpoint_id: str
    run_id: str
    step_index: int
    state: Dict[str, Any]  # messages, notes, budgets snapshot...
    created_at: float = field(default_factory=time.time)
    interrupt: Optional[Interrupt] = None


class CheckpointStore:
    """In-memory checkpointer with JSON export (swap for Postgres in prod)."""

    def __init__(self) -> None:
        self._checkpoints: Dict[str, Checkpoint] = {}

    def save(self, checkpoint: Checkpoint) -> None:
        self._checkpoints[checkpoint.checkpoint_id] = checkpoint

    def load(self, checkpoint_id: str) -> Optional[Checkpoint]:
        return self._checkpoints.get(checkpoint_id)

    def latest(self, run_id: str) -> Optional[Checkpoint]:
        candidates = [c for c in self._checkpoints.values() if c.run_id == run_id]
        return max(candidates, key=lambda c: c.created_at) if candidates else None

    def to_json(self) -> str:
        return json.dumps(
            {cid: {"run_id": c.run_id, "step": c.step_index, "created_at": c.created_at} for cid, c in self._checkpoints.items()},
            indent=2,
        )


class HumanApprovalFlow:
    """
    Ties interrupts + policy + checkpoints together. Two modes:
    - callback mode: a registered resolver decides immediately (GUI/tests).
    - manual mode: interrupt() returns the Interrupt; outer code resolves it and
      calls resume(); state is checkpointed meanwhile.
    """

    def __init__(self, policy: Optional[ApprovalPolicy] = None, store: Optional[CheckpointStore] = None):
        self.policy = policy or ApprovalPolicy()
        self.store = store or CheckpointStore()
        self.resolver: Optional[Callable[[Interrupt], Decision]] = None
        self.audit_trail: List[Dict[str, Any]] = []

    def set_resolver(self, resolver: Callable[[Interrupt], Decision]) -> None:
        self.resolver = resolver

    def check(self, tool_name: str, arguments: Dict[str, Any]) -> Optional[Interrupt]:
        """Returns an unresolved Interrupt if mode == 'ask'; None if allowed; raises if denied."""
        mode = self.policy.mode_for(tool_name, arguments)
        if mode == "allow":
            return None
        if mode == "deny":
            raise PermissionError(f"Tool '{tool_name}' is denied by approval policy.")
        return Interrupt(
            interrupt_id=f"intr_{uuid.uuid4().hex[:10]}",
            tool_name=tool_name,
            arguments=arguments,
        )

    def resolve(self, interrupt: Interrupt, decision: Decision,
                edited_arguments: Optional[Dict[str, Any]] = None,
                human_response: Optional[str] = None) -> Interrupt:
        interrupt.resolve(decision, edited_arguments, human_response)
        self.audit_trail.append(
            {
                "interrupt_id": interrupt.interrupt_id,
                "tool": interrupt.tool_name,
                "decision": decision.value,
                "ts": time.time(),
                "edited": edited_arguments is not None,
            }
        )
        return interrupt

    def auto_resolve(self, interrupt: Interrupt) -> Interrupt:
        """Callback mode: delegate to the registered resolver."""
        if not self.resolver:
            # Safe default: reject when no resolver is wired (fail-closed).
            return self.resolve(interrupt, Decision.REJECT, human_response="No approval resolver configured; defaulting to rejection.")
        decision = self.resolver(interrupt)
        return self.resolve(interrupt, decision)

    def checkpoint(self, run_id: str, step_index: int, state: Dict[str, Any],
                   interrupt: Optional[Interrupt] = None) -> Checkpoint:
        cp = Checkpoint(
            checkpoint_id=f"cp_{uuid.uuid4().hex[:10]}",
            run_id=run_id,
            step_index=step_index,
            state=state,
            interrupt=interrupt,
        )
        self.store.save(cp)
        return cp
