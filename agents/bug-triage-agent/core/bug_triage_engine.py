"""
Bug Triage Engine.
Classifies bug reports, builds reproduction checklists, and ranks root-cause
hypotheses by prior probability with disconfirming tests.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class TriageReport:
    defect_class: str
    severity: str
    priority: str
    repro_confidence: float
    checklist: List[str] = field(default_factory=list)
    hypotheses: List[dict] = field(default_factory=list)
    questions_for_reporter: List[str] = field(default_factory=list)
    verdict: str = ""

SEVERITY_MATRIX = {
    ("crash", "all_users"): ("SEV1", "P0"),
    ("crash", "some_users"): ("SEV2", "P1"),
    ("data_corruption", "all_users"): ("SEV1", "P0"),
    ("data_corruption", "some_users"): ("SEV1", "P0"),
    ("security", "any"): ("SEV1", "P0"),
    ("perf", "all_users"): ("SEV2", "P1"),
    ("ui", "some_users"): ("SEV3", "P2"),
}

CLASS_SIGNALS = {
    "crash": ["traceback", "exception", "segfault", "panic", "crash", "killed", "core dump", "500"],
    "data_corruption": ["wrong data", "data loss", "missing record", "corrupt", "overwritten", "duplicate charge", "off by"],
    "security": ["auth", "permission", "unauthorized", "leak", "token", "xss", "injection", "spoof"],
    "perf": ["slow", "timeout", "latency", "hangs", "freezes", "memory", "cpu", "o(n"],
    "ui": ["button", "css", "layout", "misaligned", "modal", "renders", "scroll", "font"],
}

HYPOTHESIS_PRIORS = [
    (r"after (deploy|release|upgrade|migration)", "regression-in-new-code", 0.45,
     "Bisect between last known-good and current release; run the diff's touched tests."),
    (r"(null|none|undefined|nan)", "null-handling-gap", 0.35,
     "Add precondition asserts at the boundary that produces the value."),
    (r"(race|concurrent|parallel|thread|async)", "concurrency-race", 0.40,
     "Reproduce under deterministic scheduling (fake clocks / single-thread lockstep)."),
    (r"(cache|stale|old version|cdn)", "stale-cache-or-version-skew", 0.35,
     "Bypass cache; force version pin; compare payloads directly."),
    (r"(encoding|utf|unicode|emoji|charset)", "encoding-mismatch", 0.30,
     "Replay bytes as-is; assert content-type and explicit codecs at both ends."),
    (r"(large|huge|many|million|bulk)", "scale-edge-case", 0.30,
     "Bisect input size to find the cliff; profile at 0.5x and 2x of it."),
    (r"(sometimes|intermittent|randomly|flaky)", "nondeterminism-ordering", 0.35,
     "Seed every RNG; sort collections; log iteration order to diff runs."),
    (r"(permission|denied|403|forbidden)", "authz-config-drift", 0.30,
     "Compare effective vs intended policy; test with a freshly provisioned principal."),
]

class BugTriageEngine:
    """Evidence-first triage: never guesses without naming the disconfirming test."""

    @classmethod
    def triage(cls, text: str) -> TriageReport:
        low = text.lower()

        scores = {c: sum(1 for kw in kws if kw in low) for c, kws in CLASS_SIGNALS.items()}
        defect_class = max(scores, key=lambda k: scores[k]) if max(scores.values()) > 0 else "unclear"

        all_users = any(w in low for w in ("all users", "everyone", "all customers", "100% of"))
        security = scores.get("security", 0) > 0
        if security:
            sev, pri = "SEV1", "P0"
        else:
            sev, pri = SEVERITY_MATRIX.get((defect_class, "all_users" if all_users else "some_users"),
                                           ("SEV3", "P2"))

        has_steps = bool(re.search(r"(step\s*\d|1\.)", low))
        has_expected = "expected" in low
        has_actual = "actual" in low or "instead" in low
        has_env = bool(re.search(r"(version|v\d|os |browser|python \d|node \d|ubuntu|macos|windows)", low))
        repro_confidence = round(
            0.2 * has_steps + 0.25 * has_expected + 0.25 * has_actual + 0.15 * has_env
            + (0.15 if re.search(r"(always|every time|100%)", low) else 0.0), 2)

        hypotheses = []
        for pattern, name, prior, disproof in HYPOTHESIS_PRIORS:
            m = re.search(pattern, low)
            if m:
                hypotheses.append({"hypothesis": name, "probability": prior,
                                   "trigger": m.group(0), "disconfirming_test": disproof})
        hypotheses.sort(key=lambda h: -h["probability"])
        if not hypotheses:
            hypotheses.append({"hypothesis": "insufficient-evidence", "probability": 0.5,
                               "trigger": "-", "disconfirming_test":
                               "Collect env, steps, expected/actual, and first failing version."})

        checklist = [
            "Re-read report; quote the exact error/output verbatim.",
            "Reproduce in a clean environment matching the reported stack.",
            "Record: first-seen version, affected %, error rate graphs around the timestamp.",
            "Capture full logs + minimal failing input; attach both to the ticket.",
        ]
        if defect_class == "data_corruption":
            checklist.append("Freeze and back up the affected dataset before any repair attempt.")
        if security:
            checklist.append("Engage security on-call; preserve evidence; do NOT test live payloads.")

        questions = []
        if not has_env:
            questions.append("What is the exact version/OS/browser where this occurs?")
        if not has_steps:
            questions.append("What are the minimal steps to reproduce?")
        if not has_expected:
            questions.append("What did you expect to happen instead?")
        if not re.search(r"(always|sometimes|once|intermittent)", low):
            questions.append("Does it happen every time or intermittently?")

        verdict = f"{defect_class.upper()} | {sev}/{pri} | repro-confidence {repro_confidence:.0%}"
        return TriageReport(defect_class=defect_class, severity=sev, priority=pri,
                            repro_confidence=repro_confidence, checklist=checklist,
                            hypotheses=hypotheses, questions_for_reporter=questions,
                            verdict=verdict)

    @staticmethod
    def format_report(r: TriageReport) -> str:
        out = ["=" * 62, "BUG TRIAGE AGENT — REPORT", "=" * 62, r.verdict, "-" * 62,
               "Reproduction checklist:"]
        out += [f"  {i}. {c}" for i, c in enumerate(r.checklist, 1)]
        out += ["-" * 62, "Root-cause hypotheses (ranked):"]
        for h in r.hypotheses:
            out.append(f"  {h['probability']:.0%}  {h['hypothesis']}  (trigger: {h['trigger']})")
            out.append(f"        disprove via: {h['disconfirming_test']}")
        if r.questions_for_reporter:
            out += ["-" * 62, "Questions for reporter (missing evidence):"]
            out += [f"  ? {q}" for q in r.questions_for_reporter]
        out.append("=" * 62)
        return "\n".join(out)
