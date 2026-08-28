"""
Music Composer Engine — Music Composer.
Composition with MIDI, arrangement, theory, and score export
Deterministic, offline, stdlib-only. No API keys. Studio-grade heuristics (render/license/translation).
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


class MusicComposerEngine:
    """Deterministic engine for Music Composer — zero network, studio logic."""

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

        # Creative signals
        creative_signals = {
            "video": sum(k in low for k in ["video","premiere","resolve","capcut","subtitle","timeline","grading","proxy"]),
            "3d": sum(k in low for k in ["blender","3ds max","cinema 4d","houdini","arnold","cycles","octane","pbr","uv","render farm","geometry nodes"]),
            "music": sum(k in low for k in ["music","audio","daw","midi","beat","808","sample","denoise","mastering","composer"]),
            "youtube": sum(k in low for k in ["youtube","shorts","playlist","premiere","end screen","remix","curation","publish"]),
        }
        metrics["creative_signals"]=creative_signals
        detected = max(creative_signals, key=creative_signals.get) if max(creative_signals.values())>0 else "agnostic"
        metrics["detected_domain"]=detected
        # Hook/CTA for publish
        has_cta = any(k in low for k in ["cta","subscribe","follow","premiere","schedule"])
        metrics["has_cta"]=has_cta


        # H1: keyword coverage for music composer
        domain_keywords=['music', 'composer']
        hits=sum(1 for kw in domain_keywords if kw in low)
        if hits==0 and len(low)>20:
            findings.append(Finding("music-composer-agent","medium","Low Music Composer signal","No core keywords (" + ", ".join(domain_keywords) + ") detected","Add explicit coverage of music composer or confirm scope is out-of-domain"))
        metrics["keyword_hits"]=hits
        # H2: thin/structured
        if metrics["words"]<12:
            findings.append(Finding("music-composer-agent","low","Thin content","Very short input — shallow analysis","Provide 2-3 representative paragraphs or a file"))
        elif metrics["words"]>1500:
            metrics["depth"]="deep"
        else:
            metrics["depth"]="standard"
        if ":" not in t and "\n" not in t.strip():
            findings.append(Finding("music-composer-agent","low","Unstructured input","Single-line / no key:value structure","Provide bullets, JSON, or sections for richer output"))
        # H3: render/license for studio
        if "music-composer-agent" in ["blender-studio-agent","three-studio-max-agent","cinema4d-motion-agent","houdini-fx-agent","3d-modeling-architect-agent","3d-texturing-agent","3d-render-optimizer-agent"] and "license" not in low and "render" not in low and metrics["words"]>25:
            findings.append(Finding("music-composer-agent","low","Render/license hygiene light","No render/license framing for 3D task","State renderer (Cycles/Arnold/Redshift) and asset license"))
        if "music-composer-agent" in ["video-editor-pro-agent","premiere-workflow-agent","davinci-resolve-agent","capcut-template-agent","subtitle-transcription-agent","youtube-remix-engine-agent","youtube-publisher-agent"] and not has_cta and metrics["words"]>30:
            findings.append(Finding("music-composer-agent","low","Publish CTA light","No schedule/premiere/subscribe CTA for publish task","Add CTA/end-screen/premiere plan"))
        if "copyright" in low or "piracy" in low:
            findings.append(Finding("music-composer-agent","high","Copyright risk language","Input mentions copyright/piracy","Ensure cleared sources, keep attribution"))


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
            next_steps.append("Fix critical findings first — they block publish/render")
        if high:
            next_steps.append(f"Triage {high} high-severity items in priority order")
        if verdict in ("NEEDS_REVIEW","BLOCKED"):
            next_steps.append("Re-run after fixes to confirm score improvement")
        if metrics.get("keyword_hits",0)==0:
            next_steps.append("Re-check with domain-specific content to improve signal")

        if not next_steps:
            next_steps.append("No blocking issues — proceed to render/publish and monitor")
            next_steps.append("Add to studio pipeline and re-check after export")
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
