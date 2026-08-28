"""
Language Coach Agent Engine.
Analyzes learner writing: CEFR level estimate with evidence, error
taxonomy, targeted drills, spaced-repetition queue, model rewrites.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class ErrorItem:
    kind: str
    count: int
    example: str
    fix_rule: str

@dataclass
class CoachingPlan:
    estimated_cefr: str
    cefr_evidence: List[str] = field(default_factory=list)
    errors: List[ErrorItem] = field(default_factory=list)
    drills: List[str] = field(default_factory=list)
    srs_queue: List[str] = field(default_factory=list)
    model_rewrites: List[str] = field(default_factory=list)
    verdict: str = ""

COMMON_ERRORS = {
    "article_errors": (r"\b(a|an|the)\s+(?=\b(?:information|advice|furniture|research|evidence)\b)", 2,
                       "uncountable nouns take no article: 'information', not 'an information'"),
    "preposition_errors": (r"\b(depend of|married with|discuss about|explain about|married with)\b", 2,
                           "verb-specific prepositions: depend ON, married TO, discuss (no about)"),
    "third_person_s": (r"\b(he|she|it)\s+(\w+?)(?<!s)\b", 1,
                       "third-person singular present takes -s: 'she writes'"),
    "plural_errors": (r"\b(these|those|many|several|two|three)\s+(\w+?)(?<!s)\b", 1,
                      "plural determiners need plural nouns: 'many reasons'"),
    "double_negative": (r"\b(don't|doesn't|didn't|not)\s+\w+\s+(no|nothing|never|nobody)\b", 3,
                        "one negation per clause in standard English"),
    "run_on": (r"[,;]\s+\w+[^.!?]{35,}[.!?]", 1,
               "comma splices: split the sentence or use a conjunction"),
    "wrong_tense": (r"\b(since|for)\s+\w+\s+ago\b", 2,
                     "'since/for' never pairs with 'ago'"),
    "subject_verb": (r"\b(people|data|criteria)\s+is\b", 2,
                     "'people/data/criteria are' (plural in usage)"),
    "collocation": (r"\b(do|make)\s+(a\s+)?(mistake|progress|research|homework)\b", 1,
                    "fixed collocations: MAKE progress/mistakes, DO research/homework"),
}

CEFR_MARKERS = {
    "A1": ["I am", "he is", "my name", "I like"],
    "A2": ["yesterday", "last week", "I went", "because"],
    "B1": ["I think", "should", "if I", "used to", "although"],
    "B2": ["however", "therefore", "in spite of", "would have", "moreover"],
    "C1": ["nevertheless", "notwithstanding", "were it not", "had I known", "thereby", "albeit"],
    "C2": ["inasmuch as", "insofar as", "paradoxically", "it follows that", "qua "],
}

class LanguageCoachEngine:
    """Correct the pattern, not the sentence — drills beat red ink."""

    @classmethod
    def coach(cls, text: str, target_lang: str = "english", level: str = "unknown") -> CoachingPlan:
        low = " " + text.lower() + " "
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
        words = re.findall(r"[A-Za-z']+", text)
        n = max(1, len(words))

        # CEFR estimate: highest marker tier present with >=2 hits
        est = None
        tier_order = ["A1", "A2", "B1", "B2", "C1", "C2"]
        hits_by_tier = {}
        for tier in tier_order:
            hits = sum(1 for m in CEFR_MARKERS[tier] if m in low)
            hits_by_tier[tier] = hits
        for tier in reversed(tier_order):
            if hits_by_tier.get(tier, 0) >= 2:
                est = tier
                break
        # lexical diversity adjustment
        ttr = len(set(w.lower() for w in words)) / n
        avg_sent = len(words) / max(1, len(sentences))
        if est is None:
            est = "B1" if ttr > 0.55 and avg_sent > 12 else "A2" if ttr > 0.4 else "A1"
        if level != "unknown":
            est = level  # trust the declared level; still show evidence

        evidence = [
            f"type-token ratio {ttr:.2f} (higher = more varied vocabulary)",
            f"avg sentence length {avg_sent:.1f} words",
            "marker hits: " + ", ".join(f"{t}:{hits_by_tier[t]}" for t in tier_order if hits_by_tier.get(t)),
        ]

        errors = []
        for kind, (pattern, weight, rule) in COMMON_ERRORS.items():
            hits = re.findall(pattern, text, re.I)
            if hits:
                ex = " ".join(hits[0]) if isinstance(hits[0], tuple) else str(hits[0])
                errors.append(ErrorItem(kind, len(hits), ex[:60], rule))
        errors.sort(key=lambda e: -e.count)

        drills = []
        for e in errors[:3]:
            drill_map = {
                "article_errors": "Drill: 10 sentences describing abstract nouns — say each with/without article and justify.",
                "preposition_errors": "Drill: verb+preposition flashcards (depend ON, insist ON, argue WITH) — 3 rounds, say-aloud.",
                "third_person_s": "Drill: narrate a friend's daily routine for 60 seconds in present tense; record and listen for missing -s.",
                "plural_errors": "Drill: quantifier+noun pairs (many/much/few/little) — sort 20 nouns into countable/uncountable first.",
                "double_negative": "Drill: rewrite 5 negative sentences into single-negation standard forms.",
                "run_on": "Drill: take your own long sentences; split each at the conjunction. Read aloud — breath points are sentence boundaries.",
                "wrong_tense": "Drill: timeline exercise — place 'ago', 'since', 'for' events on a time axis; the axis forbids the wrong pairings.",
                "subject_verb": "Drill: subject-verb agreement ladder: is/are, has/have, was/were with tricky subjects (people, data, criteria).",
                "collocation": "Drill: do/make collocation sort — 30 common nouns, two columns, timed twice.",
            }
            drills.append(f"{e.kind} (x{e.count}): {drill_map.get(e.kind, 'targeted repetition with feedback')}")

        srs = [
            "Day 1: study today's 3 error rules + self-test with 5 fresh examples each.",
            "Day 2: review (recognition: spot the error in corrupted sentences).",
            "Day 4: review (production: write 5 correct sentences using the target structure).",
            "Day 8: mixed review — errors interleaved so you must DIAGNOSE, not just apply.",
            "Day 16: final review; any lapse resets the card to Day 1. Harsh spacing is the feature.",
        ]

        rewrites = []
        for s in sentences[:2]:
            fixed = s
            fixed = re.sub(r"\ban\s+(information|advice|furniture|research)\b", r"\1", fixed, flags=re.I)
            fixed = re.sub(r"\bdepend of\b", "depend on", fixed, flags=re.I)
            fixed = re.sub(r"\bdiscuss about\b", "discuss", fixed, flags=re.I)
            fixed = re.sub(r"\bmake (a )?(mistake|progress|research)\b", r"do \2", fixed, flags=re.I)
            fixed = re.sub(r"\bsince (\w+) ago\b", r"\1 ago", fixed, flags=re.I)
            if fixed != s:
                rewrites.append(f"before: {s[:90]}\n after: {fixed[:90]}")
        if not rewrites and errors:
            rewrites.append("Pattern-level rewrite: apply the top error rule to your next 3 written paragraphs — your text's errors are systematic, not random.")

        verdict = (f"{len(words)} words | CEFR ~{est} | {len(errors)} error types "
                   f"({sum(e.count for e in errors)} instances) | {len(drills)} drills")
        return CoachingPlan(est, evidence, errors, drills, srs, rewrites, verdict)

    @staticmethod
    def format_plan(p: CoachingPlan) -> str:
        out = ["=" * 62, "LANGUAGE COACH AGENT — PLAN", "=" * 62, p.verdict, "-" * 62,
               f"Estimated level: {p.estimated_cefr}",
               "Evidence:"] + [f"  - {e}" for e in p.cefr_evidence]
        if p.errors:
            out += ["-" * 62, "Error taxonomy (fix in this order):"]
            for e in p.errors:
                out.append(f"  [{e.kind:18}] x{e.count}  e.g. \"{e.example}\"")
                out.append(f"      rule: {e.fix_rule}")
        else:
            out += ["-" * 62, "No common error patterns detected — push into harder material."]
        out += ["-" * 62, "Targeted drills:"] + [f"  * {d}" for d in p.drills]
        out += ["-" * 62, "Spaced repetition queue:"] + [f"  - {s}" for s in p.srs_queue]
        if p.model_rewrites:
            out += ["-" * 62, "Model rewrites:"] + [f"  {r}" for r in p.model_rewrites]
        out += ["=" * 62, "Output beats input: write 150 words daily; this coach audits the patterns, you do the reps."]
        return "\n".join(out)
