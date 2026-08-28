"""
Team Effectiveness Lab Engine — Team Effectiveness Lab.
Team health: trust, clarity, dynamics, and Lencioni-style friction mapping
Deterministic, offline, stdlib-only. No API keys. HR-grade guardrails (PII/bias/compliance).
"""

import re
import hashlib
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


class TeamEffectivenessEngine:
    """Deterministic engine for Team Effectiveness Lab — zero network, HR-grade logic."""

    SEVERITY_ORDER = {"info":0,"low":1,"medium":2,"high":3,"critical":4}

    @classmethod
    def analyze(cls, text: str, **kwargs) -> Analysis:
        findings: List[Finding] = []
        metrics: Dict[str, Any] = {}
        t=(text or "").strip()
        low=t.lower()

        if not t:
            return Analysis(verdict="NEEDS_INPUT", score=0.0,
                            findings=[Finding("input","medium","Empty input","No content provided","Provide text/file to analyze")],
                            metrics={"chars":0}, next_steps=["Provide input text or --file"])

        metrics["chars"]=len(t)
        metrics["words"]=len(t.split())
        metrics["lines"]=len(t.splitlines())

        # HR-specific signals
        hr_keywords = ["hr","hrbp","talent","learning","performance","skills","succession","dei","inclusion","wellbeing","engagement","coaching","onboarding","workforce","manager","leader","employee","culture","feedback","goal"]
        metrics["hr_signal_hits"]=sum(1 for k in hr_keywords if k in low)
        # PII heuristic (emails, ids)
        pii_hits = len(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", t))
        if pii_hits>0:
            metrics["pii_emails"]=pii_hits
        # bias language
        bias_terms = ["culture fit","young","energetic","digital native","rockstar","ninja","manpower","guys"]
        found_bias=[b for b in bias_terms if b in low]
        if found_bias:
            metrics["bias_flags"]=found_bias

        # Domain heuristics for Team Effectiveness Lab

        # H1: keyword coverage for team effectiveness
        domain_keywords=['team', 'effectiveness']
        hits=sum(1 for kw in domain_keywords if kw in low)
        if hits==0 and len(low)>20:
            findings.append(Finding("team-effectiveness-agent","medium","Low Team Effectiveness Lab signal","No core keywords (" + ", ".join(domain_keywords) + ") detected","Add explicit coverage of team effectiveness or confirm scope is out-of-domain"))
        metrics["keyword_hits"]=hits
        # H2: thin/structured
        if metrics["words"]<12:
            findings.append(Finding("team-effectiveness-agent","low","Thin content","Very short input — shallow analysis","Provide 2-3 representative paragraphs or a file"))
        elif metrics["words"]>1500:
            metrics["depth"]="deep"
        else:
            metrics["depth"]="standard"
        if ":" not in t and "\n" not in t.strip():
            findings.append(Finding("team-effectiveness-agent","low","Unstructured input","Single-line / no key:value structure","Provide bullets, JSON, or sections for richer output"))
        # H3: PII/bias guardrails (HR-grade)
        if pii_hits>0:
            findings.append(Finding("team-effectiveness-agent","high","PII detected (emails)","Found " + str(pii_hits) + " email(s) in input","Scrub/anonymize PII before sharing; use placeholder IDs"))
        if found_bias:
            findings.append(Finding("team-effectiveness-agent","medium","Bias language flagged","Terms: " + ", ".join(found_bias),"Rewrite with inclusive, skills-based language; add structured rubric"))
        # H4: HR compliance framing
        if any(w in low for w in ["critical","urgent","blocker","grievance","termination","legal"]):
            findings.append(Finding("team-effectiveness-agent","high","High-stakes HR language","Input declares grievance/termination/legal scope","Loop in ER/legal, document rationale, and keep audit trail"))
            metrics["hr_risk"]=True
        # H5: evidence/measure check (HR/L&D needs metrics)
        if "metric" not in low and "measure" not in low and "kpi" not in low and metrics["words"]>30:
            findings.append(Finding("team-effectiveness-agent","low","Measurement language absent","No metric/measure/KPI framing for an HR/L&D task","Add leading + lagging measures and how you will know it worked"))
        # H6: action vs insight balance
        if "action" not in low and "next step" not in low and metrics["words"]>40:
            findings.append(Finding("team-effectiveness-agent","low","Action orientation light","Few action/next-step cues in input","Close with 3 owner-dated actions"))


        # Score
        critical=sum(1 for f in findings if f.severity=="critical")
        high=sum(1 for f in findings if f.severity=="high")
        medium=sum(1 for f in findings if f.severity=="medium")
        score=max(0, 100 - critical*25 - high*15 - medium*7 - len(findings)*2)
        if critical>0:
            verdict="BLOCKED"
        elif high>=2:
            verdict="NEEDS_REVIEW"
        elif medium>=3 or high==1:
            verdict="NEEDS_REVIEW"
        elif findings:
            verdict="PASS_WITH_NOTES"
        else:
            verdict="PASS"

        next_steps=[]
        if verdict=="BLOCKED":
            next_steps.append("Fix critical findings first — they block safe progress")
        if high:
            next_steps.append(f"Triage {high} high-severity items in priority order")
        if verdict in ("NEEDS_REVIEW","BLOCKED"):
            next_steps.append("Re-run after fixes to confirm score improvement")
        if metrics.get("keyword_hits",0)==0:
            next_steps.append("Re-check with domain-specific content to improve signal")

        if not next_steps:
            next_steps.append("No blocking issues — proceed and re-check on next change")
            next_steps.append("Add this check to peer review / HRBP calibration so gaps are caught early")
        return Analysis(verdict=verdict, score=round(float(score),1), findings=findings, metrics=metrics, next_steps=next_steps)

    @classmethod
    def format_report(cls, analysis: Analysis) -> str:
        lines=[]
        lines.append(f"# {cls.__name__} Report — {analysis.verdict} (score {analysis.score}/100)")
        lines.append("")
        if analysis.metrics:
            lines.append("## Metrics")
            for k,v in analysis.metrics.items():
                lines.append(f"- **{k}**: {v}")
            lines.append("")
        if analysis.findings:
            lines.append("## Findings (ranked)")
            ranked=sorted(analysis.findings, key=lambda f: cls.SEVERITY_ORDER.get(f.severity,0), reverse=True)
            for f in ranked:
                lines.append(f"- **{f.severity.upper()}** [{f.category}] {f.title}: {f.detail} → *Fix: {f.fix}*")
            lines.append("")
        if analysis.next_steps:
            lines.append("## Next Steps")
            for i,s in enumerate(analysis.next_steps,1):
                lines.append(f"{i}. {s}")
            lines.append("")
        lines.append(f"**Verdict: {analysis.verdict}** — deterministic offline analysis, no API keys used.")
        return "\n".join(lines)
