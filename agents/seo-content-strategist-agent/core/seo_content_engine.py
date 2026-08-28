"""
SEO Content Strategist Agent Engine.
Classifies search intent, designs pillar+spoke topic clusters,
drafts outlines, internal link graphs, and E-E-A-T checklists.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class SEOStrategy:
    keyword: str
    intent: str
    cluster: List[dict] = field(default_factory=list)
    titles: List[str] = field(default_factory=list)
    outline: List[str] = field(default_factory=list)
    internal_links: List[str] = field(default_factory=list)
    eeat: List[str] = field(default_factory=list)
    serp_features: List[str] = field(default_factory=list)
    verdict: str = ""

INTENT_RULES = [
    (r"\b(how to|tutorial|guide|learn|what is|why|explained|vs)\b", "informational"),
    (r"\b(best|top|review|compare|comparison|alternative)\b", "commercial"),
    (r"\b(buy|price|pricing|cheap|discount|order|download|get)\b", "transactional"),
    (r"\b(login|sign in|docs|documentation|api)\b", "navigational"),
]

SPOKE_TEMPLATES = [
    ("definition", "What is {kw}? The plain-English definition"),
    ("howto", "How to {kw}: step-by-step with failure modes"),
    ("comparison", "{kw} vs alternatives: decision matrix"),
    ("cost", "The real cost of {kw} (with math)"),
    ("mistakes", "7 {kw} mistakes teams make (and fixes)"),
    ("benchmarks", "{kw} benchmarks: what the numbers hide"),
    ("case", "{kw} case study: before/after telemetry"),
    ("checklist", "{kw} production-readiness checklist"),
]

class SEOContentStrategistEngine:
    """Rank for a cluster, not a keyword — pages win positions; clusters win markets."""

    @classmethod
    def strategy(cls, keyword: str, audience: str = "technical decision makers",
                 intent: str = "auto") -> SEOStrategy:
        low = keyword.lower()
        if intent == "auto":
            intent = next((i for pat, i in INTENT_RULES if re.search(pat, low)), "informational")

        cluster = [{"type": "PILLAR", "title": f"The Complete Guide to {keyword} ({intent} intent)",
                    "target": "head keyword, 2,500+ words, hub for all spokes"}]
        for kind, tpl in SPOKE_TEMPLATES:
            cluster.append({"type": f"spoke:{kind}",
                            "title": tpl.format(kw=keyword),
                            "target": f"long-tail: '{kind} {keyword}' variants"})

        titles = [
            f"{keyword}: The No-BS Guide for {audience} (2026)",
            f"We Tested {keyword} for 90 Days — Here's What Broke",
            f"{keyword} in Production: 12 Failure Modes and Fixes",
            f"The {keyword} Decision Tree (Copy It)",
            f"{keyword}: What Vendors Won't Tell You",
        ]

        outline = [
            f"H1: {keyword} — the complete {intent} guide",
            f"H2: TL;DR — the 60-second answer (capture the snippet)",
            f"H2: What {keyword} actually is (definition + diagram)",
            f"H2: When {keyword} is the wrong choice (trust through honesty)",
            f"H2: How to {keyword}: step-by-step (numbered, skimmable)",
            "H2: Costs, tradeoffs, and the math (table)",
            "H2: Real examples with numbers (original data = E-E-A-T moat)",
            "H2: Common mistakes (each mapped to a fix)",
            f"H2: {keyword} checklist (downloadable/template)",
            "H2: FAQ (mine PAA questions; answer in <=45 words each)",
        ]

        links = [
            f"PILLAR <-> every spoke (bidirectional; anchor with the spoke's exact target phrase)",
            "spoke:cost <-> spoke:comparison (money pages interlink)",
            "spoke:case -> product page ONLY if the case study used the product (else E-E-A-T damage)",
            "Add 2-3 outbound links to primary sources (not competitors ranking for this term)",
        ]

        eeat = [
            "EXPERIENCE: include at least one 'we tried this and here's the scar' section with original data.",
            "EXPERTISE: name the author with credentials + byline + LinkedIn link.",
            "AUTHORITATIVENESS: cite primary sources (specs, papers, changelogs) not roundups.",
            "TRUST: publish last-updated date; own the negatives; no fake urgency.",
            "Refresh contract: this page gets a quarterly audit pass or it decays out of the top 10.",
        ]

        serp = [
            "Featured snippet: structure the TL;DR as a 45-word direct answer.",
            "People Also Ask: seed 6 PAA questions as H3s under the FAQ H2.",
            "Table box: the cost/tradeoff table targets the comparison rich result.",
            "Video: a 90s screencast earns the video pack + doubles dwell time.",
        ]

        verdict = f"CLUSTER DESIGNED | intent: {intent} | 1 pillar + {len(SPOKE_TEMPLATES)} spokes"
        return SEOStrategy(keyword, intent, cluster, titles, outline, links, eeat, serp, verdict)

    @staticmethod
    def format_strategy(s: SEOStrategy) -> str:
        out = ["=" * 62, "SEO CONTENT STRATEGIST AGENT — STRATEGY", "=" * 62,
               f"Keyword: {s.keyword} | Intent: {s.intent}", s.verdict, "-" * 62, "Topic cluster:"]
        for c in s.cluster:
            out.append(f"  [{c['type']:16}] {c['title']}")
            out.append(f"                  -> {c['target']}")
        out += ["-" * 62, "Title variants (A/B):"] + [f"  - {t}" for t in s.titles]
        out += ["-" * 62, "Pillar outline:"] + [f"  {o}" for o in s.outline]
        out += ["-" * 62, "Internal link graph:"] + [f"  * {l}" for l in s.internal_links]
        out += ["-" * 62, "E-E-A-T checklist:"] + [f"  * {e}" for e in s.eeat]
        out += ["-" * 62, "SERP feature targets:"] + [f"  * {f}" for f in s.serp_features]
        out.append("=" * 62)
        return "\n".join(out)
