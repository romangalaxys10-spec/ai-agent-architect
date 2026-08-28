"""
Email Triage Agent Engine.
Sorts an inbox into urgency quadrants, extracts asks/deadlines,
and drafts reply skeletons for the top items.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class EmailItem:
    idx: int
    sender: str
    subject: str
    quadrant: str          # Q1 do-now / Q2 schedule / Q3 delegate / Q4 read-later
    action: str
    ask: str
    deadline: str
    draft: str = ""

@dataclass
class TriagePlan:
    items: List[EmailItem] = field(default_factory=list)
    quadrant_counts: dict = field(default_factory=dict)
    time_blocks: List[str] = field(default_factory=list)
    verdict: str = ""

URGENT_WORDS = ["urgent", "asap", "immediately", "critical", "blocker", "down", "outage",
                "today", "eod", "by 5", "deadline"]
IMPORTANT_WORDS = ["decision", "approve", "approval", "contract", "offer", "board", "investor",
                   "renewal", "compliance", "legal", "escalation", "interview"]
DELEGATE_MARKERS = ["for your review", "fyi", "loop in", "cc", "update", "weekly", "newsletter",
                    "notification", "automated", "no-reply", "noreply"]
ASK_VERBS = ["need", "please", "can you", "review", "approve", "sign", "confirm", "send",
             "provide", "update", "decide", "book", "call"]
DEADLINE_RE = re.compile(r"\b(?:by|before|due)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday|eod|eow|tomorrow|today|\d{1,2}/\d{1,2}|\w+ \d{1,2}(?:st|nd|rd|th)?)", re.I)

class EmailTriageEngine:
    """The inbox is other people's priority list for your life — re-rank it."""

    @classmethod
    def triage(cls, emails: List[dict]) -> TriagePlan:
        items = []
        for i, em in enumerate(emails, 1):
            sender = str(em.get("from", em.get("sender", "unknown")))
            subject = str(em.get("subject", ""))
            body = str(em.get("body", "")) + " " + subject
            low = body.lower()

            urgent = sum(1 for w in URGENT_WORDS if w in low)
            important = sum(1 for w in IMPORTANT_WORDS if w in low)
            delegatable = sum(1 for w in DELEGATE_MARKERS if w in low)

            if urgent >= 1 and important >= 1:
                quadrant = "Q1_DO_NOW"
            elif important >= 1 and urgent == 0:
                quadrant = "Q2_SCHEDULE"
            elif urgent >= 1 and important == 0:
                quadrant = "Q1_DO_NOW" if urgent >= 2 else "Q3_DELEGATE_OR_QUICK_REPLY"
            else:
                quadrant = "Q4_READ_LATER" if delegatable >= 1 else "Q3_DELEGATE_OR_QUICK_REPLY"

            asks = [v for v in ASK_VERBS if v in low]
            ask = asks[0] if asks else ("respond to status" if "update" in low else "read")
            dm = DEADLINE_RE.search(body)
            deadline = dm.group(0) if dm else ("today" if "today" in low or "asap" in low else "-")

            if quadrant == "Q1_DO_NOW":
                action = "REPLY within the hour"
                draft = (f"Hi {sender.split('@')[0].title()},\n\n"
                         f"On it — handling now. You'll have an answer by {deadline if deadline != '-' else 'EOD'}.\n\n"
                         f"(quick confirm: {'/'.join(asks[:2])} — correct?)")
            elif quadrant == "Q2_SCHEDULE":
                action = "BOOK a 30-min decision slot"
                draft = (f"Hi {sender.split('@')[0].title()},\n\n"
                         f"This deserves real thought, not a hallway answer. "
                         f"Proposing 30 min tomorrow to decide: {subject[:50]}.\n"
                         f"Pre-read attached — one page, the decision framed as A/B/C.")
            elif quadrant == "Q3_DELEGATE_OR_QUICK_REPLY":
                action = "DELEGATE with context or 2-line reply"
                draft = (f"Forwarding to the owner with context: [1 line of why]. "
                         f"CC'ing you — no action needed unless you object by {deadline if deadline != '-' else 'Friday'}.")
            else:
                action = "BATCH: read in the Friday sweep"
                draft = ""

            items.append(EmailItem(i, sender, subject, quadrant, action, ask, deadline, draft))

        counts = {}
        for it in items:
            counts[it.quadrant] = counts.get(it.quadrant, 0) + 1

        q1 = [it for it in items if it.quadrant == "Q1_DO_NOW"]
        q2 = [it for it in items if it.quadrant == "Q2_SCHEDULE"]
        blocks = [
            f"NOW-9:30: clear {len(q1)} Q1 item(s) — replies are short because urgency is theirs, not complexity.",
            "9:30-11:00: DEEP BLOCK — no email app open; the Q2 items get their decision slots booked, not answered.",
            f"11:00: batch-delegate the {counts.get('Q3_DELEGATE_OR_QUICK_REPLY', 0)} Q3 items (5 min each, template replies).",
            f"Friday 16:00: {counts.get('Q4_READ_LATER', 0)} Q4 items in one sweep — archive liberally; unread-forever is a decision too.",
            "Guardrail: inbox to zero ACTIONS, not zero emails. Anything older than 14 days unanswered gets archived with a one-line close-out.",
        ]

        verdict = f"{len(items)} emails | {counts.get('Q1_DO_NOW', 0)} do-now | {counts.get('Q2_SCHEDULE', 0)} schedule | {counts.get('Q3_DELEGATE_OR_QUICK_REPLY', 0)} delegate | {counts.get('Q4_READ_LATER', 0)} later"
        return TriagePlan(items, counts, blocks, verdict)

    @staticmethod
    def format_plan(p: TriagePlan) -> str:
        out = ["=" * 62, "EMAIL TRIAGE AGENT — PLAN", "=" * 62, p.verdict, "-" * 62]
        for it in p.items:
            out.append(f"  #{it.idx} [{it.quadrant}] from {it.sender[:30]}")
            out.append(f"      subject : {it.subject[:60]}")
            out.append(f"      ask/deadline: {it.ask} / {it.deadline}")
            out.append(f"      action  : {it.action}")
            if it.draft:
                first = it.draft.splitlines()[0]
                out.append(f"      draft   : {first[:70]}...")
        out += ["-" * 62, "Time blocks:"]
        out += [f"  * {b}" for b in p.time_blocks]
        out.append("=" * 62)
        return "\n".join(out)
