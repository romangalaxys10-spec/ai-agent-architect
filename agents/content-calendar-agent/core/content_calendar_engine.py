"""
Content Calendar Agent Engine.
Generates multi-week editorial calendars with format mix ratios,
hooks, channel adaptations, KPI targets, and a repurposing map.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class CalendarEntry:
    week: int
    day: str
    channel: str
    format: str
    hook: str
    kpi: str

@dataclass
class Calendar:
    entries: List[CalendarEntry] = field(default_factory=list)
    mix: dict = field(default_factory=dict)
    pillars: List[str] = field(default_factory=list)
    repurpose_map: List[str] = field(default_factory=list)
    kpi_targets: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    verdict: str = ""

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
FORMAT_MIX = [("educational deep-dive", 0.40), ("practical how-to", 0.25),
              ("opinion/data take", 0.20), ("community/promo", 0.15)]

HOOKS = {
    "educational deep-dive": [
        "The {topic} teardown: what actually happens under the hood",
        "{topic}: everything nobody documented (with receipts)",
        "We stress-tested {topic} until it broke — full postmortem",
    ],
    "practical how-to": [
        "{topic} in 15 minutes: the copy-paste path",
        "The {topic} checklist we run before every release",
        "Fix {topic} the boring way (that always works)",
    ],
    "opinion/data take": [
        "Hot take: everyone does {topic} backwards",
        "The data says {topic} advice is 80% folklore",
        "{topic}: the tradeoff nobody mentions",
    ],
    "community/promo": [
        "You asked about {topic} — community answers, compiled",
        "Show us your {topic} setup: 5 submissions dissected",
        "What we shipped this month (and what {topic} broke)",
    ],
}

CHANNEL_FIT = {
    "blog": "1,400+ words, SEO skeleton, one original chart",
    "linkedin": "200-300 words, first line is the whole argument, no external link in body",
    "x": "thread of 5-9 tweets, hook tweet stands alone, numbers in 2 of the tweets",
    "newsletter": "subject line <45 chars, one big idea, one CTA",
    "youtube": "8-min script, 15s hook, retention beat every 90s",
    "instagram": "carousel of 6-8 slides, slide 1 = claim, last = CTA",
}

class ContentCalendarEngine:
    """Consistency is a system, not a mood — the calendar is the system."""

    @classmethod
    def generate(cls, goal: str, audience: str = "technical practitioners",
                 channels: List[str] = None, weeks: int = 4) -> Calendar:
        channels = channels or ["blog", "linkedin", "x"]
        weeks = max(1, min(weeks, 12))
        topic = goal

        entries = []
        hook_i = 0
        for w in range(1, weeks + 1):
            for d_idx, day in enumerate(DAYS[:max(3, min(5, len(channels) + 2))]):
                # pick format by mix ratios across the week
                roll = (d_idx / max(1, len(DAYS[:5])))
                fmt = FORMAT_MIX[0][0]
                acc = 0.0
                for name, share in FORMAT_MIX:
                    acc += share
                    if roll < acc:
                        fmt = name
                        break
                if w % 4 == 0 and day == "Fri":
                    fmt = "community/promo"  # monthly ship-roundup slot
                channel = channels[(d_idx + w) % len(channels)]
                hook_tpl = HOOKS[fmt][hook_i % len(HOOKS[fmt])]
                hook_i += 1
                kpi = {"educational deep-dive": "avg read time > 3 min; 3+ bookmarks",
                       "practical how-to": "copy events / repo stars; comments asking follow-ups",
                       "opinion/data take": "reply rate; quote-tweets (both agree and disagree)",
                       "community/promo": "DMs/replies; CTR to product page < 2% (promo fatigue guard)"}[fmt]
                entries.append(CalendarEntry(w, day, channel, fmt, hook_tpl.format(topic=topic), kpi))

        mix = {name: round(share, 2) for name, share in FORMAT_MIX}

        pillars = [
            f"Pillar 1 — teach: {topic} fundamentals, own the search intent",
            f"Pillar 2 — prove: original data/benchmarks about {topic}",
            f"Pillar 3 — take sides: defensible opinions on {topic} tradeoffs",
        ]

        repurpose = [
            "blog deep-dive -> 3-x thread + 1 LinkedIn post + newsletter section (one source, four surfaces)",
            "any original chart -> standalone post (charts outperform prose on reach)",
            "best-performing thread -> next month's deep-dive outline (demand-validated)",
            "community answers -> FAQ page (compounds SEO + reduces support load)",
        ]

        kpis = [
            "Leading: saves/bookmarks per post (intent to return) — not impressions.",
            "Lagging: search rank for the pillar term; subscriber growth per 4 weeks.",
            "Health: promo share never exceeds 20% of the calendar or reach decays.",
        ]

        warnings = []
        if weeks >= 4 and len(channels) <= 1:
            warnings.append("Single channel for 4+ weeks: you are renting one audience; add a second surface.")
        if "x" in channels and "blog" not in channels:
            warnings.append("Threads without a home base: put the canonical version on a channel you own.")
        if not warnings:
            warnings.append("Mix healthy: 65% give-value formats before any ask.")

        verdict = f"{weeks} weeks x {len(DAYS[:5])} slots | {len(entries)} entries | {len(channels)} channels"
        return Calendar(entries, mix, pillars, repurpose, kpis, warnings, verdict)

    @staticmethod
    def format_calendar(c: Calendar) -> str:
        out = ["=" * 62, "CONTENT CALENDAR AGENT — CALENDAR", "=" * 62, c.verdict, "-" * 62,
               "Format mix: " + ", ".join(f"{k} {v:.0%}" for k, v in c.mix.items()),
               "-" * 62]
        cur_week = 0
        for e in c.entries:
            if e.week != cur_week:
                cur_week = e.week
                out.append(f"  ——— Week {e.week} ———")
            out.append(f"  {e.day} [{e.channel:9}] {e.format:24} {e.hook[:46]}")
        out += ["-" * 62, "Content pillars:"]
        out += [f"  * {p}" for p in c.pillars]
        out += ["-" * 62, "Repurposing map:"]
        out += [f"  * {r}" for r in c.repurpose_map]
        out += ["-" * 62, "KPI targets:"]
        out += [f"  * {k}" for k in c.kpi_targets]
        if c.warnings:
            out += ["-" * 62, "Warnings:"] + [f"  ! {w}" for w in c.warnings]
        out.append("=" * 62)
        return "\n".join(out)
