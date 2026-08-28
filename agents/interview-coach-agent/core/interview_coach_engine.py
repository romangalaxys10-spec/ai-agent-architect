"""
Interview Coach Agent Engine.
Designs structured interviews: competency-mapped question bank with
STAR follow-ups, anchored 1-5 rubrics, legal guardrails, scorecards.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class Question:
    competency: str
    question: str
    follow_ups: List[str] = field(default_factory=list)
    red_flags: List[str] = field(default_factory=list)
    green_flags: List[str] = field(default_factory=list)

@dataclass
class InterviewKit:
    role: str
    level: str
    questions: List[Question] = field(default_factory=list)
    rubric: List[str] = field(default_factory=list)
    illegal_avoid: List[str] = field(default_factory=list)
    scorecard: List[str] = field(default_factory=list)
    structure: List[str] = field(default_factory=list)
    verdict: str = ""

QUESTION_BANK = {
    "coding": [
        ("Walk me through a piece of code you wrote recently that you're proud of. What would you change about it now?",
         ["What were the constraints you were coding under?", "How did you know it was done?"]),
        ("I describe a bug, you think aloud through diagnosing it. Ready? 'Users report the dashboard loads slowly only on Mondays.'",
         ["What would you check first?", "How would you prove your hypothesis?"]),
    ],
    "system design": [
        ("Design a rate limiter for a public API. Start with the requirements you'd pin down.",
         ["What fails at 10x scale?", "Where does consistency matter here?"]),
        ("You inherit a monolith with zero tests and one release per quarter. What do you do in the first 90 days?",
         ["What do you NOT do?", "How do you measure whether you're winning?"]),
    ],
    "collaboration": [
        ("Tell me about a technical disagreement you lost. What happened after?",
         ["What did you learn about the other side's position?", "Would you argue it differently today?"]),
        ("Describe a time you had to get work from a team you don't manage.",
         ["How did you handle the first 'no'?", "What did you trade?"]),
    ],
    "ownership": [
        ("Tell me about something you shipped that failed in production. Walk me through the incident.",
         ["What did the postmortem change — be specific?", "Who did you tell first?"]),
        ("What's the most boring-but-important thing you've maintained? How did you keep it alive?",
         ["How did you make maintenance visible to others?"]),
    ],
    "communication": [
        ("Explain your current project to me as if I'm a new PM on the team.",
         ["Now explain it to me as if I'm the CFO.", "What did you cut out of each version and why?"]),
    ],
    "leadership": [
        ("Tell me about someone you grew. What did they go on to do?",
         ["What did you do when they surpassed you at something?"]),
        ("A senior engineer on your team is delivering well but burning others out. What do you do?",
         ["What if it's your best performer?", "What if 'the team' is wrong about them?"]),
    ],
    "learning": [
        ("What have you learned in the last 6 months that changed how you work?",
         ["What did it replace? What was wrong with the old way?"]),
    ],
}

LEVEL_DEPTH = {
    "junior": 2, "mid": 3, "senior": 4, "staff": 4, "principal": 5,
}

ILLEGAL_TOPICS = [
    "Age, birth year, or 'when did you graduate' (age proxy)",
    "Family, kids, pregnancy plans, or childcare arrangements",
    "National origin, accent, citizenship beyond work-authorization yes/no",
    "Religion, holidays observed, or 'what church/temple do you attend'",
    "Health conditions or disability inquiries before a conditional offer",
    "Salary history (banned in many jurisdictions — budget the role instead)",
    "Arrest record (distinct from relevant convictions, per local law)",
]

class InterviewCoachEngine:
    """Unstructured interviews measure charisma. Structured ones measure the job."""

    @classmethod
    def design(cls, role: str, level: str = "senior", competencies: List[str] = None) -> InterviewKit:
        comps = [c.lower().strip() for c in (competencies or ["coding", "system design", "collaboration", "ownership"])]
        depth = LEVEL_DEPTH.get(level, 3)

        questions = []
        for comp in comps:
            bank = QUESTION_BANK.get(comp, QUESTION_BANK["collaboration"])
            for i, (q, follow) in enumerate(bank):
                if i >= max(1, depth - 1):
                    break
                level_prefix = {
                    "junior": "keep it to a scoped scenario",
                    "mid": "include one tradeoff they had to live with",
                    "senior": "push into cross-team blast radius",
                    "staff": "probe the org-level incentives at play",
                    "principal": "probe multi-year and ecosystem consequences",
                }[level]
                questions.append(Question(
                    comp, q, follow + [f"For {level}: {level_prefix}."],
                    red_flags=["blames others without owning any part",
                               "cannot name a single specific detail",
                               "story has no failure in it (either sanitized or low ownership)"],
                    green_flags=["names specifics: systems, numbers, names of tradeoffs",
                                 "owns a mistake unprompted",
                                 "changes their mind mid-answer when the evidence shifts"]))

        rubric = [
            "1 — Could not engage with the question; no specifics; would need heavy support.",
            "2 — Engaged but stayed abstract; specifics thin; tradeoffs named without reasoning.",
            "3 — Solid: concrete example, sound reasoning, one meaningful tradeoff owned.",
            "4 — Strong: multiple real constraints juggled; taught the panel something.",
            "5 — Exceptional: reframed the problem; evidence of repeat success; panel would follow them.",
            "Score EVERY candidate on the SAME questions. Notes must quote the candidate, not summarize your feelings.",
        ]

        scorecard = [
            "Per competency: score (1-5) + one verbatim quote as evidence.",
            "Recommendation field: STRONG HIRE / HIRE / NO HIRE — no 'leaning' options.",
            "Any interviewer scoring 2+ points away from the panel triggers a calibration call, not an average.",
            "Decision within 24h of the last interview; memory decay starts immediately.",
        ]

        structure = [
            f"60-min {level} loop: 5 min warmup, 40 min competency questions ({', '.join(comps[:3])}), "
            "10 min candidate questions, 5 min next-steps.",
            "Panels write notes DURING, not after — after-notes are fiction with a timestamp.",
            "Same question order for every candidate; behavioral questions come before design so everyone starts warm.",
        ]

        verdict = f"{len(questions)} questions | {len(comps)} competencies | {level} depth | structured loop"
        return InterviewKit(role, level, questions, rubric, ILLEGAL_TOPICS, scorecard, structure, verdict)

    @staticmethod
    def format_kit(k: InterviewKit) -> str:
        out = ["=" * 62, "INTERVIEW COACH AGENT — KIT", "=" * 62,
               f"Role: {k.role} ({k.level})", k.verdict, "-" * 62, "Question bank:"]
        for i, q in enumerate(k.questions, 1):
            out.append(f"  Q{i} [{q.competency}] {q.question}")
            out += [f"      follow-up: {f}" for f in q.follow_ups]
            out.append(f"      green: {q.green_flags[0]}")
            out.append(f"      red  : {q.red_flags[0]}")
        out += ["-" * 62, "Scoring rubric (anchored):"]
        out += [f"  {r}" for r in k.rubric]
        out += ["-" * 62, "DO NOT ASK (legal guardrails):"]
        out += [f"  ! {t}" for t in k.illegal_avoid]
        out += ["-" * 62, "Scorecard protocol:"]
        out += [f"  * {s}" for s in k.scorecard]
        out += ["-" * 62, "Loop structure:"]
        out += [f"  - {s}" for s in k.structure]
        out.append("=" * 62)
        return "\n".join(out)
