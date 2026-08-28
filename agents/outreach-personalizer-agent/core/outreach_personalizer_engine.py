"""
Outreach Personalizer Agent Engine.
Extracts prospect hooks, writes 3-tone personalized emails,
and lints spam triggers with an A/B sequence plan.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class OutreachPack:
    prospect_hooks: List[str] = field(default_factory=list)
    variants: List[dict] = field(default_factory=list)
    spam_words_found: List[str] = field(default_factory=list)
    spam_score: float = 0.0
    sequence: List[str] = field(default_factory=list)
    verdict: str = ""

SPAM_WORDS = ["free", "guarantee", "act now", "limited time", "no obligation", "risk-free",
              "buy now", "click here", "special offer", "discount", "urgent", "opportunity",
              "revolutionary", "game-changer", "synergy", "circle back", "touch base"]

HOOK_PATTERNS = [
    (r"\b(CTO|VP Engineering|Head of Engineering|Director of Engineering)\b", "senior technical leadership — cares about risk and velocity tradeoffs"),
    (r"\b(scale|scaling|hypergrowth|Series [ABC])\b", "scaling pain — reliability and process debt are topical"),
    (r"\b(hiring|headcount|team of \d+|grew the team)\b", "team growth — onboarding and standards friction"),
    (r"\b(migration|monolith|legacy|refactor)\b", "modernization work in flight"),
    (r"\b(outage|downtime|incident|SEV)\b", "recent reliability events — a live wound"),
    (r"\b(Rust|Go|TypeScript|Python|Kubernetes|serverless)\b", "explicit stack signal — reference it precisely"),
    (r"\b(talk|conference|podcast|blog|post)\b", "public content exists — cite it honestly"),
    (r"\b(launched|announced|released|shipped)\b", "recent launch — timing hook"),
]

class OutreachPersonalizerEngine:
    """Personalization is research made visible — one earned detail beats five flattered ones."""

    @classmethod
    def personalize(cls, prospect_text: str, offer: str = "a 15-minute architecture review call") -> OutreachPack:
        low = prospect_text.lower()
        hooks = []
        for pat, interp in HOOK_PATTERNS:
            m = re.search(pat, prospect_text)
            if m:
                hooks.append(f"{m.group(0)} — {interp}")

        first_name = "there"
        m = re.search(r"(?:name[:\s]+|^)\s*([A-Z][a-z]{2,15})\b", prospect_text)
        if m and m.group(1).lower() not in ("the", "our", "team"):
            first_name = m.group(1)

        company = "your team"
        m = re.search(r"\bat\s+([A-Z][A-Za-z0-9\-]+)\b", prospect_text)
        if m:
            company = m.group(1)

        hook_line = hooks[0] if hooks else "your engineering roadmap"
        hook_snippet = hook_line.split(" — ")[0] if hooks else "what your team is building"

        variants = [
            {"tone": "peer-expert",
             "subject": f"{hook_snippet} — quick engineering question",
             "body": (f"Hi {first_name},\n\n"
                      f"I read that {company} is dealing with {hook_line.split(' — ')[0] if hooks else 'scaling'}. "
                      f"Most teams at that stage hit the same wall: incident load rises faster than headcount.\n\n"
                      f"I put together a 2-page teardown of how 3 similar teams cut review time ~40% without adding process bloat.\n\n"
                      f"Worth {offer}?\n\n"
                      f"— sent by a human who read your post before writing this")},
            {"tone": "crisp-executive",
             "subject": f"16-min idea for {company}",
             "body": (f"{first_name} —\n\n"
                      f"Signal: {hook_snippet}.\n"
                      f"Claim: teams like yours recover 3-5 eng-hours/week with one workflow change.\n"
                      f"Proof: 2-page teardown, real numbers, no fluff.\n\n"
                      f"Open to {offer}? If not, reply 'pass' and I'll close the loop.\n\n"
                      f"(Respects your time: 4 sentences, one ask.)")},
            {"tone": "curious-storyteller",
             "subject": f"the {hook_snippet} problem, retold",
             "body": (f"Hi {first_name},\n\n"
                      f"Every team I've talked to recently has a version of the same story about {hook_snippet}: "
                      f"the fix that worked at 5 engineers quietly breaks at 30.\n\n"
                      f"There's usually one specific bottleneck — I found {company}'s version interesting because of "
                      f"what you mentioned around {hook_snippet}.\n\n"
                      f"I wrote up the pattern (with the failure modes). Happy to share — and if useful, {offer}.\n\n"
                      f"Either way, keep shipping.")},
        ]

        blob = " ".join(v["subject"] + " " + v["body"] for v in variants).lower()
        found = [w for w in SPAM_WORDS if w in blob]
        spam_score = round(min(1.0, 0.08 * len(found)), 2)

        for v in variants:
            v["word_count"] = len(v["body"].split())
            if v["word_count"] > 120:
                v["trim_hint"] = f"{v['word_count']} words — cut to <=120 (attention cliff)"

        sequence = [
            "Day 0: send variant A (peer-expert) Tue-Thu, 7-9am recipient local time.",
            "Day 3: value bump — share the teardown itself, no ask.",
            "Day 7: send variant B (crisp-executive) as reply on the SAME thread.",
            "Day 14: variant C (storyteller) OR a polite close-out that leaves the door open.",
            "Stop after 4 touches total. Sequence-abuse burns the domain.",
        ]

        verdict = f"3 variants | hooks: {len(hooks)} | spam score {spam_score:.0%}"
        return OutreachPack(hooks, variants, found, spam_score, sequence, verdict)

    @staticmethod
    def format_pack(p: OutreachPack) -> str:
        out = ["=" * 62, "OUTREACH PERSONALIZER AGENT — PACK", "=" * 62, p.verdict, "-" * 62,
               "Prospect hooks (earned details):"]
        out += [f"  - {h}" for h in p.prospect_hooks] or ["  - none found: DO NOT send generic email; research first"]
        for v in p.variants:
            out += ["-" * 62, f"VARIANT: {v['tone']}  ({v['word_count']} words)"]
            out.append(f"  Subject: {v['subject']}")
            out += ["  " + ln for ln in v["body"].splitlines()]
            if v.get("trim_hint"):
                out.append(f"  !! {v['trim_hint']}")
        out += ["-" * 62,
                f"Spam lint: {p.spam_score:.0%}" + (f" (found: {', '.join(p.spam_words_found)})" if p.spam_words_found else " (clean)")]
        out += ["A/B sequence:"] + [f"  {i}. {s}" for i, s in enumerate(p.sequence, 1)]
        out.append("=" * 62)
        return "\n".join(out)
