"""
Workflow Patterns (Anthropic "Building Effective Agents", Dec 2024).

First-class implementations of the five canonical workflow patterns plus the
autonomous agent loop, each with the documented decision rule:

1. PromptChaining        — sequential steps with programmatic gates.
2. Router                — classify input, dispatch to specialized handler.
3. Parallelization       — sectioning (independent subtasks) or voting (N runs + threshold).
4. OrchestratorWorkers   — central LLM decomposes dynamically, workers execute, synthesis.
5. EvaluatorOptimizer    — generator + evaluator refinement loop.

Doctrine: workflows = predefined code paths (predictable); agents = dynamic
self-direction (flexible). Use the least autonomous shape that solves the task.
"""

from __future__ import annotations

import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence, TypeVar

from .llm.providers import LLMProvider, Message, Role

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Shared types
# ---------------------------------------------------------------------------

@dataclass
class WorkflowStepResult:
    name: str
    output: Any
    gate_passed: bool = True
    latency_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowRun:
    run_id: str
    pattern: str
    results: List[WorkflowStepResult] = field(default_factory=list)
    final_output: Any = None
    decision_rule: str = ""

    @property
    def total_latency_ms(self) -> float:
        return sum(r.latency_ms for r in self.results)


# ---------------------------------------------------------------------------
# 1. Prompt chaining with gates
# ---------------------------------------------------------------------------

@dataclass
class ChainStep:
    name: str
    prompt_template: str  # "{input}" placeholder
    model: str = "echo-local"
    gate: Optional[Callable[[str], bool]] = None  # programmatic quality gate
    gate_failure_message: str = "Gate failed"


class PromptChain:
    """
    Each call processes the previous output; gates between steps can stop early.
    Use when: task decomposes into fixed subtasks. Trades latency for accuracy.
    """

    def __init__(self, provider: LLMProvider, steps: Sequence[ChainStep]):
        self.provider = provider
        self.steps = list(steps)

    def run(self, initial_input: str) -> WorkflowRun:
        run = WorkflowRun(run_id=f"chain_{uuid.uuid4().hex[:8]}", pattern="prompt_chaining",
                          decision_rule="Fixed subtasks, gates between steps")
        current = initial_input
        for step in self.steps:
            t0 = time.time()
            resp = self.provider.complete(
                [Message.user(step.prompt_template.format(input=current))], model=step.model
            )
            out = resp.content or ""
            passed = True
            if step.gate is not None:
                passed = step.gate(out)
            run.results.append(WorkflowStepResult(
                name=step.name, output=out, gate_passed=passed,
                latency_ms=(time.time() - t0) * 1000,
            ))
            if not passed:
                run.final_output = f"{step.gate_failure_message} at step '{step.name}'"
                return run
            current = out
        run.final_output = current
        return run


# ---------------------------------------------------------------------------
# 2. Router
# ---------------------------------------------------------------------------

@dataclass
class Route:
    name: str
    condition: Callable[[str], bool]  # deterministic classifier
    handler: Callable[[str], Any]
    description: str = ""


class RouterWorkflow:
    """
    Classify input, dispatch to specialized prompt/handler/model.
    Use when: input categories need different treatment (triage, model routing).
    """

    def __init__(self, routes: Sequence[Route], default_handler: Optional[Callable[[str], Any]] = None):
        self.routes = list(routes)
        self.default_handler = default_handler
        self.routing_log: List[Dict[str, Any]] = []

    def route(self, text: str) -> Optional[Route]:
        for r in self.routes:
            if r.condition(text):
                self.routing_log.append({"route": r.name, "ts": time.time()})
                return r
        return None

    def run(self, text: str) -> WorkflowRun:
        run = WorkflowRun(run_id=f"route_{uuid.uuid4().hex[:8]}", pattern="routing",
                          decision_rule="Separate attention: classify then dispatch")
        t0 = time.time()
        chosen = self.route(text)
        if chosen is None and self.default_handler is not None:
            out = self.default_handler(text)
            name = "default"
        elif chosen is not None:
            out = chosen.handler(text)
            name = chosen.name
        else:
            out = "no route matched and no default handler configured"
            name = "unrouted"
        run.results.append(WorkflowStepResult(name=name, output=out, latency_ms=(time.time() - t0) * 1000))
        run.final_output = out
        return run


# ---------------------------------------------------------------------------
# 3. Parallelization: sectioning + voting
# ---------------------------------------------------------------------------

class Parallelization:
    """
    Sectioning: independent subtasks fan out concurrently (e.g. answer + safety check).
    Voting: same prompt N times, aggregate by threshold/majority (diverse reviewers).
    """

    def __init__(self, provider: LLMProvider, max_workers: int = 4):
        self.provider = provider
        self.max_workers = max_workers

    def section(self, prompt: str, section_prompts: Sequence[str], model: str = "echo-local") -> WorkflowRun:
        run = WorkflowRun(run_id=f"par_{uuid.uuid4().hex[:8]}", pattern="parallelization.sectioning",
                          decision_rule="Independent subtasks, latency-bound")
        t0 = time.time()

        def _one(p: str) -> WorkflowStepResult:
            s = time.time()
            resp = self.provider.complete([Message.user(p)], model=model)
            return WorkflowStepResult(name=p[:40], output=resp.content, latency_ms=(time.time() - s) * 1000)

        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            run.results = list(pool.map(_one, section_prompts))
        run.final_output = [r.output for r in run.results]
        run.results.insert(0, WorkflowStepResult(name="fanout", output=f"{len(section_prompts)} sections",
                                                 latency_ms=(time.time() - t0) * 1000))
        return run

    def vote(self, prompt: str, n: int = 3, model: str = "echo-local",
             threshold: float = 0.5) -> WorkflowRun:
        """Run the same prompt n times; a candidate wins if >= threshold fraction agree."""
        run = WorkflowRun(run_id=f"vote_{uuid.uuid4().hex[:8]}", pattern="parallelization.voting",
                          decision_rule="Diversity via repetition; threshold aggregation")

        def _one(_: int) -> str:
            return self.provider.complete([Message.user(prompt)], model=model).content or ""

        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            outputs = list(pool.map(_one, range(n)))
        counts: Dict[str, int] = {}
        for o in outputs:
            counts[o] = counts.get(o, 0) + 1
        best, best_count = max(counts.items(), key=lambda kv: kv[1]) if counts else (None, 0)
        consensus = best_count / max(1, n) >= threshold
        run.results.append(WorkflowStepResult(
            name="tally", output={"votes": counts, "winner": best, "consensus": consensus},
        ))
        run.final_output = best if consensus else outputs[0] if outputs else None
        return run


# ---------------------------------------------------------------------------
# 4. Orchestrator-workers
# ---------------------------------------------------------------------------

class OrchestratorWorkers:
    """
    Central LLM dynamically decomposes the task into worker subtasks (unlike
    parallelization: subtasks are NOT predefined), workers execute, orchestrator
    synthesizes. Use for: coding across unpredictable files, multi-source research.
    """

    def __init__(self, provider: LLMProvider, worker: Callable[[str], Any],
                 model: str = "echo-local", max_workers: int = 4):
        self.provider = provider
        self.worker = worker
        self.model = model
        self.max_workers = max_workers

    def decompose(self, task: str) -> List[str]:
        """Default deterministic decomposition; override or provide LLM planner."""
        resp = self.provider.complete(
            [Message.user(f"Decompose this task into 2-4 independent worker subtasks, "
                          f"one per line, no numbering:\n{task}")],
            model=self.model,
        )
        lines = [ln.strip("- ").strip() for ln in (resp.content or "").splitlines() if ln.strip()]
        # Filter echo noise deterministically
        lines = [ln for ln in lines if ln and not ln.startswith("[echo")]
        return lines[:4] or [task]

    def run(self, task: str) -> WorkflowRun:
        run = WorkflowRun(run_id=f"orch_{uuid.uuid4().hex[:8]}", pattern="orchestrator_workers",
                          decision_rule="Dynamic decomposition; subtasks not predefined")
        subtasks = self.decompose(task)
        run.results.append(WorkflowStepResult(name="decompose", output=subtasks))

        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            outputs = list(pool.map(self.worker, subtasks))
        for st, out in zip(subtasks, outputs):
            run.results.append(WorkflowStepResult(name=st[:40], output=out))
        synthesis = self.provider.complete(
            [Message.user(f"Synthesize a unified answer from these worker outputs "
                          f"for the task '{task}':\n{outputs}")],
            model=self.model,
        )
        run.results.append(WorkflowStepResult(name="synthesize", output=synthesis.content))
        run.final_output = synthesis.content
        return run


# ---------------------------------------------------------------------------
# 5. Evaluator-optimizer
# ---------------------------------------------------------------------------

@dataclass
class EvalScore:
    score: float          # 0..1
    feedback: str
    passed: bool


class EvaluatorOptimizer:
    """
    Generator + evaluator refinement loop. Use when: clear evaluation criteria
    exist and feedback demonstrably improves output (ed-donner Sidekick pattern:
    retry / ask-user / accept outcomes with max attempts).
    """

    def __init__(
        self,
        provider: LLMProvider,
        evaluator: Callable[[str, str], EvalScore],
        generator_prompt: str = "Produce the best possible output for: {input}\n\nPrevious feedback: {feedback}",
        max_iterations: int = 3,
        score_threshold: float = 0.8,
        model: str = "echo-local",
        on_exhausted: str = "accept_best",  # accept_best | ask_human
    ):
        self.provider = provider
        self.evaluator = evaluator
        self.generator_prompt = generator_prompt
        self.max_iterations = max_iterations
        self.score_threshold = score_threshold
        self.model = model
        self.on_exhausted = on_exhausted

    def run(self, task: str) -> WorkflowRun:
        run = WorkflowRun(run_id=f"evalopt_{uuid.uuid4().hex[:8]}", pattern="evaluator_optimizer",
                          decision_rule="Clear criteria + feedback improves output")
        feedback = "none yet"
        best_output, best_score = None, -1.0
        for i in range(self.max_iterations):
            t0 = time.time()
            resp = self.provider.complete(
                [Message.user(self.generator_prompt.format(input=task, feedback=feedback))],
                model=self.model,
            )
            output = resp.content or ""
            verdict = self.evaluator(task, output)
            run.results.append(WorkflowStepResult(
                name=f"iteration_{i + 1}", output=output, metadata={"score": verdict.score, "feedback": verdict.feedback},
                latency_ms=(time.time() - t0) * 1000,
            ))
            if verdict.score > best_score:
                best_output, best_score = output, verdict.score
            if verdict.passed:
                run.final_output = output
                return run
            feedback = verdict.feedback
        if self.on_exhausted == "ask_human":
            run.final_output = {"needs_human_review": True, "best_output": best_output, "best_score": best_score}
        else:
            run.final_output = best_output
        return run


PATTERN_SELECTION_GUIDE = {
    "prompt_chaining": "Task decomposes into fixed subtasks; gates add accuracy.",
    "routing": "Inputs fall into distinct categories needing different treatment.",
    "parallelization.sectioning": "Independent subtasks; latency matters.",
    "parallelization.voting": "Diverse verdicts needed; majority raises precision.",
    "orchestrator_workers": "Subtasks cannot be predicted in advance.",
    "evaluator_optimizer": "Clear evaluation criteria; feedback measurably improves output.",
    "agent_loop": "Open-ended task count / unpredictable tool sequences required.",
}
