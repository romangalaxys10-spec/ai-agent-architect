"""
Refactor Pilot Engine.
Detects code smells (duplication, long functions, god classes, magic numbers,
deep nesting, long parameter lists) and emits a risk-gated refactoring flight plan.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class Smell:
    kind: str
    location: str
    severity: str
    detail: str
    risk: float

@dataclass
class RefactorStep:
    order: int
    name: str
    action: str
    guard: str
    effort_hours: float

@dataclass
class RefactorPlan:
    smells: List[Smell] = field(default_factory=list)
    steps: List[RefactorStep] = field(default_factory=list)
    maintainability_before: int = 0
    maintainability_after: int = 0
    total_effort_hours: float = 0.0
    verdict: str = ""

AGGRESSIVENESS = {
    1: {"max_func": 120, "max_params": 6, "min_dup_lines": 6, "cap_steps": 3},
    2: {"max_func": 70, "max_params": 5, "min_dup_lines": 4, "cap_steps": 6},
    3: {"max_func": 40, "max_params": 4, "min_dup_lines": 3, "cap_steps": 10},
}

class RefactorPilotEngine:
    """Behavior-preserving refactors only — every step ships with its safety guard."""

    @classmethod
    def plan(cls, source: str, aggressiveness: int = 2) -> RefactorPlan:
        cfg = AGGRESSIVENESS[aggressiveness]
        lines = source.splitlines()
        smells: List[Smell] = []

        # --- long functions
        func_re = re.compile(r"^\s*def\s+(\w+)\s*\(")
        starts = [(i + 1, m.group(1)) for i, m in enumerate(func_re.finditer("\n".join(lines)))
                  for _ in [None]]
        boundaries = []
        for idx, line in enumerate(lines):
            m = func_re.match(line)
            if m:
                boundaries.append((idx, m.group(1)))
        for j, (start_idx, name) in enumerate(boundaries):
            end_idx = boundaries[j + 1][0] - 1 if j + 1 < len(boundaries) else len(lines) - 1
            length = end_idx - start_idx + 1
            if length > cfg["max_func"]:
                smells.append(Smell("long_function", f"{name} (L{start_idx+1}-{end_idx+1})",
                                    "major", f"{length} lines > {cfg['max_func']}", risk=0.5))

        # --- long parameter lists
        for idx, line in enumerate(lines):
            m = re.match(r"\s*def\s+\w+\((.*)\)", line)
            if m:
                n_params = len([p for p in m.group(1).split(",") if p.strip()])
                if n_params > cfg["max_params"]:
                    smells.append(Smell("long_param_list", f"L{idx+1}", "minor",
                                        f"{n_params} parameters > {cfg['max_params']}", risk=0.3))

        # --- magic numbers
        magics = []
        for idx, line in enumerate(lines):
            if line.strip().startswith("#"):
                continue
            for m in re.finditer(r"(?<![\w.\"\'])(\d{3,})(?![\w.])", line):
                if m.group(1) not in ("200", "201", "404", "500"):
                    magics.append((idx + 1, m.group(1)))
        if len(magics) >= 3:
            smells.append(Smell("magic_numbers", f"{len(magics)} sites", "minor",
                                f"e.g. L{magics[0][0]}={magics[0][1]}", risk=0.15))

        # --- duplication via normalized line buckets
        norm = {}
        for idx, line in enumerate(lines):
            s = re.sub(r"\s+", " ", line.strip())
            if len(s) > 25 and not s.startswith(("#", '"""', "'''")):
                norm.setdefault(s, []).append(idx + 1)
        dups = [(s, locs) for s, locs in norm.items() if len(locs) >= 2]
        if len(dups) >= cfg["min_dup_lines"]:
            smells.append(Smell("duplication", f"{len(dups)} repeated line shapes", "major",
                                f"e.g. L{dups[0][1][0]} and L{dups[0][1][1]}", risk=0.4))

        # --- god class
        class_methods = {}
        current_class = None
        for idx, line in enumerate(lines):
            cm = re.match(r"^class\s+(\w+)", line)
            if cm:
                current_class = cm.group(1)
                class_methods[current_class] = 0
            mm = re.match(r"\s+def\s+\w+", line)
            if mm and current_class:
                class_methods[current_class] += 1
        for cname, cnt in class_methods.items():
            if cnt > 12:
                smells.append(Smell("god_class", cname, "major", f"{cnt} methods", risk=0.6))

        # --- deep nesting
        for idx, line in enumerate(lines):
            indent = len(line) - len(line.lstrip())
            if indent >= 12 and line.strip():
                smells.append(Smell("deep_nesting", f"L{idx+1}", "minor",
                                    f"indent {indent} spaces", risk=0.35))
                break

        sev_weight = {"major": 12, "minor": 5}
        penalty = sum(sev_weight[s.severity] for s in smells)
        m_before = max(20, 95 - penalty)
        m_after = min(96, m_before + min(penalty, 45))
        if m_before >= 80:
            m_after = min(97, m_before + max(2, penalty // 3))

        smell_steps = {
            "duplication": ("Extract helper", "Extract repeated line clusters into named helpers; parameters for the deltas.",
                            "Golden-output test on both duplicated sites before extraction", 2.0),
            "long_function": ("Decompose function", "Split into single-responsibility helpers named after intent.",
                              "Characterization tests on current outputs first", 3.0),
            "god_class": ("Split class", "Group methods by field usage; split along those seams.",
                          "Cover public API with contract tests; keep facade during move", 8.0),
            "long_param_list": ("Introduce parameter object", "Bundle cohesive params into a dataclass with defaults.",
                                "Backward-compatible wrapper keeps old signature", 1.0),
            "magic_numbers": ("Name constants", "Promote magic numbers to module-level named constants.",
                              "Pure rename; diff-review only", 0.5),
            "deep_nesting": ("Guard clauses + extraction", "Invert conditions for early returns; extract inner block.",
                             "Branch-coverage tests on the nested predicate", 1.5),
        }
        steps: List[RefactorStep] = []
        order = 0
        for smell in sorted(smells, key=lambda s: -sev_weight[s.severity]):
            if smell.kind not in smell_steps:
                continue
            name, action, guard, effort = smell_steps[smell.kind]
            order += 1
            steps.append(RefactorStep(order, name, action, guard, effort))
            if order >= cfg["cap_steps"]:
                break
        if not steps and smells:
            steps.append(RefactorStep(1, "Triage smells", "Run with --aggressiveness 3 for deeper extraction steps.",
                                      "None (analysis only)", 0.5))

        total_effort = round(sum(s.effort_hours for s in steps), 1)
        verdict = ("REFACTOR_NOW" if penalty >= 30 else
                   "REFACTOR_INCREMENTALLY" if smells else "SHAPE_OK")
        return RefactorPlan(smells=smells, steps=steps, maintainability_before=m_before,
                            maintainability_after=m_after, total_effort_hours=total_effort,
                            verdict=verdict)

    @staticmethod
    def format_plan(p: RefactorPlan) -> str:
        out = ["=" * 62, "REFACTOR PILOT AGENT — FLIGHT PLAN", "=" * 62,
               f"Maintainability: {p.maintainability_before}/100 -> {p.maintainability_after}/100 (projected)",
               f"Smells detected: {len(p.smells)} | effort: {p.total_effort_hours}h | {p.verdict}",
               "-" * 62, "Smell inventory:"]
        if p.smells:
            for s in p.smells:
                out.append(f"  [{s.severity}] {s.kind:16} {s.location:28} {s.detail}")
        else:
            out.append("  none")
        out += ["-" * 62, "Flight plan (each step guarded):"]
        for st in p.steps:
            out.append(f"  {st.order}. {st.name} (~{st.effort_hours}h)")
            out.append(f"      action: {st.action}")
            out.append(f"      guard : {st.guard}")
        out += ["-" * 62,
                "Rule: one step per commit; full suite green before the next step starts.",
                "=" * 62]
        return "\n".join(out)
