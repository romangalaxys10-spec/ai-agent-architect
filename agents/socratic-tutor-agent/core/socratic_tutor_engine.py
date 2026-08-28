"""
Socratic Tutor Agent Engine.
Builds question ladders (recall -> apply -> analyze -> transfer),
misconception probes, hint ladders that never give the answer, and
worked examples with steps hidden behind interaction.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class Rung:
    level: str
    question: str
    misconception_probe: str
    hint_ladder: List[str] = field(default_factory=list)

@dataclass
class Session:
    topic: str
    level: str
    ladder: List[Rung] = field(default_factory=list)
    worked_example: List[str] = field(default_factory=list)
    practice_set: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    verdict: str = ""

LADDER_LEVELS = [
    ("recall", "What is {topic}, in your own words? (No textbook definitions — your words expose what's fuzzy.)"),
    ("apply", "Here's a simple {topic} scenario: it works. Now I change one input — predict what happens BEFORE you compute."),
    ("analyze", "Two systems both use {topic} but behave differently under load. What's the ONE question you'd ask to find the difference?"),
    ("transfer", "You've never seen domain X. Map {topic} onto it — what transfers, what breaks, what's the analog of the core mechanism?"),
]

MISCONCEPTIONS = {
    "recall": "Most people can define {topic} but cannot say what it REPLACES or what it costs. If you can't name the cost, the definition is memorized, not understood.",
    "apply": "The classic error: applying the {topic} rule mechanically and skipping the precondition check that decides whether the rule applies at all.",
    "analyze": "Classic trap: reaching for a more complicated explanation when one differing assumption explains everything. Occam first.",
    "transfer": "The transfer error: copying the surface features of {topic} instead of the underlying mechanism — like copying the paint of a bridge and expecting it to hold weight.",
}

class SocraticTutorEngine:
    """Never hand over the answer — hand over the next question that shrinks the confusion."""

    @classmethod
    def tutor(cls, topic: str, level: str = "beginner", goal: str = "") -> Session:
        rungs = []
        for i, (lvl, q_tpl) in enumerate(LADDER_LEVELS):
            if level == "beginner" and i >= 3:
                break
            if level == "intermediate" and i == 0:
                continue  # skip recall for intermediates
            q = q_tpl.format(topic=topic)
            probe = MISCONCEPTIONS[lvl].format(topic=topic)
            hints = {
                "recall": [
                    "Hint 1: try explaining {topic} to a smart 12-year-old — where does the explanation collapse?",
                    "Hint 2: what problem existed BEFORE {topic}? Naming the predecessor clarifies the definition.",
                    "Hint 3: (last) — what does {topic} trade away to get what it gets? Every mechanism pays.",
                ],
                "apply": [
                    "Hint 1: state the precondition of the {topic} rule out loud. Does the modified input still satisfy it?",
                    "Hint 2: change the input in the SMALLEST possible way and reason about the boundary.",
                    "Hint 3: (last) — the rule's exception IS the lesson. Which exception did you hit?",
                ],
                "analyze": [
                    "Hint 1: list what's identical between the two setups first — differences hide in what you assumed was shared.",
                    "Hint 2: rank the differences by how directly they touch the {topic} mechanism.",
                    "Hint 3: (last) — construct one experiment that would falsify your leading hypothesis.",
                ],
                "transfer": [
                    "Hint 1: write the {topic} mechanism as a sentence with NO domain-specific nouns left in it.",
                    "Hint 2: re-instantiate that abstract sentence in domain X, term by term.",
                    "Hint 3: (last) — the piece that won't re-instantiate is the boundary of the concept. Study exactly there.",
                ],
            }[lvl]
            rungs.append(Rung(lvl, q, probe, [h.format(topic=topic) for h in hints]))

        worked = [
            f"WORKED EXAMPLE (steps revealed one at a time — try each step yourself first):",
            f"Step 1 — restate the problem in your own words. (Do it. Misreading is failure mode #1.)",
            f"Step 2 — identify which {topic} property the problem is actually testing.",
            f"Step 3 — apply the mechanism, narrating WHY each move is legal.",
            f"Step 4 — sanity-check the answer against a boundary case (what if the input were tiny/huge/empty?).",
            f"Step 5 — generalize: write the one sentence you'd tell someone stuck on this exact problem.",
        ]

        practice = [
            "P1 (warm-up): a textbook-shaped {topic} problem — builds fluency, no tricks.",
            "P2 (boundary): the same problem with one input at an edge — tests precondition awareness.",
            "P3 (broken): a problem where {topic} is the WRONG tool; the skill is noticing, not solving.",
            "P4 (transfer): {topic} in a domain you've never seen it in — the final boss.",
        ]

        success = [
            "Learner can re-explain the concept using their own example (not the tutor's).",
            "Learner names the precondition AND the failure mode unprompted.",
            "Learner correctly identifies a problem where the concept does NOT apply.",
            f"Session ends only when the learner has taught something BACK — teaching is the terminal rung.",
        ]

        n_rungs = len(rungs)
        verdict = f"{level} session on '{topic}' | {n_rungs}-rung ladder | 4 practice problems | hints: 3 per rung, answer never given"
        return Session(topic, level, rungs, worked, practice, success, verdict)

    @staticmethod
    def format_session(s: Session) -> str:
        out = ["=" * 62, "SOCRATIC TUTOR AGENT — SESSION", "=" * 62, s.verdict, "-" * 62,
               "Question ladder (answer each before seeing the next):"]
        for i, r in enumerate(s.ladder, 1):
            out.append(f"  Rung {i} [{r.level.upper()}]")
            out.append(f"    Q: {r.question}")
            out.append(f"    probe: {r.misconception_probe}")
            out += [f"    {h}" for h in r.hint_ladder]
        out += ["-" * 62, "Worked example protocol:"]
        out += [f"  {w}" for w in s.worked_example]
        out += ["-" * 62, "Practice set (difficulty gradient):"]
        out += [f"  {p}" for p in s.practice_set]
        out += ["-" * 62, "Success criteria (how you know it worked):"]
        out += [f"  * {c}" for c in s.success_criteria]
        out += ["=" * 62, "Tutor rule: silence after questions is the method, not a malfunction. Count to 10."]
        return "\n".join(out)
