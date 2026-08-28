"""
Social Media Manager Agent Engine.
Generates platform-fit post variants, tiered hashtag sets,
thread/carousel structures, reply templates, and posting windows.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class PostVariant:
    angle: str
    text: str
    char_count: int

@dataclass
class SocialPack:
    platform: str
    variants: List[PostVariant] = field(default_factory=list)
    hashtags: dict = field(default_factory=dict)
    structure: List[str] = field(default_factory=list)
    reply_kit: List[dict] = field(default_factory=list)
    post_windows: str = ""
    guardrails: List[str] = field(default_factory=list)
    verdict: str = ""

PLATFORM_RULES = {
    "x": {"max": 280, "link_penalty": True, "thread": "5-9 tweets; tweet 1 must stand alone as content"},
    "linkedin": {"max": 3000, "first_line": True, "no_external_link_in_body": True},
    "instagram": {"max": 2200, "carousel": "6-8 slides; slide 1 is the claim, slide last is CTA"},
    "bluesky": {"max": 300, "chill": "lowercase-leaning tone performs; no engagement bait"},
    "mastodon": {"max": 500, "no_hashtag_spam": "max 2 hashtags; CW for controversial topics"},
}

HASHTAG_TIERS = {
    "broad": ["#ai", "#tech", "#startups"],
    "niche": ["#aiagents", "#llmops", "#devtools", "#promptengineering", "#mlops"],
    "branded": ["#buildinpublic", "#agentarchitect"],
}

class SocialMediaManagerEngine:
    """Same idea, five shapes — the platform is the format."""

    @classmethod
    def generate(cls, topic: str, platform: str = "x", voice: str = "technical, direct, no-hype") -> SocialPack:
        rules = PLATFORM_RULES.get(platform, PLATFORM_RULES["x"])
        max_len = rules["max"]
        vw = [v.strip() for v in voice.split(",")]

        def clamp(text: str) -> str:
            if len(text) <= max_len:
                return text
            # hard trim at sentence boundary
            cuts = [text.rfind(". ", 0, max_len - 1), text.rfind("\n", 0, max_len - 1)]
            cut = max(cuts)
            return text[:cut + 1] if cut > max_len * 0.5 else text[:max_len - 3] + "..."

        core = re.sub(r"\s+", " ", topic).strip().rstrip(".")
        first_words = " ".join(core.split()[:6])

        v1 = clamp(f"{core}.\n\nThe part nobody mentions: it fails silently until it's expensive.\n\n"
                   f"Three fixes, one checklist, receipts below.")
        v2 = clamp(f"We ran {first_words} for 90 days.\n\nWhat broke, what held, what we'd do differently — "
                   f"with the numbers nobody publishes.")
        v3 = clamp(f"Unpopular opinion: most teams do {first_words} backwards.\n\n"
                   "Not their fault — the default docs teach the happy path. Here's the messy path:")

        variants = [
            PostVariant("value-first", v1, len(v1)),
            PostVariant("proof-driven", v2, len(v2)),
            PostAngle := PostVariant("contrarian", v3, len(v3)),
        ]

        tags = {}
        if platform in ("x", "instagram"):
            tags = {
                "tier-1 broad (high reach, low relevance)": HASHTAG_TIERS["broad"][:1],
                "tier-2 niche (the actual audience)": HASHTAG_TIERS["niche"][:3],
                "tier-3 branded/community": HASHTAG_TIERS["branded"][:2],
            }
        elif platform in ("bluesky", "mastodon", "linkedin"):
            tags = {"minimal (platform norm)": HASHTAG_TIERS["niche"][:2]}

        structure = []
        if platform == "x":
            structure = [
                "Tweet 1 (the hook): the claim + why it matters — must work standalone.",
                "Tweet 2-3: the mechanism, one idea per tweet, numbers where possible.",
                "Tweet 4-5: the mistakes + fixes (this is the screenshot-tweet).",
                "Final tweet: CTA to the long-form; 'link in reply' to dodge link penalty.",
            ]
        elif platform == "linkedin":
            structure = [
                "Line 1 is the whole post (feeds truncate at ~210 chars) — no throat-clearing.",
                "Body: 8-12 short lines, one idea each, whitespace as pacing.",
                "Link goes in FIRST COMMENT, not body (algorithm deprioritizes external links).",
                "End with a real question — comments in the first hour drive distribution.",
            ]
        elif platform == "instagram":
            structure = [
                "Slide 1: the claim in <10 words, high contrast.",
                "Slides 2-6: one idea each, 25 words max, big type.",
                "Slide 7: the summary (screenshot-able value).",
                "Slide 8: CTA — 'save this' outperforms 'share this'.",
            ]
        else:
            structure = [
                "Lead with substance; these platforms punish engagement bait.",
                "One idea per post; link freely (no algorithm penalty).",
                "Reply to every comment in the first 2 hours to seed discussion.",
            ]

        reply_kit = [
            {"trigger": "genuine question", "reply": "answer specifically + add one detail not in the post; then ask THEM a question"},
            {"trigger": "disagreement (polite)", "reply": "steelman their point first, then show the boundary where your claim holds"},
            {"trigger": "disagreement (rude)", "reply": "one factual reply max; never a second — the audience judges, not the troll"},
            {"trigger": "'link?'", "reply": "reply with link + pin it; asked-for links convert 3-5x"},
            {"trigger": "correction (you're wrong)", "reply": "thank + correct the post visibly; edits hidden in comments kill trust"},
        ]

        windows = {
            "x": "Tue-Thu 8-10am and 4-6pm ET; threads before 10am, hot-takes after 4pm",
            "linkedin": "Tue-Thu 7:30-9am local; B2B posts before work hours",
            "instagram": "weekdays 11am-1pm and 7-9pm; carousels on Sundays overperform",
            "bluesky": "evenings 8-11pm ET; culture is chatty, not broadcast",
            "mastodon": "weekday mornings EU+US overlap; timezone-distributed instances",
        }[platform]

        guardrails = [
            f"voice check: {', '.join(vw)} — if a line sounds like a press release, cut it",
            "no engagement bait ('comment YES if...') — reach sugar, trust poison",
            "substantive edits happen as 'UPDATED:' replies, never silent edits",
            "if you can't defend the strongest counter-argument in the post, don't post it yet",
        ]

        verdict = f"{len(variants)} variants for {platform} | max {max_len} chars | "
        verdict += f"{sum(len(v) for v in tags.values())} hashtags in {len(tags)} tier(s)"
        return SocialPack(platform, variants, tags, structure, reply_kit, windows, guardrails, verdict)

    @staticmethod
    def format_pack(p: SocialPack) -> str:
        out = ["=" * 62, "SOCIAL MEDIA MANAGER AGENT — PACK", "=" * 62, p.verdict, "-" * 62]
        for v in p.variants:
            out.append(f"  [{v.angle}] ({v.char_count} chars)")
            out += ["    " + ln for ln in v.text.splitlines()]
            out.append("")
        if p.hashtags:
            out += ["-" * 62, "Hashtags (tiered):"]
            for tier, tags in p.hashtags.items():
                out.append(f"  {tier}: {' '.join(tags)}")
        out += ["-" * 62, "Structure:"]
        out += [f"  * {s}" for s in p.structure]
        out += ["-" * 62, "Reply kit:"]
        for r in p.reply_kit:
            out.append(f"  IF {r['trigger']} -> {r['reply']}")
        out += ["-" * 62, f"Posting windows: {p.post_windows}",
                "-" * 62, "Guardrails:"]
        out += [f"  ! {g}" for g in p.guardrails]
        out.append("=" * 62)
        return "\n".join(out)
