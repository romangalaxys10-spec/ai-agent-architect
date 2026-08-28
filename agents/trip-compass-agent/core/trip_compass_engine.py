"""
Trip Compass Agent Engine.
Builds day-by-day itineraries with pacing rules, geographic clustering,
budget allocation, packing list, and contingency plans.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class DayPlan:
    day: int
    anchor: str
    blocks: List[str] = field(default_factory=list)
    intensity: str = "balanced"

@dataclass
class Itinerary:
    destination: str
    days: List[DayPlan] = field(default_factory=list)
    budget_split: dict = field(default_factory=dict)
    packing: List[str] = field(default_factory=list)
    contingencies: List[str] = field(default_factory=list)
    pre_travel: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    verdict: str = ""

ACTIVITY_BANK = {
    "culture": ["main museum (book first-entry slot)", "historic quarter walking loop", "local market + food stalls"],
    "food": ["neighborhood bistro lunch", "street-food crawl (3 stops)", "cooking class or food tour"],
    "walking": ["old-town self-guided walk", "waterfront/promenade stroll", "park + viewpoint hike"],
    "nature": ["signature park/garden", "half-day nature escape", "sunset viewpoint"],
    "beach": ["beach morning (before crowds)", "coastal walk", "sunset swim"],
    "nightlife": ["live music venue", "rooftop bar", "evening plaza hang"],
    "shopping": ["artisan district", "covered market", "design/flea market"],
    "history": ["landmark cathedral/temple", "ruins/fort", "history museum"],
    "family": ["interactive museum", "zoo/aquarium", "playground park"],
    "adventure": ["guided hike/bike rental", "water sport session", "climbing/trek outing"],
}

PACE_RULES = {
    "relaxed": {"anchors": 1, "blocks": 2, "rest": "afternoon siesta block every day"},
    "balanced": {"anchors": 2, "blocks": 3, "rest": "one light half-day after every 2 full days"},
    "intense": {"anchors": 3, "blocks": 4, "rest": "one recovery evening per 3 days — schedule it or crash on day 4"},
}

class TripCompassEngine:
    """The itinerary is a pacing problem wearing a geography costume."""

    @classmethod
    def plan(cls, destination: str, days: int, preferences: List[str], budget: float,
             pace: str = "balanced") -> Itinerary:
        days = max(1, min(days, 21))
        prefs = preferences or ["culture", "food", "walking"]
        rule = PACE_RULES[pace]

        # rotate activities across days, avoid two heavy days in a row
        day_plans = []
        pool = []
        for p in prefs:
            pool.extend(ACTIVITY_BANK.get(p.lower().strip(), ACTIVITY_BANK["culture"]))
        if not pool:
            pool = ACTIVITY_BANK["culture"] + ACTIVITY_BANK["food"]

        i = 0
        for d in range(1, days + 1):
            is_arrival = d == 1
            is_departure = d == days and days > 1
            anchors = 1 if (is_arrival or is_departure) else rule["anchors"]

            blocks = []
            if is_arrival:
                blocks.append("morning: arrive, drop bags, orient (walk one loop near the hotel — jet lag cure)")
            if is_departure:
                blocks.append("morning: buffer + souvenir pass; depart with margin for transit delays")
            while len(blocks) < rule["blocks"]:
                act = pool[i % len(pool)]
                i += 1
                tod = "afternoon" if len(blocks) == 0 and not is_arrival else \
                      "afternoon" if "morning" not in blocks[-1][:6] and blocks else "morning"
                blocks.append(f"{tod}: {act}")
            if d % 2 == 0 and pace != "intense":
                blocks.append("late: " + rule["rest"])
            day_plans.append(DayPlan(d, pool[(d - 1) % len(pool)] if pool else "explore", blocks,
                                     pace if (is_arrival or is_departure) else "full"))

        split = {
            "stay": round(budget * 0.35, 0),
            "food": round(budget * 0.25, 0),
            "activities": round(budget * 0.20, 0),
            "transit": round(budget * 0.12, 0),
            "buffer": round(budget * 0.08, 0),
        }

        packing = [
            "documents: passport/ID + 2 printed bookings + 1 offline map screenshot",
            "power: universal adapter + power bank (navigation kills phones)",
            "walking: the comfortable shoes — you will do 15k+ steps/day at this pace",
            "layer: one rain-proof layer regardless of forecast",
        ]
        for p in prefs:
            if p.lower() in ("beach", "nature", "adventure"):
                packing.append(f"{p.lower()} kit: sunscreen, water bottle, quick-dry clothing")
        if days >= 5:
            packing.append("laundry plan: pack for 4 days and wash once — bags stay carry-on")

        contingencies = [
            "Rain day: swap the walking/outdoor day with the museum day — keep the swap cost-free by booking refundable entries.",
            "Strike/transit outage: pre-identify one walkable cluster near your stay as a fallback day.",
            "Illness: designate Day-3 as the compressible day (drop it without losing anchors).",
        ]

        pre_travel = [
            "Book: 1st-choice anchor per day (refundable), airport transfer, first night's stay.",
            "Check: visa/entry rules, roaming/eSIM, emergency number + embassy contact.",
            "Copy: itinerary + docs to a trusted contact; set a daily check-in if solo.",
        ]

        warnings = []
        if days <= 2 and len(prefs) >= 4:
            warnings.append(f"{days} day(s) cannot honor {len(prefs)} interests — pick the top 2 or the trip becomes a checklist.")
        if budget / days < 60:
            warnings.append(f"Budget works out to {budget/days:.0f}/day — tight in most cities; raise the buffer or plan picnics.")
        if pace == "intense" and days >= 5:
            warnings.append("Intense pace for 5+ days usually collapses — the recovery evenings are non-negotiable.")

        verdict = (f"{days}-day {pace} itinerary for {destination} | {len(prefs)} interest tracks | "
                   f"budget {budget:.0f} ({budget/days:.0f}/day)")
        return Itinerary(destination, day_plans, split, packing, contingencies, pre_travel,
                         warnings, verdict)

    @staticmethod
    def format_itinerary(it: Itinerary) -> str:
        out = ["=" * 62, "TRIP COMPASS AGENT — ITINERARY", "=" * 62, it.verdict, "-" * 62]
        for d in it.days:
            out.append(f"  Day {d.day}: anchor = {d.anchor[:46]}")
            out += [f"      {b}" for b in d.blocks]
        out += ["-" * 62, "Budget split:"]
        out += [f"  {k:10} {v:>8.0f}" for k, v in it.budget_split.items()]
        out += [f"  {'TOTAL':10} {sum(it.budget_split.values()):>8.0f}"]
        out += ["-" * 62, "Packing:"]
        out += [f"  * {p}" for p in it.packing]
        out += ["-" * 62, "Contingencies:"] + [f"  - {c}" for c in it.contingencies]
        out += ["-" * 62, "Pre-travel checklist:"] + [f"  - {p}" for p in it.pre_travel]
        if it.warnings:
            out += ["-" * 62, "Warnings:"] + [f"  ! {w}" for w in it.warnings]
        out.append("=" * 62)
        return "\n".join(out)
