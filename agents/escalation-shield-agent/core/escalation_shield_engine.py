"""
Escalation Shield Agent Engine.
Computes churn-risk from account signals and prescribes the save play
before the customer escalates or churns.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class EscalationAssessment:
    account: str
    churn_score: float
    tier: str
    evidence: List[str] = field(default_factory=list)
    save_play: List[str] = field(default_factory=list)
    concessions: List[str] = field(default_factory=list)
    follow_up_cadence: str = ""
    verdict: str = ""

class EscalationShieldEngine:
    """Save the account before the customer writes the goodbye email."""

    @classmethod
    def assess(cls, signals: dict) -> EscalationAssessment:
        account = str(signals.get("account", signals.get("name", "unknown-account")))
        tickets_30d = float(signals.get("tickets_30d", 0))
        tickets_prev_30d = float(signals.get("tickets_prev_30d", tickets_30d or 1))
        open_tickets = float(signals.get("open_tickets", 0))
        oldest_open_days = float(signals.get("oldest_open_days", 0))
        sentiment = str(signals.get("sentiment", "neutral")).lower()
        plan = str(signals.get("plan", "standard")).lower()
        tenure_months = float(signals.get("tenure_months", 12))
        mrr = float(signals.get("mrr", 0))
        usage_drop_pct = float(signals.get("usage_drop_pct", 0))
        champion_departed = bool(signals.get("champion_departed", False))
        renewal_days = float(signals.get("renewal_days", 180))

        evidence, score = [], 0.0

        # ticket velocity
        if tickets_30d > tickets_prev_30d * 1.5 and tickets_30d >= 4:
            score += 18; evidence.append(f"Ticket velocity up: {tickets_30d:.0f} in 30d vs {tickets_prev_30d:.0f} prior")
        elif tickets_30d >= 8:
            score += 10; evidence.append(f"High ticket volume: {tickets_30d:.0f}/30d")
        if open_tickets >= 4:
            score += 10; evidence.append(f"{open_tickets:.0f} tickets still open")
        if oldest_open_days >= 7:
            score += 12; evidence.append(f"Oldest open ticket aging {oldest_open_days:.0f} days")
        elif oldest_open_days >= 3:
            score += 6; evidence.append(f"Oldest open ticket aging {oldest_open_days:.0f} days")

        if sentiment in ("angry", "furious", "negative"):
            score += 15; evidence.append(f"Reported sentiment: {sentiment}")
        elif sentiment == "frustrated":
            score += 9; evidence.append("Reported sentiment: frustrated")

        if usage_drop_pct >= 40:
            score += 20; evidence.append(f"Usage down {usage_drop_pct:.0f}% — product value not landing")
        elif usage_drop_pct >= 20:
            score += 10; evidence.append(f"Usage down {usage_drop_pct:.0f}%")

        if champion_departed:
            score += 15; evidence.append("Internal champion departed — re-establish a new one")
        if renewal_days <= 60 and renewal_days > 0:
            score += 10; evidence.append(f"Renewal in {renewal_days:.0f} days")
        if tenure_months <= 3:
            score += 5; evidence.append("Young account — onboarding may have failed")
        if plan in ("enterprise", "growth") and score >= 25:
            score += 5; evidence.append(f"High-value {plan} plan (MRR {mrr:.0f})")

        score = min(100.0, score)
        tier = ("CRITICAL — exec sponsor must engage this week" if score >= 60 else
                "AT_RISK — CSM-led save play now" if score >= 35 else
                "WATCH — monitor in weekly account review" if score >= 15 else "HEALTHY")

        play, concessions = [], []
        if score >= 35:
            play.append("Call within 24h — human voice, not email; acknowledge specifics from the evidence list.")
        if usage_drop_pct >= 20:
            play.append("Schedule a value-realization session: map their workflows to the 3 features they abandoned.")
        if oldest_open_days >= 7 or open_tickets >= 4:
            play.append("Assign a single-named engineer to burn down the open-ticket backlog; daily updates until clear.")
        if champion_departed:
            play.append("Book an onboarding-refresh for the new stakeholder; re-run success criteria.")
        if renewal_days <= 60:
            play.append("Trigger early-renewal conversation with roadmap co-commitments in writing.")
        if not play:
            play.append("No intervention needed — capture what IS working into the account's success plan.")

        if score >= 60:
            concessions = ["Service credits tied to the specific SLA misses (not blanket discount)",
                           "Named CSM + monthly exec business review for 2 quarters"]
        elif score >= 35:
            concessions = ["Free training workshop for the team",
                           "Priority support tier trial (30 days)"]

        cadence = ("daily until score < 35, then weekly" if score >= 60 else
                   "weekly for 4 weeks" if score >= 35 else "monthly account review")

        verdict = f"CHURN_RISK {score:.0f}/100 | {tier.split(' — ')[0]}"
        return EscalationAssessment(account, score, tier, evidence, play, concessions, cadence, verdict)

    @staticmethod
    def format_assessment(a: EscalationAssessment) -> str:
        out = ["=" * 62, "ESCALATION SHIELD AGENT — ASSESSMENT", "=" * 62,
               f"Account: {a.account}", a.verdict, f"Tier: {a.tier}", "-" * 62, "Evidence:"]
        out += [f"  - {e}" for e in a.evidence] or ["  - no negative signals detected"]
        out += ["-" * 62, "Save play:"]
        out += [f"  {i}. {p}" for i, p in enumerate(a.save_play, 1)]
        if a.concessions:
            out += ["Concessions (pre-approved):"] + [f"  * {c}" for c in a.concessions]
        out += [f"Follow-up cadence: {a.follow_up_cadence}", "=" * 62]
        return "\n".join(out)
