"""
Competitor Radar Agent Engine.
Classifies competitor moves, scores threat, updates battlecards,
and prescribes counter-plays per event.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class RadarEvent:
    raw: str
    competitor: str
    category: str
    threat: str
    threat_score: float
    counter_play: str
    battlecard_delta: str

@dataclass
class RadarReport:
    events: List[RadarEvent] = field(default_factory=list)
    category_counts: dict = field(default_factory=dict)
    top_threats: List[str] = field(default_factory=list)
    battlecard_updates: List[str] = field(default_factory=list)
    cadence: str = ""
    verdict: str = ""

CATEGORY_RULES = [
    ("pricing", [r"\b(cuts?|drops?|lowers?|reduces?)\s+(prices?|pricing)", r"prices? (?:cut|change|war)",
                 r"free tier", r"pricing page", r"new plans?\b"], 0.9),
    ("feature_parity", [r"launch(es|ed)? \w+", r"new feature", r"now supports", r"GA\b", r"releases?\b"], 0.6),
    ("partnership", [r"partner(ship)?", r"integrat(es|ion)", r"reseller", r"OEM", r"co-sell"], 0.7),
    ("funding", [r"raises?", r"Series [ABC]", r"\$\d+M", r"funding", r"valuation"], 0.5),
    ("pr_stunt", [r"announces?", r"report", r"survey", r"benchmark", r"claimed"], 0.3),
    ("hiring", [r"hires?", r"joins", r"VP of", r"new C[ETOF]O"], 0.4),
    ("outage", [r"outage", r"down", r"breach", r"incident", r"downtime"], 0.2),
]

COUNTER_PLAYS = {
    "pricing": "Same-day counter: publish TCO comparison; remind buyers switching costs recur twice (migration + retraining).",
    "feature_parity": "Don't chase feature-for-feature: demo the adjacent workflow their feature breaks; contrast depth vs checkbox.",
    "partnership": "Accelerate your own partner motion with the SAME partner if non-exclusive; else deepen exclusives you hold.",
    "funding": "Expect pricing aggression + marketing blitz in 2 quarters; lock 2-year contracts with key accounts NOW.",
    "pr_stunt": "Publish your own primary data within 72h while their claim is unchallenged; own the narrative window.",
    "hiring": "Their new exec signals next-year roadmap; adjust your roadmap comms to pre-empt that exact area.",
    "outage": "Same-day empathetic outreach to their shared accounts (never gloating); reliability switch-kit + migration offer.",
}

class CompetitorRadarEngine:
    """Watch the field, not the scoreboard — every move has a counter."""

    @classmethod
    def analyze(cls, event_lines: List[str], our_position: str = "") -> RadarReport:
        events: List[RadarEvent] = []
        for line in event_lines:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                date, competitor, desc = parts[0], parts[1], parts[2]
            elif len(parts) == 2:
                date, competitor, desc = "-", parts[0], parts[1]
            else:
                date, competitor, desc = "-", "unknown", parts[0] if parts else line

            low = desc.lower()
            category, base = "pr_stunt", 0.3
            for cat, pats, w in CATEGORY_RULES:
                if any(re.search(p, low) for p in pats):
                    category, base = cat, w
                    break

            # proximity to our differentiators raises the threat
            proximity = 0.0
            our_words = [w for w in re.findall(r"[a-z]{4,}", our_position.lower())]
            if our_words:
                overlap = sum(1 for w in our_words if w in low)
                proximity = min(0.4, 0.08 * overlap)

            multiple_hits = sum(1 for _, pats, _ in CATEGORY_RULES if any(re.search(p, low) for p in pats))
            score = round(min(1.0, base + proximity + 0.1 * (multiple_hits - 1)), 2)
            threat = "high" if score >= 0.75 else "medium" if score >= 0.5 else "low"

            events.append(RadarEvent(
                raw=line.strip()[:100], competitor=competitor, category=category,
                threat=threat, threat_score=score,
                counter_play=COUNTER_PLAYS[category],
                battlecard_delta=f"[{category}] {competitor}: update '{desc[:60]}' + our counter: "
                                 f"{COUNTER_PLAYS[category][:70]}"))

        counts = {}
        for e in events:
            counts[e.category] = counts.get(e.category, 0) + 1

        top = sorted(events, key=lambda e: -e.threat_score)[:5]
        top_out = [f"{e.competitor} ({e.category}, threat {e.threat_score:.0%}): {e.counter_play}" for e in top]

        updates = []
        seen_cats = set()
        for e in sorted(events, key=lambda e: -e.threat_score):
            if e.category not in seen_cats:
                updates.append(e.battlecard_delta)
                seen_cats.add(e.category)
            if len(updates) >= 5:
                break

        cadence = ("DAILY scan this week (3+ high-threat events), then weekly" if
                   len([e for e in events if e.threat == "high"]) >= 3 else
                   "Weekly scan + monthly deep-dive on the top threat category")
        verdict = f"{len(events)} events | top category: {max(counts, key=counts.get) if counts else '-'}"
        return RadarReport(events, counts, top_out, updates, cadence, verdict)

    @staticmethod
    def format_report(r: RadarReport) -> str:
        out = ["=" * 62, "COMPETITOR RADAR AGENT — REPORT", "=" * 62, r.verdict, "-" * 62,
               "Category mix: " + (", ".join(f"{k}={v}" for k, v in r.category_counts.items()) or "none"),
               "-" * 62, "Events:"]
        for e in r.events[:10]:
            out.append(f"  [{e.threat:6} {e.threat_score:.0%}] {e.competitor:16} {e.category:14} {e.raw[:60]}")
        out += ["-" * 62, "Top threats + counter-plays:"]
        out += [f"  {i}. {t}" for i, t in enumerate(r.top_threats, 1)] or ["  none"]
        out += ["-" * 62, "Battlecard updates:"]
        out += [f"  * {u}" for u in r.battlecard_updates]
        out += ["-" * 62, f"Scan cadence: {r.cadence}", "=" * 62]
        return "\n".join(out)
