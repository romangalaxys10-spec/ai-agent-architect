"""
Migration Planner Engine.
Turns "move from X to Y" into a phased, reversible migration campaign with
risk gates, rollback points, effort estimates, and HITL approval checkpoints.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class MigrationPhase:
    number: int
    name: str
    steps: List[str]
    risk_gate: str
    rollback: str
    effort_days: float
    requires_hitl: bool

@dataclass
class MigrationPlan:
    from_tech: str
    to_tech: str
    surface_inventory: dict
    phases: List[MigrationPhase] = field(default_factory=list)
    total_effort_days: float = 0.0
    irreversibility_points: List[str] = field(default_factory=list)
    verdict: str = ""

KNOWN_PLAYBOOKS = {
    ("python 3.9", "python 3.12"): "Run pyupgrade + ruff --fix; check C-extension wheels exist for 3.12; watch datetime.utcnow deprecations.",
    ("python 2", "python 3"): "six/canonical: run python-modernize, fix bytes/str boundaries first, then drop six.",
    ("django 3", "django 4"): "Fix removed deprecation paths (USE_L10N, nullfirst), then jump to 4.2 LTS.",
    ("react 17", "react 18"): "Adopt createRoot, audit third-party renderers, enable concurrent features incrementally.",
    ("vue 2", "vue 3"): "Composition API migration via @vue/composition-api bridge; audit filtered APIs.",
    ("monolith", "microservices"): "Extract by strangler-fig, NOT big-bang; start with the least-coupled capability.",
    ("mysql", "postgres"): "Dual-write during transition; watch case-sensitivity and zero-date semantics.",
    ("javascript", "typescript"): "allowJs:true -> strict in stages; type the boundaries (API layer) first.",
}

class MigrationPlannerEngine:
    """Big-bang migrations fail quietly — this plans strangler-fig style instead."""

    @classmethod
    def plan(cls, from_tech: str, to_tech: str, inventory_text: str = "") -> MigrationPlan:
        key = (from_tech.strip().lower(), to_tech.strip().lower())
        playbook = KNOWN_PLAYBOOKS.get(key, "No canned playbook: derive steps from the inventory scan below.")

        # inventory signal extraction
        inv = inventory_text or ""
        files = len(re.findall(r"^\s*\S+\.(py|ts|js|java|go|rb|php)\s*$", inv, re.M)) or len(
            re.findall(r"\S+\.(?:py|ts|js|java|go|rb|php)\b", inv))
        db_hits = len(re.findall(r"(?i)\b(migration|schema|table|model|orm)\b", inv))
        api_hits = len(re.findall(r"(?i)\b(api|route|endpoint|controller|handler)\b", inv))
        test_hits = len(re.findall(r"(?i)\b(test|spec|coverage)\b", inv))
        config_hits = len(re.findall(r"(?i)\b(config|dockerfile|yaml|toml|ini|env)\b", inv))

        surface = {
            "files_detected": files,
            "db_layer_signals": db_hits,
            "api_surface_signals": api_hits,
            "test_coverage_signals": test_hits,
            "config_signals": config_hits,
        }

        scale = max(1, files) * (1 + 0.15 * (db_hits + api_hits))
        base_days = 3 + min(scale * 0.35, 25)

        phases = [
            MigrationPhase(1, "Inventory & freeze", [
                "Generate the full inventory (files, entry points, DB objects, API routes, config).",
                "Tag each item: keep / transform / delete; publish the map as migration.md.",
                "Freeze new feature work on to-be-migrated seams (or route it behind flags).",
            ], "Inventory covers 100% of entry points, signed off by the module owners.",
             "None needed — phase is read-only.", round(base_days * 0.15, 1), True),
            MigrationPhase(2, "Compatibility shim", [
                "Introduce the shim layer (adapter interfaces) mirroring the target's contracts.",
                "Move call sites behind the shim without changing behavior.",
                f"Playbook hint: {playbook}",
            ], "All call sites route through the shim; suite green; no behavior diff in golden tests.",
             "Delete the shim; callers return to direct calls.", round(base_days * 0.25, 1), False),
            MigrationPhase(3, "Dual-run", [
                "Run old and new implementations side by side (dual-write / shadow-read as applicable).",
                "Diff outputs continuously; log every divergence with inputs.",
                "Route canary traffic (1% -> 10% -> 50%) to the new path.",
            ], "Divergence rate < 0.1% over 2 weeks AND zero SEV1/SEV2 attributable to the new path.",
             "Flip traffic back to 100% old path; shim remains until cleanup.", round(base_days * 0.35, 1), True),
            MigrationPhase(4, "Cut over & cleanup", [
                "Switch to the new implementation as source of truth.",
                "Remove the old path and the shim after a 2-week soak.",
                "Update docs, runbooks, and dashboards; retire old alarms.",
            ], "Two consecutive weeks green on the new path; rollback rehearsal executed once.",
             "Old path is only deleted after the soak — until then, flip back is trivial.",
             round(base_days * 0.25, 1), True),
        ]

        irreversibility = [
            "Phase 3 -> 4 boundary: once the old path is deleted, rollback = redeploy old build + data backfill.",
            "Schema migrations: destructive DDL needs a backup snapshot + tested restore before execution.",
        ]
        if db_hits and not test_hits:
            irreversibility.insert(0, "WARNING: DB-heavy surface with no test signals — add contract tests before Phase 2.")

        total = round(sum(p.effort_days for p in phases), 1)
        risk = "HIGH" if (db_hits + api_hits) > 10 and test_hits < 3 else \
               "MEDIUM" if db_hits else "LOW"
        verdict = f"MIGRATION_VIABLE | risk {risk} | ~{total} engineer-days | strangler-fig, 4 phases"
        return MigrationPlan(from_tech=from_tech, to_tech=to_tech, surface_inventory=surface,
                             phases=phases, total_effort_days=total,
                             irreversibility_points=irreversibility, verdict=verdict)

    @staticmethod
    def format_plan(p: MigrationPlan) -> str:
        out = ["=" * 62, "MIGRATION PLANNER AGENT — CAMPAIGN PLAN", "=" * 62,
               f"{p.from_tech}  ->  {p.to_tech}", p.verdict, "-" * 62,
               "Surface inventory: " + ", ".join(f"{k}={v}" for k, v in p.surface_inventory.items()),
               "-" * 62]
        for ph in p.phases:
            out.append(f"Phase {ph.number}: {ph.name} (~{ph.effort_days}d)"
                       + ("  [HITL gate]" if ph.requires_hitl else ""))
            out += [f"   - {s}" for s in ph.steps]
            out.append(f"   risk gate: {ph.risk_gate}")
            out.append(f"   rollback : {ph.rollback}")
        out += ["-" * 62, "Irreversibility points:"]
        out += [f"  ! {i}" for i in p.irreversibility_points]
        out += ["=" * 62]
        return "\n".join(out)
