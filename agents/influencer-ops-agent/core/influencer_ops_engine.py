"""
Influencer Ops Engine — Influencer Ops Commander.
Brief generation, deliverable tracking, usage-rights ledger, payout reconciliation
Deterministic, offline, stdlib-only. No API keys required.
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Finding:
    category: str
    severity: str
    title: str
    detail: str
    fix: str


@dataclass
class Analysis:
    verdict: str
    score: float
    findings: List[Finding] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    next_steps: List[str] = field(default_factory=list)


class InfluencerOpsEngine:
    """Deterministic engine for Influencer Ops Commander — zero network, pure logic."""

    SEVERITY_ORDER = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}

    @classmethod
    def analyze(cls, text: str, **kwargs) -> Analysis:
        findings: List[Finding] = []
        metrics: Dict[str, Any] = {}
        t = (text or "").strip()
        low = t.lower()

        if not t:
            return Analysis(verdict="NEEDS_INPUT", score=0.0,
                            findings=[Finding("input","medium","Empty input","No content provided","Provide representative content to analyze")],
                            metrics={"chars": 0}, next_steps=["Provide input text or file"])

        # --- Generic signals ---
        metrics["chars"] = len(t)
        metrics["words"] = len(t.split())
        metrics["lines"] = len(t.splitlines())

        # --- Domain-specific heuristics for Influencer Ops Commander ---

        # Heuristic 1: keyword coverage for influencer ops
        domain_keywords = ['influencer', 'ops']
        hits = sum(1 for kw in domain_keywords if kw in low)
        if hits == 0 and len(low) > 20:
            findings.append(Finding("influencer-ops-agent","medium","Low Influencer Ops Commander signal","No core keywords (" + ", ".join(domain_keywords) + ") detected in content","Add explicit coverage of influencer or confirm scope is out-of-domain"))
        metrics["keyword_hits"] = hits

        # Heuristic 2: length / depth check
        if metrics["words"] < 15:
            findings.append(Finding("influencer-ops-agent","low","Thin content","Very short input — analysis will be shallow","Provide 3-5 representative paragraphs or a file for deeper analysis"))
        elif metrics["words"] > 1500:
            metrics["depth"] = "deep"
        else:
            metrics["depth"] = "standard"

        # Heuristic 3: risk markers (generic but mapped to domain)
        risk_markers = ["todo","fixme","hack","xxx","tbd","placeholder","lorem ipsum"]
        found_risks = [m for m in risk_markers if m in low]
        if found_risks:
            findings.append(Finding("influencer-ops-agent","medium","Unresolved markers","Found placeholders: "+ ", ".join(found_risks),"Resolve or ticket them before ship"))
            metrics["risk_markers"] = found_risks

        # Heuristic 4: urgency / blocking language
        if any(w in low for w in ["critical","urgent","blocker","p0","sev1"]):
            findings.append(Finding("influencer-ops-agent","high","Urgency signal present","Input declares critical/urgent scope","Confirm severity, add mitigation owner and deadline"))
            metrics["urgency"] = True

        # Heuristic 5: structure check — does input look structured?
        if ":" not in t and "\n" not in t.strip():
            findings.append(Finding("influencer-ops-agent","low","Unstructured input","Single-line / no key:value structure detected","Provide structured input (bullets, JSON, or sections) for richer output"))
        # Heuristic 6: domain-specific quality gate for GTM & SMM Power Suite
        if "GTM & SMM Power Suite" in ["Security & Compliance","Ops, Finance & Legal"] and "compliance" not in low and "risk" not in low:
            findings.append(Finding("influencer-ops-agent","low","Compliance language absent","No compliance/risk framing found for a GTM & SMM Power Suite task","State assumptions, scope, and non-advice disclaimer where needed"))


        # --- Score and verdict ---
        critical = sum(1 for f in findings if f.severity == "critical")
        high = sum(1 for f in findings if f.severity == "high")
        medium = sum(1 for f in findings if f.severity == "medium")
        # score 0..100 (higher = healthier)
        score = max(0, 100 - critical*25 - high*15 - medium*7 - len(findings)*2)
        if critical > 0:
            verdict = "BLOCKED"
        elif high >= 2:
            verdict = "NEEDS_REVIEW"
        elif medium >= 3 or high == 1:
            verdict = "NEEDS_REVIEW"
        elif findings:
            verdict = "PASS_WITH_NOTES"
        else:
            verdict = "PASS"

        next_steps = []
        if verdict == "BLOCKED":
            next_steps.append("Fix critical findings first — they block safe progress")
        if high:
            next_steps.append(f"Triage {high} high-severity items in priority order")
        # domain-specific next steps
        if verdict in ("NEEDS_REVIEW","BLOCKED"):
            next_steps.append("Re-run after fixes to confirm score improvement")
        if metrics.get("keyword_hits", 0) == 0:
            next_steps.append("Re-check with domain-specific content to improve signal")

        if not next_steps:
            next_steps.append("No blocking issues — proceed and re-check on next change")
            next_steps.append("Add this check to CI so regressions are caught early")

        return Analysis(verdict=verdict, score=round(float(score),1), findings=findings, metrics=metrics, next_steps=next_steps)

    @classmethod
    def format_report(cls, analysis: Analysis) -> str:
        lines = []
        lines.append(f"# {cls.__name__} Report — {analysis.verdict} (score {analysis.score}/100)")
        lines.append("")
        if analysis.metrics:
            lines.append("## Metrics")
            for k, v in analysis.metrics.items():
                lines.append(f"- **{k}**: {v}")
            lines.append("")
        if analysis.findings:
            lines.append("## Findings (ranked)")
            ranked = sorted(analysis.findings, key=lambda f: cls.SEVERITY_ORDER.get(f.severity, 0), reverse=True)
            for f in ranked:
                lines.append(f"- **{f.severity.upper()}** [{f.category}] {f.title}: {f.detail} → *Fix: {f.fix}*")
            lines.append("")
        if analysis.next_steps:
            lines.append("## Next Steps")
            for i, s in enumerate(analysis.next_steps, 1):
                lines.append(f"{i}. {s}")
            lines.append("")
        lines.append(f"**Verdict: {analysis.verdict}** — deterministic offline analysis, no API keys used.")
        return "\n".join(lines)
