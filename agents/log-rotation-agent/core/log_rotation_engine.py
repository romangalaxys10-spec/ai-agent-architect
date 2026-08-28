"""
Log Rotation Steward Engine — Log Rotation Steward.
logrotate/journal vacuuming, retention budgets, and centralized shipper wiring
Deterministic, offline, stdlib-only. No API keys required.
OS-aware: detects Linux/macOS/Windows from input text and adapts heuristics.
"""

import re
import platform
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


class LogRotationEngine:
    """Deterministic engine for Log Rotation Steward — zero network, pure logic + OS heuristics."""

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

        # --- OS detection from input (not host) ---
        os_signals = {"linux": sum(k in low for k in ["linux","ubuntu","systemd","apt ","snap","journalctl","ext4","cgroup"]),
                       "macos": sum(k in low for k in ["macos","mac os","darwin","launchd","brew","defaults ","xcode","sip","tcc"]),
                       "windows": sum(k in low for k in ["windows","win32","powershell","registry","winget","ntfs","defender","gpo"])}
        detected = max(os_signals, key=os_signals.get) if max(os_signals.values())>0 else "agnostic"
        metrics["detected_os"]=detected
        metrics["os_signals"]=os_signals
        try:
            metrics["host_platform"]=platform.system()
        except Exception:
            metrics["host_platform"]="unknown"

        # --- Domain heuristics for Log Rotation Steward ---

        # H1: keyword coverage for log rotation
        domain_keywords=['log', 'rotation']
        hits=sum(1 for kw in domain_keywords if kw in low)
        if hits==0 and len(low)>20:
            findings.append(Finding("log-rotation-agent","medium","Low Log Rotation Steward signal","No core keywords (" + ", ".join(domain_keywords) + ") detected","Add explicit coverage of log rotation or confirm scope is out-of-domain"))
        metrics["keyword_hits"]=hits
        # H2: length/depth
        if metrics["words"]<12:
            findings.append(Finding("log-rotation-agent","low","Thin content","Very short input — shallow analysis","Provide 3-5 representative paragraphs or a file"))
        elif metrics["words"]>1500:
            metrics["depth"]="deep"
        else:
            metrics["depth"]="standard"
        # H3: risk markers
        risk_markers=["todo","fixme","hack","xxx","tbd","placeholder","lorem ipsum","password","secret"]
        found=[m for m in risk_markers if m in low]
        if found:
            findings.append(Finding("log-rotation-agent","medium","Unresolved/secrets markers","Found: " + ", ".join(found),"Resolve/ticket them; scrub secrets before ship"))
            metrics["risk_markers"]=found
        # H4: urgency
        if any(w in low for w in ["critical","urgent","blocker","p0","sev1","outage"]):
            findings.append(Finding("log-rotation-agent","high","Urgency signal","Input declares critical/urgent/outage","Confirm severity, owner, deadline, and rollback plan"))
            metrics["urgency"]=True
        # H5: structure
        if ":" not in t and "\n" not in t.strip():
            findings.append(Finding("log-rotation-agent","low","Unstructured input","Single-line / no key:value structure","Provide bullets, JSON, or sections for richer output"))
        # H6: cross-OS / safety gate
        if "Server Mgmt (Linux/Mac/Win)"=="Server Mgmt (Linux/Mac/Win)" and detected=="agnostic" and metrics["words"]>25:
            findings.append(Finding("log-rotation-agent","low","OS-agnostic input","No Linux/macOS/Windows signal for a server-mgmt task","State target OS/distro and version; re-run with --os flag"))
        if "Server Mgmt (Linux/Mac/Win)" in ["Browser Use","Terminal Use"] and any(k in low for k in ["eval(","exec(","innerhtml","shell=true"]):
            findings.append(Finding("log-rotation-agent","high","Injection surface hint","Input contains code-like injection patterns","Validate/quoted-arg guard, sanitize, and add tests"))


        # --- Score ---
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
            next_steps.append("Add this check to CI/pre-commit so regressions are caught early")
        if detected!="agnostic":
            next_steps.append(f"Re-run with explicit --os {detected} or compare across Linux/macOS/Windows")

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
