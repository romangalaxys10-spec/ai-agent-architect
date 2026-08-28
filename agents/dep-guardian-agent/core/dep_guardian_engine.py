"""
Dependency Guardian Engine.
Audits requirements manifests for risk (floating pins, EOL majors, risky
version pins) and produces a safe upgrade order with lockfile advice.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class DepRisk:
    name: str
    version: str
    spec: str
    risks: List[str] = field(default_factory=list)
    risk_score: float = 0.0
    action: str = ""

@dataclass
class DepAudit:
    total: int
    pinned: int
    floating: int
    deps: List[DepRisk] = field(default_factory=list)
    upgrade_order: List[str] = field(default_factory=list)
    lockfile_advice: List[str] = field(default_factory=list)
    verdict: str = ""

# majors that shipped famous breaking changes / EOL cycles (heuristic knowledge)
EOL_KNOWLEDGE = {
    ("django", "2"): "Django 2.x is EOL; upgrade through 3.2 -> 4.2 LTS first.",
    ("django", "3"): "Django 3.x is EOL; target 4.2 LTS.",
    ("python", "3.7"): "Python 3.7 is EOL since mid-2023.",
    ("python", "3.8"): "Python 3.8 is EOL since late 2024.",
    ("requests", "2.25"): "requests <2.31 has CVE-2023-32681 (Proxy-Authorization leak).",
    ("urllib3", "1."): "urllib3 1.x has redirect/CVE history; move to 2.x.",
    ("pillow", "8"): "Pillow <10 has multiple CVEs (e.g. CVE-2023-44271).",
    ("cryptography", "3"): "cryptography <42 has OpenSSL linkage advisories.",
    ("pyyaml", "5"): "PyYAML <5.4 / unsafe load has RCE CVE-2020-14343 family.",
    ("log4j", "2.13"): "log4j <2.15 is Log4Shell (CVE-2021-44228) — critical.",
    ("lodash", "4.16"): "old lodash has prototype-pollution CVEs.",
    ("openssl", "1.0"): "OpenSSL 1.0.x is EOL.",
}

RISKY_NAMES = {
    "pickle": "stdlib pickle is not a dep — if listed, something is wrong.",
}

class DepGuardianEngine:
    """Supply-chain discipline: every pin is a promise; every float is a bet."""

    @classmethod
    def audit(cls, manifest_text: str) -> DepAudit:
        deps: List[DepRisk] = []
        for raw in manifest_text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                line = line.lstrip("-").strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r"([A-Za-z0-9_.\-]+)\s*([=<>!~^]{0,2})\s*([0-9A-Za-z.*!\-+]*)", line)
            if not m:
                continue
            name, op, ver = m.group(1), m.group(2), m.group(3)
            risks, score = [], 0.0

            if op in ("", "==", "") and not ver:
                risks.append("fully floating: any future release can enter the build")
                score += 3.0
            if op in (">=", "~=", "^", ">", "<"):
                risks.append(f"range pin ({op}{ver}): resolves differently over time")
                score += 1.5
            if op == "==" and ver:
                risks.append("exact pin: security patches require manual bump")
                score += 0.5
            low = name.lower()
            for (key, prefix), msg in EOL_KNOWLEDGE.items():
                if low == key and ver.startswith(prefix):
                    risks.append(msg)
                    score += 4.0
            if ver == "0." or ver.startswith("0."):
                risks.append("0.x: breaking changes allowed at any time")
                score += 1.0
            if any(c.isalpha() and c not in "abcdef" for c in ver) and ver:
                pass  # alpha tags like 1.0b2 handled below
            if re.search(r"(a|b|rc|dev)\d?$", ver):
                risks.append("pre-release pin in production manifest")
                score += 2.0
            if low in RISKY_NAMES:
                risks.append(RISKY_NAMES[low]); score += 2.0

            if not risks:
                action = "keep"
                score = 0.2
            elif score >= 3.5:
                action = "upgrade-priority"
            elif score >= 1.5:
                action = "upgrade-soon"
            else:
                action = "monitor"
            deps.append(DepRisk(name, ver or "*", op or "none", risks, score, action))

        deps_sorted = sorted(deps, key=lambda d: -d.risk_score)
        upgrade_order = [f"{d.name} ({d.version}) -> {d.action}" for d in deps_sorted
                         if d.action in ("upgrade-priority", "upgrade-soon")][:8]
        pinned = sum(1 for d in deps if d.spec == "==")
        floating = sum(1 for d in deps if d.spec in ("", "none", ">=", "~=", "^", ">", "<"))

        lockfile = [
            "Commit a lockfile (requirements.txt --hash or pip-tools compile) for reproducible builds.",
            "Enable automated dependency PRs (Renovate/Dependabot) with a CI green requirement.",
            "Add `pip-audit` / `npm audit --audit-level=high` as a required CI stage.",
        ]
        if any(d.risk_score >= 4 for d in deps):
            lockfile.insert(0, "URGENT: known-vulnerable/EOL pins present — patch before any feature work.")

        worst = deps_sorted[0].risk_score if deps_sorted else 0
        verdict = ("SUPPLY_CHAIN_RISK" if worst >= 3.5
                   else "NEEDS_PINNING" if floating > len(deps) / 2 and deps
                   else "HEALTHY")
        return DepAudit(total=len(deps), pinned=pinned, floating=floating, deps=deps_sorted,
                        upgrade_order=upgrade_order, lockfile_advice=lockfile, verdict=verdict)

    @staticmethod
    def format_audit(a: DepAudit) -> str:
        out = ["=" * 62, "DEPENDENCY GUARDIAN AGENT — AUDIT", "=" * 62,
               f"Deps: {a.total} | pinned: {a.pinned} | floating/ranged: {a.floating} | {a.verdict}",
               "-" * 62, "Risk-ranked dependencies:"]
        if a.deps:
            for d in a.deps[:15]:
                out.append(f"  {d.risk_score:4.1f}  {d.name:24} {d.spec}{d.version:12} [{d.action}]")
                for r in d.risks:
                    out.append(f"        - {r}")
        else:
            out.append("  (empty manifest)")
        if a.upgrade_order:
            out += ["-" * 62, "Upgrade order (highest risk first):"]
            out += [f"  {i}. {u}" for i, u in enumerate(a.upgrade_order, 1)]
        out += ["-" * 62, "Lockfile & CI advice:"]
        out += [f"  * {l}" for l in a.lockfile_advice]
        out.append("=" * 62)
        return "\n".join(out)
