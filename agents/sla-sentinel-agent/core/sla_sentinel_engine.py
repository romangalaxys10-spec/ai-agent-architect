"""
SLA Sentinel Agent Engine.
Projects SLA breach risk per ticket from age velocity and orders the queue
by preventable-breach value.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class TicketRisk:
    ticket_id: str
    priority: str
    sla_hours: float
    age_hours: float
    hours_remaining: float
    breach_probability: float
    recommended_action: str

@dataclass
class SLAProjection:
    total: int
    at_risk: List[TicketRisk] = field(default_factory=list)
    breached: List[str] = field(default_factory=list)
    intervention_order: List[str] = field(default_factory=list)
    capacity_note: str = ""
    verdict: str = ""

DEFAULT_SLA = {"P1": 4, "P2": 24, "P3": 72, "P4": 168}

ACTIONS = {
    (0.85, 1.01): "BREACHED/UNRECOVERABLE — send proactive apology + root-cause commitment; log postmortem.",
    (0.6, 0.85): "CRITICAL — pull a senior agent off P3 queue; draft response now, resolve or set expectations.",
    (0.35, 0.6): "HIGH — bundle with duplicate reports; first-touch template + ETA promise.",
    (0.15, 0.35): "MEDIUM — queue behind criticals; batch with the daily P2 sweep.",
    (0.0, 0.15): "LOW — normal queue order; add to the self-service deflection backlog.",
}

class SLASentinelEngine:
    """Breaches are visible hours in advance — this is the early-warning radar."""

    @classmethod
    def project(cls, tickets: List[dict]) -> SLAProjection:
        risks: List[TicketRisk] = []
        breached = []
        for t in tickets:
            tid = str(t.get("id", t.get("ticket", "?")))
            pri = str(t.get("priority", "P3")).upper()
            sla = float(t.get("sla_hours", DEFAULT_SLA.get(pri, 48)))
            age = float(t.get("age_hours", 0))
            waiting = bool(t.get("awaiting_customer", False))
            contact_count = float(t.get("customer_contacts", 1))

            if waiting:
                age = age * 0.4  # customer-held time typically excluded from SLA

            remaining = sla - age
            # velocity: each extra customer contact compresses effective time
            pressure = 1.0 + 0.15 * max(0, contact_count - 1)
            if remaining <= 0:
                prob = 1.0
            else:
                prob = min(0.98, max(0.02, (age / sla) * pressure))

            action = ""
            for (lo, hi), act in ACTIONS.items():
                if lo <= prob < hi:
                    action = act
                    break

            risks.append(TicketRisk(tid, pri, sla, age, round(remaining, 1), round(prob, 2), action))
            if remaining <= 0:
                breached.append(tid)

        at_risk = sorted((r for r in risks if r.breach_probability >= 0.35 and r.hours_remaining > 0),
                         key=lambda r: (-r.breach_probability, r.hours_remaining))

        order = []
        for r in at_risk[:8]:
            order.append(f"{r.ticket_id} [{r.priority}] p={r.breach_probability:.0%} "
                         f"{r.hours_remaining}h left -> {r.recommended_action}")

        n_p1_p2 = len([r for r in risks if r.priority in ("P1", "P2")])
        if n_p1_p2 >= 5:
            capacity = f"Queue overloaded: {n_p1_p2} P1/P2 live. Request surge staffing or enable macro deflection."
        elif len(at_risk) >= 3:
            capacity = f"{len(at_risk)} tickets trending toward breach — clear them before the daily sweep ends."
        else:
            capacity = "Capacity is adequate; no surge actions needed."

        verdict = (f"{len(tickets)} tickets | {len(breached)} already breached | "
                   f"{len(at_risk)} at risk (p>=35%)")
        return SLAProjection(len(tickets), at_risk, breached, order, capacity, verdict)

    @staticmethod
    def format_projection(p: SLAProjection) -> str:
        out = ["=" * 62, "SLA SENTINEL AGENT — PROJECTION", "=" * 62, p.verdict, "-" * 62,
               p.capacity_note]
        if p.breached:
            out += ["Already breached (recovery comms needed): " + ", ".join(p.breached[:10])]
        out += ["-" * 62, "Intervention order (highest breach probability first):"]
        if p.intervention_order:
            out += [f"  {i}. {o}" for i, o in enumerate(p.intervention_order, 1)]
        else:
            out.append("  none — no ticket crosses the 35% risk threshold")
        out += ["-" * 62,
                "Policy: P1 breach requires an incident-style timeline; P2/P3 feed the weekly SLA review.",
                "=" * 62]
        return "\n".join(out)
