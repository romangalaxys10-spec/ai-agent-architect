"""
Lead Qualifier Agent Engine.
Scores leads on BANT evidence with quotes, tiers them honestly
(MQL / SQL / DISQUALIFY), and writes next-best-actions.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class Pillar:
    name: str
    score: float
    evidence: List[str]

@dataclass
class QualificationVerdict:
    pillars: List[Pillar] = field(default_factory=list)
    total_score: float = 0.0
    tier: str = ""
    disqualifiers: List[str] = field(default_factory=list)
    next_actions: List[str] = field(default_factory=list)
    verdict: str = ""

BUDGET_PATTERNS = [
    (r"\$?\s?(\d{2,3})(k|,000)\b", 1.0),
    (r"budget (?:is|of|around|approved)", 0.9),
    (r"(?:funded|raised|series [abc]|profitable)", 0.7),
    (r"(?:procurement|finance (?:will|can) approve|capex)", 0.6),
]
AUTHORITY_PATTERNS = [
    (r"\b(ceo|cto|cfo|coo|vp\b|vice president|head of|director of|founder|owner)\b", 1.0),
    (r"\b(manager|lead|principal|architect)\b", 0.6),
    (r"(?:evaluate|shortlist|decision committee|buying committee)", 0.5),
    (r"\b(intern|student|research(?:ing)? only)\b", -0.8),
]
NEED_PATTERNS = [
    (r"(?:need|must have|require|looking for|searching for|pain point)", 0.8),
    (r"(?:can't|cannot|struggling to|failing to|blocked by)", 1.0),
    (r"(?:current (?:tool|system|vendor)|incumbent)", 0.5),
    (r"(?:just curious|exploring|no rush)", 0.2),
]
TIMELINE_PATTERNS = [
    (r"(?:this (?:week|month|quarter)|asap|immediately|yesterday)", 1.0),
    (r"(?:next (?:quarter|month)|Q[1-4]\b|\d{1,2} (?:weeks|months))", 0.7),
    (r"(?:sometime|eventually|next year|no timeline|when we get time)", 0.2),
    (r"(?:budget cycle|fiscal year end)", 0.5),
]

FIT_SIGNALS = [
    (r"(?:python|api|sdk|integration|automation|platform|saas|devops)", 0.5),
]

class LeadQualifierEngine:
    """Honest pipeline: a lead without evidence is a lead without a score."""

    @classmethod
    def _score(cls, text: str, patterns) -> tuple:
        low = text.lower()
        score, evidence = 0.0, []
        for pat, weight in patterns:
            for m in re.finditer(pat, low):
                score += weight
                evidence.append(f'"{text[max(0, m.start()-25):m.end()+25].strip()}"')
                if score >= 1.5:
                    break
            if score >= 1.5:
                break
        return min(score, 1.5), evidence[:3]

    @classmethod
    def qualify(cls, lead_text: str) -> QualificationVerdict:
        pillars = []
        for name, pats in (("Budget", BUDGET_PATTERNS), ("Authority", AUTHORITY_PATTERNS),
                           ("Need", NEED_PATTERNS), ("Timeline", TIMELINE_PATTERNS)):
            s, ev = cls._score(lead_text, pats)
            pillars.append(Pillar(name, round(min(1.0, s), 2), ev))

        fit, _ = cls._score(lead_text, FIT_SIGNALS)
        total = round(25 * sum(p.score for p in pillars) + 5 * min(fit, 1.0), 1)

        disq = []
        if re.search(r"\b(student|homework|personal project|just curious|free plan only)\b",
                     lead_text, re.I):
            disq.append("No commercial intent detected (student/hobby/curiosity language).")
        if pillars[0].score == 0 and pillars[3].score <= 0.2:
            disq.append("Neither budget signal nor timeline — park in nurture, do not book.")
        if re.search(r"\b(intern|job applicant|looking for a job)\b", lead_text, re.I):
            disq.append("This is a job-seeker, not a buyer — route to recruiting.")

        if disq and total < 60:
            tier = "DISQUALIFY"
        elif total >= 80:
            tier = "SQL"
        elif total >= 55:
            tier = "MQL"
        else:
            tier = "NURTURE"

        actions = {
            "SQL": ["Book discovery call within 48h (they are ready).",
                    "Prep: pull the quoted pain points into the agenda verbatim.",
                    "Loop in the AE + solutions engineer for the technical track."],
            "MQL": ["Send the 1-page ROI brief matched to their stated pain.",
                    "Offer a self-serve trial + 15-min optional walkthrough.",
                    "Re-score after 2 engagements; promote if Budget or Timeline moves."],
            "NURTURE": ["Add to the 6-touch education sequence (no pitch in first 3).",
                        "Score engagement monthly; exit the sequence at 2 unsubscribes."],
            "DISQUALIFY": ["Close as disqualified with the reason recorded (keeps conversion metrics honest).",
                           "Point to free docs/community for the non-commercial path."],
        }[tier]

        verdict = f"{tier} | score {total}/110 | " + ", ".join(f"{p.name}:{p.score:.0%}" for p in pillars)
        return QualificationVerdict(pillars, total, tier, disq, actions, verdict)

    @staticmethod
    def format_verdict(v: QualificationVerdict) -> str:
        out = ["=" * 62, "LEAD QUALIFIER AGENT — VERDICT", "=" * 62, v.verdict, "-" * 62]
        for p in v.pillars:
            out.append(f"  {p.name:10} {p.score:.0%}")
            for e in p.evidence:
                out.append(f"      evidence: {e}")
        if v.disqualifiers:
            out += ["-" * 62, "Disqualifiers:"]
            out += [f"  ! {d}" for d in v.disqualifiers]
        out += ["-" * 62, "Next actions:"]
        out += [f"  {i}. {a}" for i, a in enumerate(v.next_actions, 1)]
        out.append("=" * 62)
        return "\n".join(out)
