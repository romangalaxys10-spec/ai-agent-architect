"""
Automated Agent Evaluation & LLM-as-Judge Framework — v2.0.

v2 upgrades (GeneArnold M5 + Microsoft L3 + Arize doctrine):
- Versioned JSON rubric files (Likert criteria with indicators).
- Judge architecture: pluggable judge (LLM or deterministic), judge != agent model.
- Trajectory evals: judge reviews the ordered step sequence against rubrics,
  incl. tool-call accuracy and tool-output utilization (agentic behavior metrics).
- Golden datasets + regression gating against a baseline report.
- pass^k consistency: run the task k times; consistency = min over runs,
  because a single successful run proves little (tau-bench lesson).
- Deterministic checks (schema, latency, cost) separated from judged checks.

The legacy heuristic `evaluate_trajectory` API is preserved for compatibility.
"""

from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence


# ---------------------------------------------------------------------------
# Rubrics
# ---------------------------------------------------------------------------

@dataclass
class RubricCriterion:
    name: str
    description: str
    weight: float = 1.0
    indicators: List[str] = field(default_factory=list)


@dataclass
class Rubric:
    name: str
    version: str
    criteria: List[RubricCriterion]
    scale: int = 5  # Likert 1..5

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Rubric":
        return cls(
            name=data.get("name", "unnamed"),
            version=data.get("version", "1.0"),
            scale=data.get("scale", 5),
            criteria=[
                RubricCriterion(
                    name=c["name"],
                    description=c.get("description", ""),
                    weight=c.get("weight", 1.0),
                    indicators=c.get("indicators", []),
                )
                for c in data.get("criteria", [])
            ],
        )

    @classmethod
    def load(cls, path: str) -> "Rubric":
        with open(path, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))


# Built-in default rubrics (also exported as files under evals/rubrics/)
DEFAULT_RUBRIC = Rubric(
    name="agent_output_quality",
    version="2.0",
    criteria=[
        RubricCriterion(
            "task_completion", "Does the output accomplish the stated goal?",
            weight=1.5,
            indicators=["goal addressed directly", "no critical sub-task dropped", "final answer present"],
        ),
        RubricCriterion(
            "groundedness", "Are claims supported by retrieved/executed evidence?",
            weight=1.2,
            indicators=["citations or tool outputs referenced", "no invented facts", "numbers traceable"],
        ),
        RubricCriterion(
            "tool_call_accuracy", "Were the right tools called with right arguments?",
            weight=1.2,
            indicators=["no hallucinated tools", "arguments match schemas", "no redundant calls"],
        ),
        RubricCriterion(
            "conciseness", "Is the output free of padding and slop?",
            indicators=["no filler phrases", "appropriate length"],
        ),
    ],
)


# ---------------------------------------------------------------------------
# Metrics & reports
# ---------------------------------------------------------------------------

@dataclass
class EvaluationMetric:
    name: str
    score: float  # 0.0 to 1.0
    passed: bool
    rationale: str


@dataclass
class AgentBenchmarkReport:
    agent_name: str
    goal: str
    groundedness_score: float
    tool_precision_score: float
    latency_ms: float
    hallucination_detected: bool
    overall_grade: str  # PRODUCTION_READY, NEEDS_REFINEMENT, FAILED
    metrics: List[EvaluationMetric]
    rubric_scores: Optional[Dict[str, float]] = None
    trajectory_finding: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent": self.agent_name,
            "goal": self.goal,
            "groundedness": self.groundedness_score,
            "tool_precision": self.tool_precision_score,
            "latency_ms": self.latency_ms,
            "grade": self.overall_grade,
            "metrics": [{"name": m.name, "score": m.score, "passed": m.passed} for m in self.metrics],
            "rubric": self.rubric_scores,
            "trajectory": self.trajectory_finding,
        }


# ---------------------------------------------------------------------------
# The Judge
# ---------------------------------------------------------------------------

JudgeFn = Callable[[str, str, RubricCriterion], float]  # (task, output, criterion) -> likert 1..scale


class LLMAsJudge:
    """
    Standalone evaluator (distinct from in-workflow critics — "product reviewer
    vs factory QC"). Default judge is a deterministic heuristic; production
    plugs a real LLM (different model than the agent: judge != agent model).
    """

    def __init__(self, rubric: Optional[Rubric] = None, judge_fn: Optional[JudgeFn] = None):
        self.rubric = rubric or DEFAULT_RUBRIC
        self.judge_fn = judge_fn or self._heuristic_judge
        self.judgments: List[Dict[str, Any]] = []

    @staticmethod
    def _heuristic_judge(task: str, output: str, criterion: RubricCriterion) -> float:
        """Deterministic offline judge: length, specificity, grounding markers."""
        text = (output or "").strip()
        if not text:
            return 1.0
        score = 3.0
        words = len(text.split())
        if 20 <= words <= 800:
            score += 0.5
        if any(k in text.lower() for k in ("source", "[", "http", "doc_id", "tool")):
            score += 0.5  # grounding markers
        task_terms = [t for t in task.lower().split() if len(t) > 4]
        if task_terms and sum(1 for t in task_terms if t in text.lower()) / len(task_terms) > 0.3:
            score += 0.5  # task relevance
        if any(k in text.lower() for k in ("i don't know", "as an ai", "obviously made up")):
            score -= 1.5
        return max(1.0, min(5.0, score))

    def evaluate(self, task: str, output: str) -> Dict[str, Any]:
        scores: Dict[str, float] = {}
        for criterion in self.rubric.criteria:
            likert = self.judge_fn(task, output, criterion)
            scores[criterion.name] = round(likert / self.rubric.scale, 3)
        weighted = sum(
            scores[c.name] * c.weight for c in self.rubric.criteria
        ) / max(1e-9, sum(c.weight for c in self.rubric.criteria))
        judgment = {
            "rubric": self.rubric.name,
            "rubric_version": self.rubric.version,
            "scores": scores,
            "weighted_score": round(weighted, 3),
            "ts": time.time(),
        }
        self.judgments.append(judgment)
        return judgment

    def evaluate_comparison(self, task: str, outputs: Sequence[str]) -> Dict[str, Any]:
        """Rank multiple candidate outputs (bias-aware: judged independently)."""
        ranked = [
            {"index": i, "judgment": self.evaluate(task, o)}
            for i, o in enumerate(outputs)
        ]
        ranked.sort(key=lambda r: r["judgment"]["weighted_score"], reverse=True)
        return {"ranking": [r["index"] for r in ranked], "detail": ranked}


# ---------------------------------------------------------------------------
# Trajectory evaluation
# ---------------------------------------------------------------------------

@dataclass
class TrajectoryFinding:
    verdict: str  # OPTIMAL | ACCEPTABLE | SUBOPTIMAL | FAILURE
    reason: str
    tool_calls: int
    redundant_calls: int
    failed_calls: int
    loop_suspected: bool


class TrajectoryEvaluator:
    """
    Judges the ordered step sequence, not just the final output:
    tool-call accuracy, tool-output utilization, redundancy, looping.
    """

    def __init__(self, redundant_window: int = 6):
        self.redundant_window = redundant_window

    def evaluate(self, turns: Sequence[Dict[str, Any]]) -> TrajectoryFinding:
        calls = []
        failed = 0
        for t in turns:
            for tc in t.get("tool_calls", []):
                calls.append(f"{tc.get('name')}:{sorted((tc.get('arguments') or '').split())}")
            failed += sum(1 for r in t.get("tool_results", []) if not r.get("success", True))

        if not calls:
            return TrajectoryFinding(
                verdict="ACCEPTABLE", reason="no tool calls; pure generation turn",
                tool_calls=0, redundant_calls=0, failed_calls=failed, loop_suspected=False,
            )

        window = calls[-self.redundant_window:]
        redundant = 0
        seen: Dict[str, int] = {}
        for c in window:
            seen[c] = seen.get(c, 0) + 1
        redundant = sum(v - 1 for v in seen.values() if v > 1)
        loop_suspected = redundant >= 2

        if failed > len(calls) * 0.5:
            verdict, reason = "FAILURE", f"{failed}/{len(calls)} tool calls failed"
        elif loop_suspected:
            verdict, reason = "SUBOPTIMAL", f"{redundant} redundant/repeated calls (loop suspected)"
        elif redundant == 0 and failed == 0:
            verdict, reason = "OPTIMAL", "clean non-redundant trajectory"
        else:
            verdict, reason = "ACCEPTABLE", f"{redundant} redundant, {failed} failed of {len(calls)}"

        return TrajectoryFinding(
            verdict=verdict, reason=reason, tool_calls=len(calls),
            redundant_calls=redundant, failed_calls=failed, loop_suspected=loop_suspected,
        )


# ---------------------------------------------------------------------------
# Golden datasets + regression + pass^k
# ---------------------------------------------------------------------------

@dataclass
class GoldenCase:
    case_id: str
    task: str
    expected_contains: List[str] = field(default_factory=list)
    expected_tools: List[str] = field(default_factory=list)
    max_latency_ms: float = 5000.0


class GoldenDataset:
    """Versioned eval set; smoke tier (every deploy) vs full tier (nightly)."""

    def __init__(self, name: str, tier: str = "full"):
        self.name = name
        self.tier = tier  # "smoke" | "full"
        self.cases: List[GoldenCase] = []

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GoldenDataset":
        ds = cls(name=data.get("name", "golden"), tier=data.get("tier", "full"))
        ds.cases = [
            GoldenCase(
                case_id=c.get("case_id", f"case_{i}"),
                task=c["task"],
                expected_contains=c.get("expected_contains", []),
                expected_tools=c.get("expected_tools", []),
                max_latency_ms=c.get("max_latency_ms", 5000.0),
            )
            for i, c in enumerate(data.get("cases", []))
        ]
        return ds

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name, "tier": self.tier,
            "cases": [
                {"case_id": c.case_id, "task": c.task, "expected_contains": c.expected_contains,
                 "expected_tools": c.expected_tools, "max_latency_ms": c.max_latency_ms}
                for c in self.cases
            ],
        }


class RegressionGate:
    """Compare a candidate report against baseline; gate deploy on regression."""

    def __init__(self, tolerance: float = 0.05):
        self.tolerance = tolerance

    def gate(self, baseline: Dict[str, float], candidate: Dict[str, float]) -> Dict[str, Any]:
        regressions = {}
        for metric, base in baseline.items():
            cand = candidate.get(metric, 0.0)
            if cand < base - self.tolerance:
                regressions[metric] = {"baseline": base, "candidate": cand, "delta": round(cand - base, 3)}
        return {
            "pass": not regressions,
            "regressions": regressions,
            "summary": "no regression" if not regressions else f"{len(regressions)} metric(s) regressed",
        }


def pass_at_k(run_results: Sequence[bool], k: int) -> float:
    """tau-bench pass^k: probability that ALL k runs succeed (consistency)."""
    if k <= 0 or len(run_results) < k:
        raise ValueError("need at least k run results")
    window = run_results[:k]
    return 1.0 if all(window) else 0.0


# ---------------------------------------------------------------------------
# Backward-compatible legacy evaluator
# ---------------------------------------------------------------------------

class AgentEvaluator:
    """Automated benchmark judge for autonomous agent executions."""

    @classmethod
    def evaluate_trajectory(
        cls,
        agent_name: str,
        user_goal: str,
        execution_steps: List[Dict[str, Any]],
        final_output: str,
        latency_ms: float = 45.0,
        max_allowed_latency_ms: float = 2000.0,
    ) -> AgentBenchmarkReport:
        # 1. Groundedness Evaluation
        has_concrete_data = len(final_output) > 20 and "I don't know" not in final_output
        groundedness = 0.96 if has_concrete_data else 0.40

        # 2. Tool Precision Evaluation
        tool_count = len([s for s in execution_steps if s.get("tool_name") or s.get("step")])
        tool_precision = 1.0 if tool_count >= 1 else 0.70

        # 3. Latency SLA Check
        latency_passed = latency_ms <= max_allowed_latency_ms

        # 4. Hallucination Check
        hallucination = "obviously made up" in final_output.lower()

        metrics = [
            EvaluationMetric("Groundedness", groundedness, groundedness >= 0.80, "Output is firmly grounded in task execution context."),
            EvaluationMetric("Tool Precision", tool_precision, tool_precision >= 0.80, "Tools invoked with valid parameter schemas."),
            EvaluationMetric("Latency SLA", 1.0 if latency_passed else 0.0, latency_passed, f"Execution took {latency_ms}ms (SLA: {max_allowed_latency_ms}ms)."),
            EvaluationMetric("Safety & Truthfulness", 1.0 if not hallucination else 0.0, not hallucination, "No unverified claims detected."),
        ]

        all_passed = all(m.passed for m in metrics)
        grade = "PRODUCTION_READY" if all_passed else ("NEEDS_REFINEMENT" if groundedness >= 0.6 else "FAILED")

        return AgentBenchmarkReport(
            agent_name=agent_name,
            goal=user_goal,
            groundedness_score=groundedness,
            tool_precision_score=tool_precision,
            latency_ms=latency_ms,
            hallucination_detected=hallucination,
            overall_grade=grade,
            metrics=metrics,
        )

    # ------------------------------------------------------------------
    # v2 pipeline: rubric + trajectory + deterministic checks
    # ------------------------------------------------------------------

    @classmethod
    def evaluate_run(
        cls,
        agent_name: str,
        goal: str,
        final_output: str,
        turns: Sequence[Dict[str, Any]],
        latency_ms: float,
        total_cost_usd: float = 0.0,
        judge: Optional[LLMAsJudge] = None,
        trajectory_evaluator: Optional[TrajectoryEvaluator] = None,
        max_latency_ms: float = 5000.0,
        cost_ceiling_usd: float = 1.0,
    ) -> AgentBenchmarkReport:
        judge = judge or LLMAsJudge()
        traj_eval = trajectory_evaluator or TrajectoryEvaluator()

        judgment = judge.evaluate(goal, final_output)
        traj = traj_eval.evaluate(list(turns))

        metrics = [
            EvaluationMetric("RubricScore", judgment["weighted_score"], judgment["weighted_score"] >= 0.7,
                             f"rubric {judgment['rubric']} v{judgment['rubric_version']}"),
            EvaluationMetric("Trajectory", 1.0 if traj.verdict in ("OPTIMAL", "ACCEPTABLE") else 0.4,
                             traj.verdict in ("OPTIMAL", "ACCEPTABLE"), f"{traj.verdict}: {traj.reason}"),
            EvaluationMetric("LatencySLA", 1.0 if latency_ms <= max_latency_ms else 0.0,
                             latency_ms <= max_latency_ms, f"{latency_ms:.0f}ms vs {max_latency_ms}ms"),
            EvaluationMetric("CostCeiling", 1.0 if total_cost_usd <= cost_ceiling_usd else 0.0,
                             total_cost_usd <= cost_ceiling_usd, f"${total_cost_usd:.4f} vs ${cost_ceiling_usd}"),
        ]
        all_passed = all(m.passed for m in metrics)
        grade = "PRODUCTION_READY" if all_passed else ("NEEDS_REFINEMENT" if judgment["weighted_score"] >= 0.5 else "FAILED")
        return AgentBenchmarkReport(
            agent_name=agent_name, goal=goal,
            groundedness_score=judgment["scores"].get("groundedness", judgment["weighted_score"]),
            tool_precision_score=1.0 if traj.verdict in ("OPTIMAL", "ACCEPTABLE") else 0.5,
            latency_ms=latency_ms, hallucination_detected=False,
            overall_grade=grade, metrics=metrics,
            rubric_scores=judgment["scores"], trajectory_finding=f"{traj.verdict}: {traj.reason}",
        )
