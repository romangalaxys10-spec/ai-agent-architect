"""
Oracle Keeper Engine — Oracle Keeper.
Price feeds, staleness, and circuit breaker
Deterministic, offline, stdlib-only. No API keys. SysAdmin-grade heuristics.
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


class OracleKeeperEngine:
    """Deterministic engine for Oracle Keeper — zero network, sysadmin logic."""

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

        # SysAdmin signals
        sys_signals = {
            "solana": sum(k in low for k in ["solana","anchor","pda","spl","jito","geyser","validator"]),
            "blockchain": sum(k in low for k in ["evm","solidity","contract","gas","bridge","wallet","dao"]),
            "linux": sum(k in low for k in ["linux","systemd","kernel","selinux","cron","fsck"]),
            "server": sum(k in low for k in ["server","nginx","k8s","prometheus","bare metal","provision"]),
            "security": sum(k in low for k in ["cve","vuln","threat","siem","cspm","zero trust"]),
            "debug": sum(k in low for k in ["debug","trace","flaky","bisect","heap dump","static analysis"]),
            "llm": sum(k in low for k in ["llm","ollama","vllm","gguf","quantizer","kv cache","inference"]),
            "webdesign": sum(k in low for k in ["figma","design token","wireframe","a11y","motion","landing page"]),
            "webdev": sum(k in low for k in ["frontend","backend","api","ssr","jamstack","websocket","cms","web perf"]),
        }
        metrics["sys_signals"]=sys_signals
        detected = max(sys_signals, key=sys_signals.get) if max(sys_signals.values())>0 else "agnostic"
        metrics["detected_domain"]=detected


        # H1: keyword coverage for oracle keeper
        domain_keywords=['oracle', 'keeper']
        hits=sum(1 for kw in domain_keywords if kw in low)
        if hits==0 and len(low)>20:
            findings.append(Finding("oracle-keeper-agent","medium","Low Oracle Keeper signal","No core keywords (" + ", ".join(domain_keywords) + ") detected","Add explicit coverage of oracle keeper or confirm scope is out-of-domain"))
        metrics["keyword_hits"]=hits
        # H2: thin/structured
        if metrics["words"]<12:
            findings.append(Finding("oracle-keeper-agent","low","Thin content","Very short input — shallow analysis","Provide 2-3 representative paragraphs or a file"))
        elif metrics["words"]>1500:
            metrics["depth"]="deep"
        else:
            metrics["depth"]="standard"
        if ":" not in t and "\n" not in t.strip():
            findings.append(Finding("oracle-keeper-agent","low","Unstructured input","Single-line / no key:value structure","Provide bullets, JSON, or sections for richer output"))
        # H3: domain-specific safety (Solana/chain: key exposure, Linux: secrets, Security: CVE, LLM: VRAM)
        if any(k in low for k in ["private key","mnemonic","seed phrase","secret key"]):
            findings.append(Finding("oracle-keeper-agent","critical","Secret exposure","Private key/mnemonic in input","Redact immediately, rotate, and use env/secret manager"))
        if "password" in low and "password" in "oracle-keeper-agent":
            pass
        if "SysAdmin: Blockchain" in ["SysAdmin: Security/Optimization"] and "cve" not in low and "patch" not in low and metrics["words"]>25:
            findings.append(Finding("oracle-keeper-agent","low","Patch hygiene light","No CVE/patch framing for a security task","Add CVE, EPSS, and patch SLA"))
        if "SysAdmin: Blockchain"=="SysAdmin: Local LLM" and not any(k in low for k in ["vram","quant","latency","throughput","ttft"]):
            findings.append(Finding("oracle-keeper-agent","low","Perf framing absent","No VRAM/quant/latency framing for a local LLM perf task","Add TTFT/TPS, VRAM, and quant tradeoff"))
        # H4: urgency
        if any(w in low for w in ["critical","urgent","blocker","p0","sev1","outage","exploit"]):
            findings.append(Finding("oracle-keeper-agent","high","Urgency signal","Input declares critical/urgent/outage/exploit","Confirm severity, owner, deadline, and rollback"))
            metrics["urgency"]=True
        # H5: cross-domain mismatch hint
        if "SysAdmin: Blockchain"=="SysAdmin: Solana" and sys_signals.get("solana",0)==0 and metrics["words"]>25:
            findings.append(Finding("oracle-keeper-agent","low","Solana signal absent","No solana/anchor/spl cue for a Solana task","Confirm chain target or route to EVM/general agent"))


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
            next_steps.append("Fix critical findings first — they block safe deploy")
        if high:
            next_steps.append(f"Triage {high} high-severity items in priority order")
        if verdict in ("NEEDS_REVIEW","BLOCKED"):
            next_steps.append("Re-run after fixes to confirm score improvement")
        if metrics.get("keyword_hits",0)==0:
            next_steps.append("Re-check with domain-specific content to improve signal")

        if not next_steps:
            next_steps.append("No blocking issues — proceed and re-check on next change")
            next_steps.append("Add to CI/pre-deploy gate so regressions are caught early")
        if detected!="agnostic":
            next_steps.append(f"Detected domain={detected} — re-run with targeted input for deeper checks")
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
