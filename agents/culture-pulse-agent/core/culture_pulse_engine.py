"""
Culture Pulse Agent Engine.
Analyzes engagement surveys: eNPS, distribution, comment themes,
segment gaps, and 2-3 interventions mapped to detractor themes.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class PulseReport:
    n: int
    enps: int
    distribution: dict = field(default_factory=dict)
    segments: List[dict] = field(default_factory=list)
    themes: List[dict] = field(default_factory=list)
    interventions: List[str] = field(default_factory=list)
    caveats: List[str] = field(default_factory=list)
    verdict: str = ""

NEG = {"overworked", "burnout", "burned", "underpaid", "understaffed", "chaos", "politics",
       "meetings", "micromanage", "unclear", "toxic", "ignored", "blocked", "slow", "stress",
       "layoffs", "anxiety", "leaving", "quit", "unfair", "favoritism", "reorg", "deadline"}
POS = {"growth", "learn", "learning", "autonomy", "trust", "supportive", "flexible", "clear",
       "impact", "proud", "team", "collaborate", "transparent", "recognition", "fair", "mission",
       "ownership", "mentorship", "healthy", "balanced"}
THEME_MAP = {
    "workload": ["overworked", "burnout", "understaffed", "deadline", "chaos", "meetings", "stress"],
    "growth": ["growth", "learn", "learning", "mentorship", "career"],
    "autonomy_trust": ["micromanage", "autonomy", "trust", "ownership"],
    "clarity": ["unclear", "clear", "strategy", "priority", "priorities", "reorg"],
    "comp_fairness": ["underpaid", "compensation", "salary", "unfair", "fair", "pay"],
    "leadership": ["leadership", "management", "manager", "transparent", "politics"],
}

class CulturePulseEngine:
    """Survey data is a lagging indicator of trust — read comments before scores."""

    @classmethod
    def analyze(cls, responses: List[dict]) -> PulseReport:
        if not responses:
            return PulseReport(0, 0, verdict="NO_DATA")

        scores = [int(r.get("score", 0)) for r in responses if str(r.get("score", "")).isdigit() or isinstance(r.get("score"), (int, float))]
        comments = [str(r.get("comment", "")) for r in responses if r.get("comment")]
        segments = [str(r.get("segment", r.get("team", "all"))) for r in responses]

        promoters = sum(1 for s in scores if s >= 9)
        passives = sum(1 for s in scores if 7 <= s < 9)
        detractors = sum(1 for s in scores if s < 7)
        n = len(scores)
        enps = round(100 * (promoters - detractors) / n) if n else 0
        dist = {"promoters (9-10)": promoters, "passives (7-8)": passives, "detractors (0-6)": detractors}

        # segment breakdown
        seg_map = {}
        for seg, s in zip(segments, scores):
            seg_map.setdefault(seg, []).append(s)
        segs_out = []
        for seg, ss in sorted(seg_map.items()):
            d = sum(1 for x in ss if x < 7); p = sum(1 for x in ss if x >= 9)
            e = round(100 * (p - d) / len(ss))
            segs_out.append({"segment": seg, "n": len(ss), "avg": round(sum(ss)/len(ss), 1),
                             "enps": e, "flag": "investigate" if e < enps - 15 else "ok"})

        # comment themes with sentiment
        themes = {}
        for c in comments:
            low = c.lower()
            words = set(re.findall(r"[a-z']+", low))
            neg_hits = words & NEG
            pos_hits = words & POS
            for theme, kws in THEME_MAP.items():
                if any(k in low for k in kws):
                    t = themes.setdefault(theme, {"count": 0, "neg": 0, "pos": 0, "sample": c[:100]})
                    t["count"] += 1
                    if neg_hits and not pos_hits:
                        t["neg"] += 1
                    elif pos_hits and not neg_hits:
                        t["pos"] += 1
                    elif not t["sample"]:
                        t["sample"] = c[:100]

        themes_out = sorted(
            ({"theme": k, **v, "severity": "high" if v["neg"] >= max(2, v["count"] * 0.5) else "medium" if v["neg"] else "low"}
             for k, v in themes.items()),
            key=lambda t: (-t["neg"], -t["count"]))

        interventions = []
        for t in themes_out[:3]:
            if t["theme"] == "workload" and t["neg"]:
                interventions.append("Workload: run a 2-week meeting audit + WIP limits; publish what the team STOPPED doing.")
            elif t["theme"] == "clarity" and t["neg"]:
                interventions.append("Clarity: restate strategy in one page + a live priorities doc; every project names its 'why now'.")
            elif t["theme"] == "comp_fairness" and t["neg"]:
                interventions.append("Comp: publish bands + correction process; silence reads as unfairness even when pay is fine.")
            elif t["theme"] == "autonomy_trust" and t["neg"]:
                interventions.append("Autonomy: convert one approval gate per team into a review-after; measure nothing breaks.")
            elif t["theme"] == "leadership" and t["neg"]:
                interventions.append("Leadership: skip-level listening tour (questions asked, answers published verbatim).")
            elif t["theme"] == "growth" and t["neg"]:
                interventions.append("Growth: every person gets one named growth project per quarter, reviewed in 1:1s.")
        if not interventions:
            interventions.append("No negative themes dominate — protect what works: name the mechanisms explicitly so they survive leadership change.")

        caveats = []
        if n < 10:
            caveats.append(f"n={n} is below statistical usefulness — treat as anecdotes, not signal.")
        if n and len(comments) / n < 0.5:
            caveats.append("Under half of respondents commented — comment themes may not represent the score distribution.")
        low_seg = [s for s in segs_out if s["flag"] != "ok"]
        if low_seg:
            caveats.append(f"Segment gap: {', '.join(s['segment'] + f' (eNPS {s['enps']})' for s in low_seg)} — "
                           "company-wide eNPS hides them.")
        if not caveats:
            caveats.append("Response size adequate; check anonymity guarantees before trusting trend deltas.")

        verdict = f"n={n} | eNPS {enps} | {len(themes_out)} themes | {len(low_seg)} flagged segment(s)"
        return PulseReport(n, enps, dist, segs_out, themes_out, interventions, caveats, verdict)

    @staticmethod
    def format_report(r: PulseReport) -> str:
        out = ["=" * 62, "CULTURE PULSE AGENT — REPORT", "=" * 62, r.verdict, "-" * 62,
               "Distribution: " + ", ".join(f"{k}: {v}" for k, v in r.distribution.items()),
               "-" * 62, "Segments:"]
        out += [f"  {s['segment'][:20]:20} n={s['n']:<3} avg={s['avg']:<5} eNPS={s['enps']:<5} [{s['flag']}]" for s in r.segments]
        if r.themes:
            out += ["-" * 62, "Comment themes:"]
            for t in r.themes:
                out.append(f"  {t['theme']:16} vol={t['count']:<3} neg={t['neg']:<3} pos={t['pos']:<3} [{t['severity']}]")
                out.append(f"      sample: \"{t['sample'][:90]}\"")
        out += ["-" * 62, "Interventions (map to detractor themes):"]
        out += [f"  {i}. {x}" for i, x in enumerate(r.interventions, 1)]
        out += ["-" * 62, "Caveats:"] + [f"  ! {c}" for c in r.caveats]
        out += ["=" * 62, "Rule: re-run the SAME questions next pulse — trend beats snapshot every time."]
        return "\n".join(out)
