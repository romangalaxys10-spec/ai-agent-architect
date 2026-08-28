"""
Ticket Router Agent Engine.
Classifies support tickets by intent, extracts entities, routes to queues
with SLA clocks, and suggests matching macros.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class RoutingDecision:
    category: str
    confidence: float
    priority: str
    sla_hours: int
    queue: str
    entities: dict = field(default_factory=dict)
    sentiment: str = "neutral"
    suggested_macro: str = ""
    escalation: str = "none"
    verdict: str = ""

CATEGORY_RULES = [
    ("billing", 3, ["refund", "charge", "invoice", "payment", "billing", "subscription", "price", "overcharge"], 24, "Billing Operations"),
    ("security", 4, ["hacked", "breach", "unauthorized", "phishing", "stolen", "credential", "2fa", "leak"], 4, "Security On-Call"),
    ("outage", 4, ["down", "outage", "cannot access", "error 500", "everyone", "all users", "unavailable", "site is down"], 4, "Incident Response"),
    ("bug", 3, ["bug", "broken", "not working", "fails", "crashes", "incorrect", "wrong value", "regression"], 48, "Engineering Triage"),
    ("how_to", 1, ["how do i", "how to", "where can i", "is it possible", "can i", "documentation", "tutorial", "setup"], 72, "Self-Service / Tier 1"),
    ("feature", 2, ["feature request", "would be great", "any chance you could add", "roadmap", "enhancement", "would love"], 168, "Product Feedback"),
    ("abuse", 3, ["spam", "harassment", "abuse", "report user", "illegal", "impersonat"], 24, "Trust & Safety"),
]

ANGER_WORDS = ["unacceptable", "furious", "ridiculous", "cancel my account", "cancel our account",
               "last straw", "lawyer", "chargeback", "better business bureau", "switching to"]
PRAISE_WORDS = ["love", "great job", "thank you", "amazing", "excellent", "appreciate"]

class TicketRouterEngine:
    """Route on evidence (matched keywords + entity count), never on vibes."""

    @classmethod
    def route(cls, ticket_text: str) -> RoutingDecision:
        low = ticket_text.lower()

        best_cat, best_score, sla, queue = "general", 0, 48, "General Support"
        for cat, weight, keywords, cat_sla, cat_queue in CATEGORY_RULES:
            score = sum(1 for kw in keywords if kw in low)
            if score:
                adj = score * weight
                if adj > best_score:
                    best_cat, best_score, sla, queue = cat, adj, cat_sla, cat_queue

        matches = sum(1 for _, weight, kws, _, _ in CATEGORY_RULES for kw in kws if kw in low)
        confidence = round(min(0.95, 0.3 + 0.15 * best_score + 0.03 * matches), 2) if best_score else 0.25

        anger = sum(1 for w in ANGER_WORDS if w in low)
        praise = sum(1 for w in PRAISE_WORDS if w in low)
        sentiment = "angry" if anger >= 1 else "positive" if praise >= 1 else "neutral"

        entities = {
            "order_ids": re.findall(r"\b(?:order|ord)\s*#?\s*([A-Z0-9\-]{4,})\b", ticket_text, re.I),
            "emails": re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", ticket_text),
            "amounts": re.findall(r"(?:\$|€|£)\s?\d+(?:\.\d{2})?", ticket_text),
            "versions": re.findall(r"\bv?(\d+\.\d+(?:\.\d+)?)\b", ticket_text),
            "urls": re.findall(r"https?://\S+", ticket_text),
        }

        priority = "P1" if best_cat in ("security", "outage") else \
                   "P2" if anger >= 2 or best_cat == "billing" else \
                   "P3" if best_score else "P4"
        if sentiment == "angry" and priority == "P3":
            priority = "P2"

        macros = {
            "billing": "billing_refund_policy_v3 + attach last-3-invoices snippet",
            "security": "sec_incident_kickoff + force-reset checklist + preserve-evidence note",
            "outage": "status_page_link + subscribe-to-updates + incident-comms template",
            "bug": "bug_report_template (env, steps, expected/actual) + known-issues link",
            "how_to": "docs_search_deep_link + 2 most-relevant KB articles",
            "feature": "feature_request_capture + roadmap_transparency blurb",
            "abuse": "t&s_report_intake + evidence-preservation steps",
            "general": "greeting + clarify_intent + docs_search",
        }

        escalation = "none"
        if anger >= 2:
            escalation = "attach account-health note; CSM ping if account tier >= Growth"
        if best_cat == "security" and priority == "P1":
            escalation = "page security on-call immediately; do NOT auto-reply"

        verdict = f"ROUTE -> {queue} | {best_cat} ({confidence:.0%}) | {priority} | SLA {sla}h"
        return RoutingDecision(best_cat, confidence, priority, sla, queue,
                               entities, sentiment, macros[best_cat], escalation, verdict)

    @staticmethod
    def format_decision(d: RoutingDecision) -> str:
        out = ["=" * 62, "TICKET ROUTER AGENT — DECISION", "=" * 62, d.verdict, "-" * 62,
               f"Category   : {d.category} (confidence {d.confidence:.0%})",
               f"Queue      : {d.queue}",
               f"Priority   : {d.priority} | SLA: respond within {d.sla_hours}h",
               f"Sentiment  : {d.sentiment}",
               f"Macro      : {d.suggested_macro}"]
        ents = {k: v for k, v in d.entities.items() if v}
        if ents:
            out += ["-" * 62, "Extracted entities:"]
            out += [f"  {k}: {', '.join(map(str, v[:4]))}" for k, v in ents.items()]
        if d.escalation != "none":
            out += ["-" * 62, "ESCALATION:", f"  {d.escalation}"]
        out.append("=" * 62)
        return "\n".join(out)
