"""
Meeting Brief Agent Engine.
Builds pre-meeting briefs: attendee map, timed agenda, goals,
objection-response pairs, and pre-read assignments.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class MeetingBrief:
    topic: str
    attendees: List[dict] = field(default_factory=list)
    agenda: List[str] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)
    objections: List[dict] = field(default_factory=list)
    pre_reads: List[str] = field(default_factory=list)
    missing_context: List[str] = field(default_factory=list)
    verdict: str = ""

ROLE_PLAYS = {
    "cto": ("technical risk + architectural fit", ["reference architectures", "failure modes", "migration cost"]),
    "ceo": ("business outcome + momentum", ["time-to-value", "what it unblocks", "cost of waiting"]),
    "cfo": ("cost, ROI, and downside", ["payback period", "unit economics", "exit cost"]),
    "vp": ("delivery risk + team impact", ["workflow change", "adoption plan", "success metrics"]),
    "director": ("execution details", ["rollout sequencing", "tooling overlap", "support model"]),
    "manager": ("team-level friction", ["day-to-day workflow", "training needs"]),
    "engineer": ("hands-on truth", ["API quality", "debuggability", "integration effort"]),
    "pm": ("scope + roadmap fit", ["scope creep risk", "dependencies"]),
    "founder": ("speed + leverage", ["fastest path to value", "minimal process"]),
}

OBJECTION_BANK = [
    (r"(price|expensive|budget|cost)", "Price",
     "Reframe to cost-of-inaction: quantify the hours/incidents per month; offer a phased start."),
    (r"(security|compliance|soc|gdpr|privacy)", "Security/Compliance",
     "Lead with the security one-pager: data flow diagram, retention, certifications; offer a security review call."),
    (r"(time|bandwidth|resources|busy)", "No bandwidth",
     "Propose a 2-week pilot with a fixed 4h/week cap; success criteria agreed up front."),
    (r"(integrat|work with|compatible|existing)", "Integration risk",
     "Bring the integration matrix + adapter plan; name the specific systems they run."),
    (r"(switch|migrat|lock-in|contract)", "Switching cost / lock-in",
     "Show the exit plan in writing (data export, dual-run); lock-in fear shrinks when exit is easy."),
    (r"(competitor|already use|current vendor|incumbent)", "Incumbent",
     "Never attack the incumbent; find the workflow they've stopped trying to fix and demo only that."),
    (r"(timing|later|next quarter|not now)", "Timing",
     "Tie to their dated event (launch, audit, renewal) — postpone without a date is a soft no; ask for one."),
]

class MeetingBriefEngine:
    """Walk in with the map, the goal, and the answers to objections not yet asked."""

    @classmethod
    def brief(cls, topic: str, attendees: List[str], context: str = "") -> MeetingBrief:
        att_out = []
        for raw in attendees:
            name = raw.strip()
            low = name.lower()
            role_key = next((k for k in ROLE_PLAYS if k in low), "pm" if "product" in low else "engineer")
            concern, talking = ROLE_PLAYS[role_key]
            att_out.append({"name": name, "lens": concern, "talk_track": talking[:2] if isinstance(talking, list) else talking})

        # agenda sizing: 25 min meeting assumption
        n = len(att_out) or 1
        agenda = [
            f"0-3 min: open with the specific context hook — quote their own words: '{(context or topic)[:70]}'.",
            f"3-8 min: current-state recap from THEIR perspective (2 of their priorities: {', '.join(a['lens'] for a in att_out[:2])}).",
            f"8-16 min: focused demo/discussion on the ONE topic that hits the top attendee's lens.",
            f"16-21 min: objection sweep — surface the known blockers before they do.",
            f"21-25 min: agree ONE concrete next step with an owner and a date. Never end on 'we'll follow up'.",
        ]
        if n >= 5:
            agenda.insert(0, "PRE-WORK: if >4 attendees, send the brief 24h ahead or the meeting will be a first-read.")

        goals = [
            "PRIMARY: leave with a dated, owned next step (pilot scope, intro, or decision date).",
            "SECONDARY: learn the real decision process — who signs, what form the decision takes.",
            "GUARDRAIL: do not present more than one capability; depth beats breadth in a first meeting.",
        ]

        blob = (context + " " + topic).lower()
        objections = []
        for pat, name, response in OBJECTION_BANK:
            if re.search(pat, blob):
                objections.append({"objection": name, "response": response})
        if not objections:
            objections.append({"objection": "price (assume always latent)",
                               "response": "Have the ROI math ready even if they never ask."})

        pre_reads = [
            "Their latest public update (post/release/changelog) — cite it by name in minute 1.",
            "One-page agenda + the single demo path you will run.",
            "Q&A cheat sheet: top-5 likely questions with 2-sentence answers.",
        ]

        missing = []
        if not context.strip():
            missing.append("No account/project context given — brief quality is capped; research before the call.")
        if n < 2:
            missing.append("Only one attendee listed — confirm the decision-maker is in the room.")

        verdict = f"BRIEF READY | {len(att_out)} attendees mapped | {len(objections)} objection plays armed"
        return MeetingBrief(topic, att_out, agenda, goals, objections, pre_reads, missing, verdict)

    @staticmethod
    def format_brief(b: MeetingBrief) -> str:
        out = ["=" * 62, "MEETING BRIEF AGENT — BRIEFING", "=" * 62,
               f"Topic: {b.topic}", b.verdict, "-" * 62, "Attendee map:"]
        for a in b.attendees:
            out.append(f"  {a['name']:28} lens: {a['lens']}")
            out.append(f"  {'':28} talk-track: {', '.join(a['talk_track']) if isinstance(a['talk_track'], list) else a['talk_track']}")
        out += ["-" * 62, "Timed agenda:"]
        out += [f"  {ag}" for ag in b.agenda]
        out += ["-" * 62, "Goals:"] + [f"  * {g}" for g in b.goals]
        out += ["-" * 62, "Objection plays:"]
        for o in b.objections:
            out.append(f"  IF '{o['objection']}' -> {o['response']}")
        out += ["-" * 62, "Pre-reads:"] + [f"  * {p}" for p in b.pre_reads]
        if b.missing_context:
            out += ["-" * 62, "MISSING CONTEXT (fix before meeting):"] + [f"  ! {m}" for m in b.missing_context]
        out.append("=" * 62)
        return "\n".join(out)
