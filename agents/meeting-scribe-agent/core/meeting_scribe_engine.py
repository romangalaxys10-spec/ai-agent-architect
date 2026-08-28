"""
Meeting Scribe Agent Engine.
Converts raw meeting notes/transcripts into decisions, action items
(owner-task-deadline triples), open questions, and a summary.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class ActionItem:
    owner: str
    task: str
    deadline: str
    raw: str

@dataclass
class MeetingDigest:
    summary: str
    decisions: List[str] = field(default_factory=list)
    actions: List[ActionItem] = field(default_factory=list)
    open_questions: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    no_deadline_count: int = 0
    verdict: str = ""

DECISION_RE = re.compile(
    r"(?:we\s+(?:decided|agreed|will go with|chose|settled on)|decision:|it's decided|"
    r"we're (?:going|moving) with|approved|signed off)\s*(.{10,140})", re.I)
ACTION_RE = re.compile(
    r"(?:^|[.\n])\s*([A-Z][a-z]+)\s+(?:will|to|should|owns|is going to)\s+({VB}.{10,110})".replace("{VB}", ""), re.I)
ACTION_VERBS = r"(?:send|write|review|build|fix|schedule|book|call|email|draft|prepare|investigate|check|follow up|ship|deploy|update|create|deliver|own|drive|ping|sync)"
QUESTION_RE = re.compile(r"(?:\?|^(?:what|how|who|when|where|why|should we|can we)\b.{10,120})$", re.I | re.M)
RISK_RE = re.compile(r"\b(risk|concern|blocked|blocker|depend(?:s|ency|encies)?|might (?:fail|slip)|tight|behind schedule)\b", re.I)
OWNER_HINTS = re.compile(r"\b(?:assigned to|owner:)\s*([A-Z][a-z]+)", re.I)

def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().rstrip(".,;")

class MeetingScribeEngine:
    """A meeting without written decisions and owners was just an expensive chat."""

    @classmethod
    def extract(cls, notes: str) -> MeetingDigest:
        lines = [l.strip() for l in notes.splitlines() if l.strip()]
        blob = notes.replace("\n", " ")

        decisions = []
        for m in DECISION_RE.finditer(blob):
            d = _clean(m.group(0))
            if len(d.split()) >= 4 and not any(d[:40] in x for x in decisions):
                decisions.append(d[:150])

        actions = []
        # pattern 1: NAME will VERB ...
        for m in re.finditer(rf"([A-Z][a-z]+)\s+(?:will|is going to|should|to)\s+({ACTION_VERBS}\b[^.;\n]{{5,110}})", blob):
            owner, task = m.group(1), _clean(m.group(2))
            dm = re.search(rf"(?:by|before|due)\s+([A-Za-z]+day|tomorrow|today|EOD|EOW|\d{{1,2}}/\d{{1,2}}|next \w+)", blob[max(0, m.start()-80):m.end()+80], re.I)
            deadline = dm.group(1) if dm else ""
            if not any(a.owner == owner and a.task[:30] == task[:30] for a in actions):
                actions.append(ActionItem(owner, task, deadline, m.group(0)[:120]))
        # pattern 2: "owner: X" annotations
        for m in OWNER_HINTS.finditer(blob):
            owner = m.group(1)
            ctx = blob[max(0, m.start()-100):m.start()]
            task = _clean(ctx.split(".")[-1])[:90]
            if task and len(task.split()) >= 3:
                actions.append(ActionItem(owner, task, "", f"{owner}: {task}"))

        questions = []
        for l in lines:
            if l.endswith("?") and 8 < len(l) < 160:
                questions.append(_clean(l)[:150])
            else:
                qm = re.match(r"^(?:Q:|question:)\s*(.{10,120})", l, re.I)
                if qm:
                    questions.append(_clean(qm.group(1)))

        risks = []
        for l in lines:
            if RISK_RE.search(l) and 6 < len(l) < 160:
                risks.append(_clean(l)[:150])
        if not risks:
            rm = RISK_RE.search(blob)
            if rm:
                risks.append(_clean(blob[max(0, rm.start()-40):rm.end()+60])[:150])

        no_deadline = sum(1 for a in actions if not a.deadline)

        top_actions = sorted(actions, key=lambda a: (not a.deadline, a.owner))[:8]
        if decisions:
            summary = (f"{len(decisions)} decision(s) made, {len(actions)} action item(s) across "
                       f"{len({a.owner for a in actions})} owner(s)"
                       + (f"; {no_deadline} action(s) lack deadlines — chase them." if no_deadline else "."))
        else:
            summary = (f"NO DECISIONS captured in these notes; {len(actions)} action item(s) found. "
                       "If a decision was made verbally, write it down now — memory is not a system of record.")

        verdict = (f"{len(decisions)} decisions | {len(actions)} actions | {no_deadline} deadline-less | "
                   f"{len(questions)} open questions | {len(risks)} risk mentions")
        return MeetingDigest(summary, decisions, top_actions, questions[:5], risks[:4], no_deadline, verdict)

    @staticmethod
    def format_digest(d: MeetingDigest) -> str:
        out = ["=" * 62, "MEETING SCRIBE AGENT — DIGEST", "=" * 62, d.verdict, "-" * 62,
               "Summary:", f"  {d.summary}", "-" * 62, "Decisions:"]
        out += [f"  > {x}" for x in d.decisions] or ["  (none detected — meeting may have been a status update)"]
        out += ["-" * 62, "Action items:"]
        if d.actions:
            out += [f"  [ ] {a.owner:12} {a.task[:70]}" + (f"  (by {a.deadline})" if a.deadline else "  (NO DEADLINE!)")
                    for a in d.actions]
        else:
            out.append("  (none detected)")
        if d.open_questions:
            out += ["-" * 62, "Open questions:"] + [f"  ? {q}" for q in d.open_questions]
        if d.risks:
            out += ["-" * 62, "Risks/concerns raised:"] + [f"  ! {r}" for r in d.risks]
        out += ["-" * 62, "Follow-up template (send within 1h):",
                "  'Team — decisions: [paste above]. Owners: [paste table]. "
                "Corrections within 24h or this becomes the record.'",
                "=" * 62]
        return "\n".join(out)
