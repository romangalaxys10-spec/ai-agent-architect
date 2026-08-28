"""
Senior System Architect Engine.
Decomposes requirements into a cognitive DAG, checks anti-patterns, and emits
an architecture blueprint wired to the framework's own primitives
(agent loop, memory tiers, tool registry, guardrails, evals).
"""

from dataclasses import dataclass
from typing import Dict, List, Any
import os
import sys

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def _load_repo_module(name: str, relpath: str):
    """Load a repo-level module by explicit path (avoids 'core' package name clash)."""
    import importlib.util
    path = os.path.join(_REPO_ROOT, relpath)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


DepthCognitiveEngine = _load_repo_module("depth_cognitive_engine", "core/depth_cognitive_engine.py").DepthCognitiveEngine


COGNITIVE_MODULES = [
    ("Perception", "Ingest goals, context, and environment signals"),
    ("Planning", "Decompose into steps, dependencies, budgets"),
    ("Execution", "Dispatch tool calls with validation and sandboxing"),
    ("Memory", "Working / episodic / semantic / vector tiers"),
    ("Verification", "Externally checkable success predicates + evals"),
    ("Guardrails", "Input/output/execution rails + HITL gates"),
]

ANTI_PATTERNS = {
    "tight_coupling": "Modules reach into each other's internals; swap in interfaces + events.",
    "unbounded_loop": "No step/token/wall-clock ceiling; wire BudgetPortfolio + LoopDetector.",
    "unverified_tool_call": "Tools invoked without schema validation or idempotency ledger.",
    "unbounded_memory": "Context grows without compaction; wire Compactor + notes recitation.",
    "no_hitl": "Irreversible actions without approval gates; wire ApprovalPolicy.",
    "no_observability": "No spans/cost metering; wire TelemetryTracer + JSONLLogger + CostLedger.",
    "prompt_as_orchestration": "Control flow living inside free-text prompts; move to code.",
}


@dataclass
class ArchitectureBlueprint:
    system_name: str
    requirement: str
    modules: List[Dict[str, Any]]
    dag_edges: List[Dict[str, str]]
    detected_anti_patterns: List[str]
    remedies: List[str]
    temporal_horizons: Dict[str, str]
    depth_score: int
    verdict: str


class SeniorArchitectEngine:
    """Autonomous architectural design, cognitive DAG decomposition, zero-trust review."""

    @classmethod
    def decompose(cls, requirement: str, system_name: str = "UnnamedSystem") -> ArchitectureBlueprint:
        depth = DepthCognitiveEngine.analyze_cognitive_depth(requirement)

        modules = [{"name": n, "responsibility": r} for n, r in COGNITIVE_MODULES]
        edges = [
            {"from": "Perception", "to": "Planning"},
            {"from": "Planning", "to": "Execution"},
            {"from": "Execution", "to": "Verification"},
            {"from": "Verification", "to": "Planning", "label": "replan-on-failure"},
            {"from": "Execution", "to": "Memory", "label": "episodic-write"},
            {"from": "Memory", "to": "Planning", "label": "recall"},
            {"from": "Execution", "to": "Guardrails", "label": "pre-dispatch-rail"},
            {"from": "Guardrails", "to": "Verification", "label": "audit-trail"},
        ]

        req = requirement.lower()
        detected = [k for k, hint in {
            "tight_coupling": any(w in req for w in ("monolith", "everything in one", "tightly coupled")),
            "unbounded_loop": any(w in req for w in ("autonomous", "long-running", "while true", "forever")),
            "unverified_tool_call": "tool" in req or "mcp" in req,
            "unbounded_memory": any(w in req for w in ("chat history", "long sessions", "documents")),
            "no_hitl": any(w in req for w in ("payments", "deploy", "delete", "email")),
            "no_observability": True,  # assume missing until proven otherwise (zero-trust)
            "prompt_as_orchestration": any(w in req for w in ("mega prompt", "one big prompt")),
        }.items() if hint]

        remedies = [ANTI_PATTERNS[k] for k in detected]

        temporal = {
            "day_1": "Single-node deployment; EchoProvider offline tests green; smoke suite passes.",
            "day_30": "Persistence + cost dashboards; golden-dataset regression gate on every PR.",
            "year_1": "Multi-tenant namespaces; A2A federation; eval-gated model promotions.",
        }

        verdict = (
            "ARCHITECTURE_SOUND"
            if len(detected) <= 2
            else "NEEDS_HARDENING" if len(detected) <= 4
            else "ARCHITECTURE_RISK"
        )

        return ArchitectureBlueprint(
            system_name=system_name,
            requirement=requirement,
            modules=modules,
            dag_edges=edges,
            detected_anti_patterns=detected,
            remedies=remedies,
            temporal_horizons=temporal,
            depth_score=depth.depth_score,
            verdict=verdict,
        )

    @classmethod
    def format_blueprint(cls, bp: ArchitectureBlueprint) -> str:
        lines = [
            f"# Architecture Blueprint: {bp.system_name}",
            f"Requirement: {bp.requirement}",
            f"Verdict: {bp.verdict}  |  Depth Score: {bp.depth_score}/10",
            "",
            "## Cognitive Modules",
        ]
        lines += [f"- **{m['name']}**: {m['responsibility']}" for m in bp.modules]
        lines.append("\n## DAG Edges")
        lines += [f"- {e['from']} -> {e['to']} {e.get('label', '')}".strip() for e in bp.dag_edges]
        lines.append("\n## Anti-Patterns Detected")
        lines += [f"- {a}" for a in bp.detected_anti_patterns] or ["- none"]
        lines.append("\n## Remedies")
        lines += [f"- {r}" for r in bp.remedies] or ["- none required"]
        lines.append("\n## Temporal Horizons")
        lines += [f"- **{k.replace('_', ' ').title()}**: {v}" for k, v in bp.temporal_horizons.items()]
        return "\n".join(lines)
