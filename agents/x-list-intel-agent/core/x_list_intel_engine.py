"""
X List Intel Engine — X List Intel.
List curation, signal vs noise, and DM-able prospect surfacing
Deterministic, offline, stdlib-only. No API keys. Platform-aware + Gemini/freebie hygiene.
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


class XListIntelEngine:
    """Deterministic engine for X List Intel — zero network, platform-aware logic."""

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

        # Platform / source signals
        platform_signals = {
            "linkedin": sum(k in low for k in ["linkedin","ssi","sales navigator"]),
            "instagram": sum(k in low for k in ["instagram","insta ","reels","ig "]),
            "x": sum(k in low for k in [" x ","twitter","x.com","thread","viral hook"]),
            "youtube": sum(k in low for k in ["youtube","yt ","thumbnail","shorts","watch time"]),
            "tiktok": sum(k in low for k in ["tiktok","sound trend","spark ads"]),
            "gemini": sum(k in low for k in ["gemini","veo","imagen","google ai"]),
            "freebie": sum(k in low for k in ["pexels","pixabay","mixkit","coverr","unsplash","free stock","free audio","pixabay music"]),
        }
        detected_platform = max(platform_signals, key=platform_signals.get) if max(platform_signals.values())>0 else "agnostic"
        metrics["detected_platform"]=detected_platform
        metrics["platform_signals"]=platform_signals

        # Hook/CTA heuristics (social)
        hook_terms = ["hook","cta","pov","story","loop","cliffhanger","pattern interrupt"]
        metrics["hook_hits"]=sum(1 for k in hook_terms if k in low)
        has_cta = any(k in low for k in ["cta","call to action","link in bio","comment","subscribe","follow"])
        metrics["has_cta"]=has_cta


        # H1: keyword coverage for x list intel
        domain_keywords=['x', 'list', 'intel']
        hits=sum(1 for kw in domain_keywords if kw in low)
        if hits==0 and len(low)>20:
            findings.append(Finding("x-list-intel-agent","medium","Low X List Intel signal","No core keywords (" + ", ".join(domain_keywords) + ") detected","Add explicit coverage of x list intel or confirm scope is out-of-domain"))
        metrics["keyword_hits"]=hits
        # H2: thin/structured
        if metrics["words"]<12:
            findings.append(Finding("x-list-intel-agent","low","Thin content","Very short input — shallow analysis","Provide 2-3 representative paragraphs or a file"))
        elif metrics["words"]>1500:
            metrics["depth"]="deep"
        else:
            metrics["depth"]="standard"
        if ":" not in t and "\n" not in t.strip():
            findings.append(Finding("x-list-intel-agent","low","Unstructured input","Single-line / no key:value structure","Provide bullets, JSON, or sections for richer output"))
        # H3: social growth guardrails
        if not has_cta and metrics["words"]>25:
            findings.append(Finding("x-list-intel-agent","low","CTA absent","No clear call-to-action detected for a social growth task","Add one CTA (comment/follow/link) per post"))
        if metrics["hook_hits"]==0 and "Social: X" in ["Social: LinkedIn","Social: X","Social: TikTok","Social: Instagram","Social: YouTube"]:
            findings.append(Finding("x-list-intel-agent","low","Hook language light","No hook/CTA/pov/loop cues for a virality task","Lead with a hook in first 2 seconds / first line"))
        # H4: freebie license hygiene (video)
        if "Social: X"=="Video: Freebie + Gemini":
            if "attribution" not in low and "license" not in low and metrics["words"]>20:
                findings.append(Finding("x-list-intel-agent","medium","License hygiene absent","No attribution/license framing for freebie-sourced video","State source + license (Pexels/Pixabay/Mixkit) and keep attribution file"))
            if "gemini" not in low and "veo" not in low and "free" not in low and detected_platform=="agnostic":
                findings.append(Finding("x-list-intel-agent","low","Freebie/Gemini signal absent","No free-stock or Gemini cue for a video-gen task","Name source (Pexels/Pixabay/Mixkit) or Gemini/VeO prompt"))
        # H5: platform mismatch
        if "Social: X".startswith("Social:") and detected_platform!="agnostic" and "Social: X".split(":")[1].strip().lower() not in detected_platform and detected_platform not in ["agnostic"]:
            # only flag if strong mismatch (e.g., YouTube agent but input says tiktok only)
            if platform_signals.get(detected_platform,0)>=2:
                findings.append(Finding("x-list-intel-agent","low","Platform mismatch hint","Input strongly signals " + detected_platform + " but agent is Social: X","Confirm target platform or route to the right agent"))
        # H6: spam/rate-limit safety
        if any(k in low for k in ["spam","scrape","bot","auto follow","auto like","bulk dm"]):
            findings.append(Finding("x-list-intel-agent","high","Automation risk language","Input mentions bulk/scrape/bot — platform rate-limit risk","Throttle, add human review, keep ToS-compliant allowlists"))


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
            next_steps.append("Fix critical findings first — they block safe publish")
        if high:
            next_steps.append(f"Triage {high} high-severity items in priority order")
        if verdict in ("NEEDS_REVIEW","BLOCKED"):
            next_steps.append("Re-run after fixes to confirm score improvement")
        if metrics.get("keyword_hits",0)==0:
            next_steps.append("Re-check with domain-specific content to improve signal")

        if not next_steps:
            next_steps.append("No blocking issues — schedule and monitor first 48h")
            next_steps.append("Add to content calendar and re-check after publish (hook/retention)")
        if detected_platform!="agnostic":
            next_steps.append(f"Re-run with platform={detected_platform} for platform-native checks")
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
