"""
Planning & Reasoning Patterns.

Implements the four plan shapes (bryanyzhu Ch.09):
- NO_PLAN      : straight execution
- CHECKLIST    : static todo list
- PLAN_EXECUTE_REPLAN : dynamic plan revised after observations
- DEPENDENCY_GRAPH    : DAG with parallelizable branches

Plus the ReAct scaffold and a PlannerWorkerCritic escalation ladder
(GeneArnold M4): worker retry -> planner re-plan -> human.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Sequence


class PlanShape(str, Enum):
    NO_PLAN = "no_plan"
    CHECKLIST = "checklist"
    PLAN_EXECUTE_REPLAN = "plan_execute_replan"
    DEPENDENCY_GRAPH = "dependency_graph"


@dataclass
class PlanStep:
    step_id: str
    description: str
    depends_on: List[str] = field(default_factory=list)
    status: str = "PENDING"  # PENDING | IN_PROGRESS | DONE | FAILED | SKIPPED
    attempts: int = 0
    result: Optional[Any] = None

    @property
    def ready(self) -> bool:
        return self.status == "PENDING" and not self.depends_on


@dataclass
class Plan:
    plan_id: str
    goal: str
    shape: PlanShape
    steps: List[PlanStep] = field(default_factory=list)
    revisions: int = 0
    created_at: float = field(default_factory=time.time)

    def pending(self) -> List[PlanStep]:
        return [s for s in self.steps if s.status in ("PENDING", "IN_PROGRESS")]

    def progress(self) -> float:
        if not self.steps:
            return 0.0
        done = sum(1 for s in self.steps if s.status == "DONE")
        return done / len(self.steps)

    def render(self) -> str:
        lines = [f"PLAN {self.plan_id} for: {self.goal} (shape={self.shape.value}, rev={self.revisions})"]
        for s in self.steps:
            marker = {"DONE": "x", "FAILED": "!", "IN_PROGRESS": ">", "SKIPPED": "-"}.get(s.status, " ")
            deps = f" (needs: {', '.join(s.depends_on)})" if s.depends_on else ""
            lines.append(f"  [{marker}] {s.step_id}: {s.description}{deps}")
        return "\n".join(lines)


class Planner:
    """Produces plans. Default is deterministic keyword heuristics; an LLM can be plugged in."""

    def __init__(self, plan_llm: Optional[Callable[[str], List[str]]] = None):
        self.plan_llm = plan_llm

    def plan(self, goal: str, shape: PlanShape = PlanShape.PLAN_EXECUTE_REPLAN) -> Plan:
        if self.plan_llm:
            raw = self.plan_llm(goal)
        else:
            raw = self._heuristic_steps(goal)
        steps = [PlanStep(step_id=f"s{i + 1}", description=d) for i, d in enumerate(raw)]
        if shape == PlanShape.DEPENDENCY_GRAPH and len(steps) >= 3:
            steps[1].depends_on = [steps[0].step_id]
            steps[2].depends_on = [steps[0].step_id]
        return Plan(plan_id=f"plan_{uuid.uuid4().hex[:8]}", goal=goal, shape=shape, steps=steps)

    @staticmethod
    def _heuristic_steps(goal: str) -> List[str]:
        g = goal.lower()
        steps: List[str] = ["Clarify success criteria and constraints"]
        if any(k in g for k in ("research", "analyz", "investigat", "find")):
            steps.append("Gather and grade source material")
        if any(k in g for k in ("build", "implement", "create", "generat", "design")):
            steps.append("Produce first working artifact")
            steps.append("Self-review artifact against criteria")
        if any(k in g for k in ("deploy", "production", "launch")):
            steps.append("Run safety and rollback checks")
        steps.append("Verify outcome with an externally checkable predicate")
        return steps


class PlanExecutor:
    """
    Executes a plan against an executor callback. Handles:
    - dependency-order dispatch (graph shape),
    - bounded retries with escalation ladder (retry -> replan -> human),
    - revision counting (replans are visible on the Plan).
    """

    def __init__(
        self,
        executor: Callable[[PlanStep], Any],
        max_step_attempts: int = 2,
        max_replans: int = 2,
        replanner: Optional[Callable[[Plan, PlanStep], Plan]] = None,
        on_escalate: Optional[Callable[[PlanStep, str], None]] = None,
    ):
        self.executor = executor
        self.max_step_attempts = max_step_attempts
        self.max_replans = max_replans
        self.replanner = replanner
        self.on_escalate = on_escalate
        self.escalations: List[Dict[str, Any]] = []

    def run(self, plan: Plan) -> Plan:
        while True:
            progressed = self._execute_pass(plan)
            if not plan.pending():
                failed = [s for s in plan.steps if s.status == "FAILED"]
                if failed:
                    if plan.revisions < self.max_replans and self.replanner:
                        # replan after terminal failures (escalation ladder: retry -> replan -> human)
                        new_plan = self.replanner(plan, failed[0])
                        new_plan.revisions = plan.revisions + 1
                        plan = new_plan
                        continue
                    # no replanner / replans exhausted: escalate failures to human
                    for s in failed:
                        self.escalations.append({"step": s.step_id, "reason": "exhausted retries and replans"})
                        if self.on_escalate:
                            self.on_escalate(s, "human")
                return plan
            if progressed:
                continue
            # nothing progressed -> blocked: escalate or replan
            blocked = plan.pending()[0]
            if plan.revisions < self.max_replans and self.replanner:
                new_plan = self.replanner(plan, blocked)
                new_plan.revisions = plan.revisions + 1
                plan = new_plan
                continue
            self.escalations.append({"step": blocked.step_id, "reason": "exhausted retries and replans"})
            if self.on_escalate:
                self.on_escalate(blocked, "human")
            blocked.status = "FAILED"
            return plan

    def _execute_pass(self, plan: Plan) -> bool:
        progressed = False
        for step in plan.steps:
            if step.status not in ("PENDING", "IN_PROGRESS"):
                continue
            deps_done = all(
                next((d for d in plan.steps if d.step_id == dep)).status == "DONE"
                for dep in step.depends_on
            )
            if not deps_done:
                if any(next((d for d in plan.steps if d.step_id == dep)).status in ("FAILED", "SKIPPED")
                       for dep in step.depends_on):
                    step.status = "SKIPPED"  # dependency failed; do not cascade execution
                    progressed = True
                continue
            step.status = "IN_PROGRESS"
            step.attempts += 1
            try:
                step.result = self.executor(step)
                step.status = "DONE"
                progressed = True
            except Exception as exc:
                if step.attempts >= self.max_step_attempts:
                    step.status = "FAILED"
                    step.result = str(exc)
                    progressed = True  # failure is terminal progress for this pass
                else:
                    step.status = "PENDING"  # will retry next pass
                    progressed = True  # a scheduled retry is forward motion, not a block
        return progressed


# ---------------------------------------------------------------------------
# ReAct scaffold
# ---------------------------------------------------------------------------

REACT_TEMPLATE = """Thought: I need to figure out {goal_step}.
Action: {tool_name}
Action Input: {arguments}
Observation: {observation}
... (repeat Thought/Action/Observation as needed)
Thought: I now know the final answer.
Final Answer: {answer}"""


class ReActScaffold:
    """
    Textual ReAct scaffold for providers without native tool calling:
    renders the loop contract into the prompt and parses Thought/Action lines.
    """

    ACTION_RE = None  # compiled lazily to avoid import cost at module load

    @classmethod
    def parse(cls, text: str) -> List[Dict[str, str]]:
        import re

        if cls.ACTION_RE is None:
            cls.ACTION_RE = re.compile(
                r"Action:\s*(?P<tool>\w+)\s*\nAction Input:\s*(?P<args>\{.*?\}|\S+)",
                re.DOTALL,
            )
        actions = []
        for m in cls.ACTION_RE.finditer(text):
            raw = m.group("args").strip()
            try:
                import json

                args = json.loads(raw)
            except Exception:
                args = {"input": raw}
            actions.append({"tool": m.group("tool"), "arguments": args})
        return actions

    @classmethod
    def render(cls, goal: str, available_tools: Sequence[str]) -> str:
        tool_lines = "\n".join(f"- {t}" for t in available_tools)
        return (
            f"Goal: {goal}\nAvailable tools:\n{tool_lines}\n\n"
            "Reason strictly in this format per step:\n"
            "Thought: <reasoning>\nAction: <tool>\nAction Input: <json args>\n"
            "and end with:\nFinal Answer: <answer>"
        )
