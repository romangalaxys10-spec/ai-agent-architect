"""
CI Surgeon Engine.
Parses CI failure logs, isolates the failure class and blame domain,
and prescribes the highest-probability fix playbook.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class Diagnosis:
    failure_class: str
    blame_domain: str
    flaky_verdict: str
    playbooks: List[dict] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    verdict: str = ""

SIGNATURES = [
    (r"AssertionError|assert\s+\w+\s*==|Expected:|but was:", "assertion_failure", "code",
     "Re-run test locally on the exact commit; read the diff of the last 24h for the asserted value's producer."),
    (r"TimeoutExpired|timed?\s*out|Timeout after", "timeout", "infra_or_code",
     "Check whether the test sleeps on network; add fake clock; then check runner CPU starvation."),
    (r"(ModuleNotFoundError|ImportError|No module named)", "import_error", "environment",
     "Pin the missing package in requirements/lockfile; verify CI uses the same env file as local."),
    (r"(Killed|OOM|out of memory|exit code 137)", "oom", "infra",
     "Reduce test parallelism or dataset size; move the heavy test to a beefier runner lane."),
    (r"(Segmentation fault|exit code 139|SIGSEGV)", "segfault", "native_dep",
     "Reproduce with debug symbols; check native extension versions; isolate with faulthandler."),
    (r"(Connection|DNS|ECONNREFUSED|ENOTFOUND|network|502|503)", "network", "infra",
     "Add retry-with-jitter; mark external service dependency; re-run to confirm transient."),
    (r"(Permission denied|EACCES|403)", "permission", "environment",
     "Check runner user + secret mounting; validate the token scope in CI settings."),
    (r"(SyntaxError|IndentationError)", "syntax_error", "code",
     "Fix the syntax error directly; run `python -m py_compile` as a pre-commit gate."),
    (r"(flake|flaky|retry|passed on retry|PASSED on attempt 2)", "flaky_marker", "flaky",
     "Quarantine the test; measure flake rate over 100 runs; fix ordering/shared-state root cause."),
]

FLAKE_WORDS = ("intermittent", "flaky", "sometimes fails", "passed on retry", "re-run passed")
NETWORK_CLASSES = {"network", "timeout"}

class CISurgeonEngine:
    """Surgical triage: class first, blame second, fix playbook third."""

    @classmethod
    def diagnose(cls, log_text: str) -> Diagnosis:
        matched, evidence = [], []
        for pattern, fclass, blame, playbook in SIGNATURES:
            hits = re.findall(pattern, log_text, re.I)
            if hits:
                matched.append((fclass, blame, playbook, len(hits)))
                for m in re.finditer(pattern, log_text, re.I):
                    start = max(0, m.start() - 40)
                    evidence.append(log_text[start:m.end() + 40].replace("\n", " ").strip()[:120])

        if not matched:
            matched = [("unknown_failure", "code",
                        "Read the first error frame in the log; the classifier found no known signature.",
                        1)]

        matched.sort(key=lambda t: -t[3])
        primary_class = matched[0][0]
        domains = {m[1] for m in matched}
        blame_domain = "+".join(sorted(domains))

        flaky_signals = sum(1 for w in FLAKE_WORDS if w in log_text.lower())
        rerun_pass = bool(re.search(r"(PASSED|SUCCESS).{0,40}(attempt 2|retry|re-run)", log_text, re.I))
        flaky_verdict = (
            "LIKELY_FLAKY" if (flaky_signals >= 1 and primary_class != "syntax_error") or rerun_pass
            else "DETERMINISTIC_FAILURE"
        )
        if primary_class in NETWORK_CLASSES and flaky_signals:
            flaky_verdict = "LIKELY_TRANSIENT_INFRA"

        playbooks = [
            {"step": i + 1, "action": pb, "expected_fix_probability": round(min(0.9, 0.55 + 0.08 * hits), 2)}
            for i, (_, _, pb, hits) in enumerate(matched[:4])
        ]

        verdict = f"{primary_class.upper()} | blame: {blame_domain} | {flaky_verdict}"
        return Diagnosis(failure_class=primary_class, blame_domain=blame_domain,
                         flaky_verdict=flaky_verdict, playbooks=playbooks,
                         evidence=evidence[:6], verdict=verdict)

    @staticmethod
    def format_diagnosis(d: Diagnosis) -> str:
        out = ["=" * 62, "CI SURGEON AGENT — DIAGNOSIS", "=" * 62, d.verdict, "-" * 62,
               "Log evidence (matched signatures):"]
        out += [f"  > {e}" for e in d.evidence] or ["  (no direct signature matched)"]
        out += ["-" * 62, "Fix playbook (ordered by fix probability):"]
        for p in d.playbooks:
            out.append(f"  step {p['step']} [{p['expected_fix_probability']:.0%}]: {p['action']}")
        out += ["-" * 62,
                "Next: apply step 1, push, and require two consecutive green runs before unblocking the team.",
                "=" * 62]
        return "\n".join(out)
