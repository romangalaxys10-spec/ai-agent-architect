"""
Deep Research Agent Engine.
Decomposes research questions, extracts claims per source, builds
corroboration/contradiction matrices, and answers with confidence bands.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class SubQuestion:
    question: str
    answer: str
    confidence: float
    supporting: List[str] = field(default_factory=list)
    contradicting: List[str] = field(default_factory=list)

@dataclass
class ResearchSynthesis:
    question: str
    sub_questions: List[SubQuestion] = field(default_factory=list)
    corroboration: List[dict] = field(default_factory=list)
    contradictions: List[str] = field(default_factory=list)
    unverifiable: List[str] = field(default_factory=list)
    source_quality: dict = field(default_factory=dict)
    confidence_band: str = ""
    verdict: str = ""

STOP = set("""the a an of for to in on with and or is are was were be been being that this these those it its
as at by from into over under about across per via we they you i not no nor but if then than so such can could
may might will would should shall must have has had do does did done""".split())

HEDGES = ["may", "might", "could", "possibly", "suggests", "appears", "unclear", "unknown",
          "debated", "contested", "it depends", "preliminary"]

NUM_RE = re.compile(r"-?\$?\d[\d,.]*\s?(%|percent|billion|million|thousand|x|USD)?", re.I)

class DeepResearchEngine:
    """Research integrity: cross-examine sources before synthesizing anything."""

    @staticmethod
    def _claims(text: str) -> List[str]:
        sents = re.split(r"(?<=[.!?])\s+", text.replace("\n", " "))
        out = []
        for s in sents:
            s = s.strip()
            if len(s.split()) >= 6 and any(c.isalnum() for c in s):
                out.append(s)
        return out[:8]

    @staticmethod
    def _overlap(a: str, b: str) -> float:
        ta = {w for w in re.findall(r"[a-z]{4,}", a.lower()) if w not in STOP}
        tb = {w for w in re.findall(r"[a-z]{4,}", b.lower()) if w not in STOP}
        return len(ta & tb) / len(ta | tb) if ta | tb else 0.0

    @staticmethod
    def _overlap_coef(a: str, b: str) -> float:
        """Overlap coefficient: |A n B| / min(|A|, |B|) — robust to length asymmetry."""
        ta = {w for w in re.findall(r"[a-z]{4,}", a.lower()) if w not in STOP}
        tb = {w for w in re.findall(r"[a-z]{4,}", b.lower()) if w not in STOP}
        return len(ta & tb) / min(len(ta), len(tb)) if ta and tb else 0.0

    @classmethod
    def synthesize(cls, question: str, sources: List[str]) -> ResearchSynthesis:
        # decompose the question
        q_words = [w for w in re.findall(r"[a-z]{4,}", question.lower()) if w not in STOP]
        sub_qs = []
        if len(q_words) >= 3:
            sub_qs.append(f"What is the current state of '{q_words[0]} {q_words[1]}'?")
            sub_qs.append(f"What quantitative evidence exists on {question.strip('?').lower()}?")
            sub_qs.append(f"What disagreements or open questions remain about {q_words[0]}?")
        else:
            sub_qs = [question, f"What evidence supports or refutes: {question}?"]

        src_claims = []
        for i, src in enumerate(sources, 1):
            for c in cls._claims(src):
                src_claims.append({"src": f"S{i}", "claim": c})
        src_quality = {}
        for i, src in enumerate(sources, 1):
            numbers = len(NUM_RE.findall(src))
            words = len(src.split())
            src_quality[f"S{i}"] = {"words": words, "quant_claims": numbers,
                                    "grade": "A" if numbers >= 2 and words > 80 else
                                             "B" if numbers >= 1 else "C"}

        # corroboration matrix: claim pairs across DIFFERENT sources with high overlap
        corrob, contras = [], []
        for i in range(len(src_claims)):
            for j in range(i + 1, len(src_claims)):
                if src_claims[i]["src"] == src_claims[j]["src"]:
                    continue
                ov = cls._overlap_coef(src_claims[i]["claim"], src_claims[j]["claim"])
                if ov >= 0.42:
                    # numeric contradiction check
                    def _digits(tok):
                        d = ""
                        for ch in tok:
                            if ch.isdigit() or ch in ".,-":
                                d += ch
                            else:
                                break
                        return d.rstrip(".,")
                    ni = {_digits(mt.group(0)) for mt in NUM_RE.finditer(src_claims[i]["claim"])}
                    nj = {_digits(mt.group(0)) for mt in NUM_RE.finditer(src_claims[j]["claim"])}
                    nums_i = {x for x in ni if x}; nums_j = {x for x in nj if x}
                    if nums_i and nums_j and not (nums_i & nums_j):
                        contras.append(f"{src_claims[i]['src']} says {nums_i} vs "
                                       f"{src_claims[j]['src']} says {nums_j} "
                                       f"(topic: {src_claims[i]['claim'][:60]}...)")
                    else:
                        corrob.append({"claims": (src_claims[i]["claim"][:70], src_claims[j]["claim"][:70]),
                                       "sources": (src_claims[i]["src"], src_claims[j]["src"]),
                                       "overlap": round(ov, 2)})

        # answer sub-questions from claims
        subs_out = []
        for sq in sub_qs:
            scored = sorted(((cls._overlap(sq, c["claim"]), c) for c in src_claims),
                            key=lambda t: -t[0])
            top = [c for ov, c in scored[:3] if ov > 0.15]
            conf = min(0.95, 0.25 + 0.2 * len(top) + 0.1 * len(sources))
            if top:
                answer = ("Evidence converges on: " +
                          " / ".join(c["claim"][:110] for c in top[:2]))
            else:
                answer = "Insufficient direct evidence in provided sources — treat as open."
                conf = 0.15
            subs_out.append(SubQuestion(sq, answer, round(conf, 2),
                                        [c["src"] for c in top],
                                        [f"{c['src']}" for c in top if any(c["claim"][:40] in x for x in contras)]))

        unverifiable = []
        for c in src_claims:
            if NUM_RE.search(c["claim"]) and not any(
                    c["claim"][:50] in (cc["claims"][0] + cc["claims"][1]) for cc in corrob):
                if any(h in c["claim"].lower() for h in HEDGES):
                    unverifiable.append(f"{c['src']}: {c['claim'][:90]}")

        mean_conf = sum(s.confidence for s in subs_out) / len(subs_out) if subs_out else 0
        band = ("HIGH" if mean_conf >= 0.7 else "MEDIUM" if mean_conf >= 0.45 else "LOW")
        verdict = (f"{len(sources)} sources | {len(src_claims)} claims | "
                   f"{len(corrob)} corroborations | {len(contras)} contradictions | confidence {band}")
        return ResearchSynthesis(question, subs_out, corrob, contras, unverifiable[:5],
                                 src_quality, band, verdict)

    @staticmethod
    def format_synthesis(s: ResearchSynthesis) -> str:
        out = ["=" * 62, "DEEP RESEARCH AGENT — SYNTHESIS", "=" * 62,
               f"Q: {s.question}", s.verdict, "-" * 62, "Source quality:"]
        out += [f"  {k}: {v['words']} words, {v['quant_claims']} quantitative claims [grade {v['grade']}]"
                for k, v in s.source_quality.items()] or ["  (no sources provided)"]
        out += ["-" * 62, "Sub-question answers:"]
        for i, sq in enumerate(s.sub_questions, 1):
            out.append(f"  Q{i}. {sq.question}")
            out.append(f"      A: {sq.answer}")
            out.append(f"      confidence: {sq.confidence:.0%} | supporting: {', '.join(sq.supporting) or 'none'}")
        if s.corroboration:
            out += ["-" * 62, f"Corroborated claims ({len(s.corroboration)}):"]
            for c in s.corroboration[:4]:
                out.append(f"  {c['sources'][0]}+{c['sources'][1]} (overlap {c['overlap']}): {c['claims'][0]}...")
        if s.contradictions:
            out += ["-" * 62, "CONTRADICTIONS (must resolve before citing):"]
            out += [f"  ! {c}" for c in s.contradictions[:5]]
        if s.unverifiable:
            out += ["-" * 62, "Hedged/unverifiable numeric claims:"]
            out += [f"  ? {u}" for u in s.unverifiable]
        out += ["-" * 62, f"OVERALL CONFIDENCE: {s.confidence_band}", "=" * 62]
        return "\n".join(out)
