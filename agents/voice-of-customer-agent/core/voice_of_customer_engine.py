"""
Voice of Customer Agent Engine.
Mines feedback corpora into quantified themes, per-theme sentiment,
and a prioritized top-5 fix list.
"""

import re
from collections import Counter
from dataclasses import dataclass, field
from typing import List

@dataclass
class VoCReport:
    n_items: int
    themes: List[dict] = field(default_factory=list)
    overall_sentiment: float = 0.0
    top_pain_points: List[dict] = field(default_factory=list)
    quotes: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    verdict: str = ""

STOP = set("""the a an and or but of for to in on with how do i my your is are be can what when why
it this that at as from by was were very really just so too also not no yes has have had they them
their there here you we i me our us if then than out up down about into over under again more most
some any all each few other such only own same s t don now d ll m o re ve y ain aren couldn didn
doesn hadn hasn haven isn ma mightn mustn needn shan shouldn wasn weren won wouldn""".split())

NEG_WORDS = set("""slow broken crashes confusing terrible awful worst hate annoying frustrating
clunky laggy buggy useless difficult hard fails missing useless expensive overpriced unreliable
painful inconsistent can't cannot wont won't""".split())
POS_WORDS = set("""love great excellent amazing awesome fast reliable intuitive easy clean beautiful
perfect helpful best smooth delightful impressed straightforward""".split())

THEME_KEYWORDS = {
    "performance": ["slow", "laggy", "latency", "performance", "load time", "fast", "speed"],
    "reliability": ["crash", "down", "bug", "buggy", "error", "fails", "unreliable", "outage"],
    "usability": ["confusing", "difficult", "hard to", "intuitive", "easy", "ux", "ui", "navigation", "clunky"],
    "pricing": ["expensive", "pricing", "price", "cost", "overpriced", "value", "worth"],
    "support": ["support", "ticket", "response time", "help", "service"],
    "onboarding": ["setup", "onboarding", "getting started", "documentation", "docs", "tutorial"],
    "integrations": ["integration", "api", "connect", "webhook", "sync"],
    "missing_features": ["wish", "missing", "add", "feature", "should have", "need a"],
}

class VoiceOfCustomerEngine:
    """Quantify the screams: every theme gets volume, sentiment, and a revenue word check."""

    @classmethod
    def analyze(cls, items: List[str]) -> VoCReport:
        if not items:
            return VoCReport(0, [], 0.0, [], [], ["No feedback items provided."], "NO_DATA")

        item_themes, item_scores = [], []
        for text in items:
            low = text.lower()
            words = set(re.findall(r"[a-z']+", low))
            neg = len(words & NEG_WORDS)
            pos = len(words & POS_WORDS)
            item_scores.append(pos - neg)
            themes = []
            for theme, kws in THEME_KEYWORDS.items():
                hits = sum(1 for kw in kws if kw in low)
                if hits >= 1:
                    themes.append(theme)
            item_themes.append(themes)

        theme_stats = {}
        for themes, score, text in zip(item_themes, item_scores, items):
            for t in themes:
                st = theme_stats.setdefault(t, {"count": 0, "neg": 0, "pos": 0, "samples": []})
                st["count"] += 1
                if score < 0:
                    st["neg"] += 1
                elif score > 0:
                    st["pos"] += 1
                if score < 0 and len(st["samples"]) < 2:
                    st["samples"].append(text[:110])

        themes_out = []
        for t, st in sorted(theme_stats.items(), key=lambda kv: -kv[1]["count"]):
            net = st["pos"] - st["neg"]
            themes_out.append({
                "theme": t, "volume": st["count"],
                "share": round(100 * st["count"] / len(items), 1),
                "negative": st["neg"], "positive": st["pos"],
                "net_sentiment": net,
                "severity": "high" if st["neg"] >= max(2, st["count"] * 0.5) else
                            "medium" if st["neg"] else "low",
            })

        # pain ranking: negative volume * weight
        weights = {"reliability": 1.4, "performance": 1.2, "usability": 1.0, "pricing": 0.9,
                   "support": 1.1, "onboarding": 0.8, "integrations": 1.0, "missing_features": 0.6}
        pain = sorted(({"theme": t["theme"], "pain_score": round(t["negative"] * weights.get(t["theme"], 1.0), 1),
                        "share": t["share"]} for t in themes_out if t["negative"] > 0),
                      key=lambda d: -d["pain_score"])[:5]

        overall = round(sum(item_scores) / len(item_scores), 2)
        quotes = []
        for text, score in zip(items, item_scores):
            if score <= -2 and len(quotes) < 3:
                quotes.append(f'"{text[:140]}"')

        recs = []
        for p in pain[:3]:
            rec_map = {
                "performance": "Profile + set perf budgets in CI; publish a speed wins changelog.",
                "reliability": "Stand up an error-budget policy; weekly bug-burn review until error rate halves.",
                "usability": "Run 5 moderated sessions on the top confusion point; fix the #1 issue within a sprint.",
                "pricing": "Publish a value-justified pricing page; add annual+usage options.",
                "support": "Reduce first-response SLA; add a rescue lane for P1 tickets.",
                "onboarding": "Rebuild the first-15-minutes path; measure activation rate weekly.",
                "integrations": "Ship the top-requested integration; document the webhook API.",
                "missing_features": "Public roadmap with voting; commit dates for the top 3 asks.",
            }
            recs.append(f"{p['theme']} (pain {p['pain_score']}): " + rec_map.get(p["theme"], "Investigate with the product team."))

        verdict = f"{len(items)} items | {len(themes_out)} themes | net sentiment {overall:+.2f}"
        return VoCReport(len(items), themes_out, overall, pain, quotes, recs, verdict)

    @staticmethod
    def format_report(r: VoCReport) -> str:
        out = ["=" * 62, "VOICE OF CUSTOMER AGENT — REPORT", "=" * 62, r.verdict, "-" * 62,
               "Theme table (volume / sentiment):"]
        for t in r.themes:
            out.append(f"  {t['theme']:18} vol={t['volume']:3} ({t['share']:4.1f}%) "
                       f"neg={t['negative']:3} pos={t['positive']:3} net={t['net_sentiment']:+d} [{t['severity']}]")
        if r.top_pain_points:
            out += ["-" * 62, "Top pain points (neg-volume weighted):"]
            out += [f"  {p['pain_score']:5.1f}  {p['theme']} ({p['share']}% of feedback)" for p in r.top_pain_points]
        if r.quotes:
            out += ["-" * 62, "Verbatims (loudest detractors):"] + [f"  {q}" for q in r.quotes]
        out += ["-" * 62, "Recommendations:"]
        out += [f"  {i}. {rec}" for i, rec in enumerate(r.recommendations, 1)]
        out.append("=" * 62)
        return "\n".join(out)
