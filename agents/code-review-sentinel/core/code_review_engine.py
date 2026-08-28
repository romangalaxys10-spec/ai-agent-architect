"""
Code Review Sentinel Engine.
Deterministic static review of Python source with severity-ranked findings,
CWE mapping, and a risk-to-effort ordered remediation plan.
Fully offline: pure stdlib, no AST exec, safe on untrusted input.
"""

import re
from dataclasses import dataclass, field
from typing import List

SEVERITY_ORDER = {"info": 0, "minor": 1, "major": 2, "blocker": 3}


@dataclass
class Finding:
    rule: str
    line: int
    severity: str
    cwe: str
    message: str
    remediation: str


@dataclass
class ReviewReport:
    lines_total: int
    functions: int
    classes: int
    max_line_length: int
    findings: List[Finding] = field(default_factory=list)
    verdict: str = "PASS"
    fix_order: List[str] = field(default_factory=list)

    @property
    def counts(self) -> dict:
        out = {"info": 0, "minor": 0, "major": 0, "blocker": 0}
        for f in self.findings:
            out[f.severity] += 1
        return out


RULES = [
    dict(rule="mutable-default-arg", pattern=r"def\s+\w+\([^)]*=\s*(\[\]|\{\}|set\(\))", severity="major",
         cwe="CWE-462", message="Mutable default argument shared across calls",
         remediation="Default to None and create the container inside the function body."),
    dict(rule="bare-except", pattern=r"^\s*except\s*:", severity="major",
         cwe="CWE-396", message="Bare except swallows KeyboardInterrupt/SystemExit",
         remediation="Catch the narrowest exception type and log it."),
    dict(rule="eval-use", pattern=r"\beval\s*\(", severity="blocker",
         cwe="CWE-95", message="eval() executes arbitrary code",
         remediation="Replace with ast.literal_eval or explicit parsing."),
    dict(rule="exec-use", pattern=r"\bexec\s*\(", severity="blocker",
         cwe="CWE-95", message="exec() executes arbitrary code",
         remediation="Remove; drive behavior with data, not code strings."),
    dict(rule="pickle-load", pattern=r"pickle\.loads?\s*\(", severity="blocker",
         cwe="CWE-502", message="Deserializing untrusted pickle enables RCE",
         remediation="Use JSON or a schema-validated format."),
    dict(rule="sql-concat", pattern=r"(execute|executemany)\s*\(\s*[f'\"]?\s*(SELECT|INSERT|UPDATE|DELETE).*?(\+\s*\w|%s\)|%\s*\w|\{)", severity="blocker",
         cwe="CWE-89", message="SQL built via string concatenation/format",
         remediation="Use parameterized queries: cursor.execute(sql, params)."),
    dict(rule="shell-true", pattern=r"(subprocess|os\.system|os\.popen|run\()[^)\n]*shell\s*=\s*True", severity="major",
         cwe="CWE-78", message="Shell injection surface (shell=True)",
         remediation="Pass an argv list with shell=False and validate inputs."),
    dict(rule="weak-hash", pattern=r"\b(md5|sha1)\s*\(", severity="major",
         cwe="CWE-327", message="Broken hash primitive used",
         remediation="Use hashlib.sha256 or better; salt passwords via bcrypt/scrypt."),
    dict(rule="insecure-random", pattern=r"\brandom\.\w+\(", severity="minor",
         cwe="CWE-338", message="Non-cryptographic RNG (fine for simulations, not tokens)",
         remediation="Use secrets.* for anything security-relevant."),
    dict(rule="eq-none", pattern=r"[=!]=\s*None\b", severity="minor",
         cwe="CWE-none", message="Identity comparison against None with ==",
         remediation="Use `is None` / `is not None`."),
    dict(rule="todo-comment", pattern=r"#\s*(TODO|FIXME|HACK|XXX)", severity="info",
         cwe="CWE-none", message="Unresolved work tracked only in a comment",
         remediation="Move to the issue tracker or resolve before merge."),
    dict(rule="print-stmt", pattern=r"^\s*print\s*\(", severity="minor",
         cwe="CWE-532", message="print() left in production path",
         remediation="Route through logging with levels."),
    dict(rule="hardcoded-secret", pattern=r"(?i)(api[_-]?key|secret|passwd|password|token)\s*[:=]\s*[\"'][^\"']{8,}", severity="blocker",
         cwe="CWE-798", message="Hardcoded credential literal",
         remediation="Load from environment/secret manager; rotate the leaked value."),
    dict(rule="tls-verify-off", pattern=r"verify\s*=\s*False", severity="blocker",
         cwe="CWE-295", message="TLS certificate verification disabled",
         remediation="Keep verify=True; pin a CA bundle if needed."),
]


def _cyclomatic_hint(line: str) -> bool:
    return bool(re.search(r"\b(if|elif|for|while|except|and|or|case)\b", line))


class CodeReviewSentinelEngine:
    """Zero-trust reviewer: assumes code is guilty until findings prove otherwise."""

    RISK_EFFORT = {"blocker": (5, 2), "major": (4, 2), "minor": (2, 1), "info": (1, 1)}

    @classmethod
    def review(cls, code: str, strict: bool = False) -> ReviewReport:
        lines = code.splitlines()
        findings: List[Finding] = []
        function_count = len(re.findall(r"^\s*def\s+\w+", code, re.M))
        class_count = len(re.findall(r"^\s*class\s+\w+", code, re.M))

        # per-line rules
        for idx, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("#") or not stripped:
                continue
            for rule in RULES:
                if re.search(rule["pattern"], line):
                    findings.append(Finding(
                        rule=rule["rule"], line=idx, severity=rule["severity"],
                        cwe=rule["cwe"], message=rule["message"],
                        remediation=rule["remediation"],
                    ))

        # structural rules: function length + nesting depth
        func_start = None
        depth_at_start = 0
        for idx, line in enumerate(lines, 1):
            indent = len(line) - len(line.lstrip())
            if re.match(r"\s*def\s+\w+", line):
                if func_start is not None:
                    cls._emit_long_function(findings, func_start, idx - 1, depth_at_start)
                func_start, depth_at_start = idx, indent
            if indent - depth_at_start >= 12:
                findings.append(Finding(
                    rule="deep-nesting", line=idx, severity="major", cwe="CWE-1123",
                    message=f"Nesting depth >= 4 levels (indent {indent})",
                    remediation="Extract inner branches into named helpers or early-return."))
        if func_start is not None:
            cls._emit_long_function(findings, func_start, len(lines), depth_at_start)

        # module-level smell: god file
        if len(lines) > 400:
            findings.append(Finding(
                rule="god-file", line=len(lines), severity="major", cwe="CWE-1124",
                message=f"File has {len(lines)} lines",
                remediation="Split along cohesive responsibilities."))

        if strict:
            for f in findings:
                if f.severity == "major":
                    f.severity = "blocker"

        counts = {"info": 0, "minor": 0, "major": 0, "blocker": 0}
        for f in findings:
            counts[f.severity] += 1

        verdict = (
            "NEEDS_CHANGES" if counts["blocker"] or counts["major"] > 3
            else "PASS_WITH_NITS" if counts["major"] or counts["minor"] > 8
            else "PASS"
        )

        fix_order = sorted(
            {(f.rule, f.severity) for f in findings},
            key=lambda pair: -cls.RISK_EFFORT[pair[1]][0] / cls.RISK_EFFORT[pair[1]][1],
        )[:8]
        fix_order = [f"{rule} [{sev}]" for rule, sev in fix_order]

        return ReviewReport(
            lines_total=len(lines), functions=function_count, classes=class_count,
            max_line_length=max((len(l) for l in lines), default=0),
            findings=findings, verdict=verdict, fix_order=fix_order,
        )

    @staticmethod
    def _emit_long_function(findings, start, end, depth):
        length = end - start + 1
        if length > 60:
            findings.append(Finding(
                rule="long-function", line=start, severity="major", cwe="CWE-1125",
                message=f"Function spans {length} lines (lines {start}-{end})",
                remediation="Decompose into helpers with single responsibilities."))

    @staticmethod
    def format_report(report: ReviewReport) -> str:
        c = report.counts
        out = [
            "=" * 62,
            "CODE REVIEW SENTINEL — REPORT",
            "=" * 62,
            f"Lines: {report.lines_total} | functions: {report.functions} | classes: {report.classes}",
            f"Findings: {len(report.findings)} "
            f"(blocker={c['blocker']} major={c['major']} minor={c['minor']} info={c['info']})",
            "-" * 62,
        ]
        if report.findings:
            ranked = sorted(report.findings, key=lambda f: -SEVERITY_ORDER[f.severity])
            for f in ranked[:25]:
                out.append(f"[{f.severity.upper():7}] L{f.line:<4} {f.rule} ({f.cwe})")
                out.append(f"           {f.message}")
                out.append(f"           fix: {f.remediation}")
            if len(ranked) > 25:
                out.append(f"... and {len(ranked) - 25} more findings")
        else:
            out.append("No rule violations detected.")
        out.append("-" * 62)
        out.append(f"VERDICT: {report.verdict}")
        if report.fix_order:
            out.append("Fix order (risk/effort): " + " -> ".join(report.fix_order))
        out.append("=" * 62)
        return "\n".join(out)
