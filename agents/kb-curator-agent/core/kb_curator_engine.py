"""
KB Curator Agent Engine.
Audits a knowledge base for coverage gaps, near-duplicate articles, staleness,
and produces a curation plan mapped to ticket themes.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class Article:
    id: str
    title: str
    tokens: set
    updated: str
    words: int

@dataclass
class CurationReport:
    total_articles: int
    avg_words: float
    duplicates: List[dict] = field(default_factory=list)
    stale: List[str] = field(default_factory=list)
    thin_content: List[str] = field(default_factory=list)
    coverage: dict = field(default_factory=dict)
    gaps: List[str] = field(default_factory=list)
    plan: List[str] = field(default_factory=list)
    verdict: str = ""

STOP = set("the a an of for to in on with how do i my your is are be can what when why and or to you we it this that at as from by".split())

class KBCuratorEngine:
    """A KB is deflection capital — audit it like a portfolio."""

    @staticmethod
    def _tokens(text: str) -> set:
        return {w for w in re.findall(r"[a-z]{3,}", text.lower()) if w not in STOP}

    @classmethod
    def curate(cls, articles: List[dict], ticket_themes: List[str] = None) -> CurationReport:
        ticket_themes = ticket_themes or []
        parsed: List[Article] = []
        for a in articles:
            body = str(a.get("body", "")) + " " + str(a.get("title", ""))
            parsed.append(Article(str(a.get("id", "?")), str(a.get("title", "untitled")),
                                  cls._tokens(body), str(a.get("updated", "")),
                                  len(str(a.get("body", "")).split())))

        # duplicates via Jaccard
        dups = []
        for i in range(len(parsed)):
            for j in range(i + 1, len(parsed)):
                inter = parsed[i].tokens & parsed[j].tokens
                union = parsed[i].tokens | parsed[j].tokens
                sim = len(inter) / len(union) if union else 0.0
                if sim >= 0.45:
                    dups.append({"a": parsed[i].id, "b": parsed[j].id,
                                 "similarity": round(sim, 2),
                                 "keep": parsed[i].id if parsed[i].words >= parsed[j].words else parsed[j].id,
                                 "merge": parsed[j].id if parsed[i].words >= parsed[j].words else parsed[i].id})
        # coverage per theme
        coverage = {}
        for theme in ticket_themes:
            tt = cls._tokens(theme)
            best = 0.0
            best_id = "-"
            for p in parsed:
                inter = tt & p.tokens
                cov = len(inter) / len(tt) if tt else 0
                if cov > best:
                    best, best_id = cov, p.id
            coverage[theme] = {"score": round(best, 2), "closest": best_id}

        gaps = [t for t, c in coverage.items() if c["score"] < 0.34]

        stale = [p.id for p in parsed if re.match(r"^20(1\d|2[0-2])", p.updated)]
        stale += [p.id for p in parsed if not p.updated]
        stale = list(dict.fromkeys(stale))
        thin = [p.id for p in parsed if p.words < 60]

        plan = []
        for d in dups[:5]:
            plan.append(f"Merge {d['merge']} into {d['keep']} (Jaccard {d['similarity']}); redirect the old URL.")
        for t in thin[:5]:
            plan.append(f"Expand article {t}: thin content (<60 words) cannot deflect a ticket.")
        for g in gaps[:5]:
            plan.append(f"Write NEW article for theme '{g}' — tickets exist, coverage is near-zero.")
        if stale:
            plan.append(f"Freshness pass on {len(stale)} article(s): verify screenshots, versions, and links.")
        if not plan:
            plan.append("KB is healthy: no merges, gaps, or staleness detected this cycle.")

        avg = round(sum(p.words for p in parsed) / len(parsed), 1) if parsed else 0
        health = 100 - 6 * len(dups) - 4 * len(gaps) - 3 * len(thin) - 2 * len(stale)
        verdict = f"KB_HEALTH {max(5, health)}/100 | {len(dups)} dup pairs, {len(gaps)} gaps, {len(stale)} stale"
        return CurationReport(len(parsed), avg, dups, stale, thin, coverage, gaps, plan, verdict)

    @staticmethod
    def format_report(r: CurationReport) -> str:
        out = ["=" * 62, "KB CURATOR AGENT — REPORT", "=" * 62, r.verdict, "-" * 62,
               f"Articles: {r.total_articles} | avg length: {r.avg_words} words"]
        if r.duplicates:
            out += ["-" * 62, "Near-duplicates (merge candidates):"]
            out += [f"  {d['a']} <-> {d['b']} sim={d['similarity']} (keep {d['keep']})" for d in r.duplicates[:6]]
        if r.coverage:
            out += ["-" * 62, "Ticket-theme coverage:"]
            out += [f"  {t}: {c['score']:.0%} (closest: {c['closest']})" for t, c in r.coverage.items()]
        if r.gaps:
            out += ["  GAPS: " + ", ".join(r.gaps)]
        if r.thin_content:
            out += ["-" * 62, "Thin content: " + ", ".join(r.thin_content[:8])]
        out += ["-" * 62, "Curation plan:"]
        out += [f"  {i}. {p}" for i, p in enumerate(r.plan, 1)]
        out.append("=" * 62)
        return "\n".join(out)
