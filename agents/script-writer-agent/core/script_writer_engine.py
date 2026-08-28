"""
Script Writer Agent Engine.
Writes video script scaffolds: 5-second hook, beat structure with
timestamps, retention tactics at drop-off points, cutdowns per platform.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class Beat:
    timestamp: str
    label: str
    content: str
    retention_tactic: str = ""

@dataclass
class Script:
    topic: str
    hook: str
    promise: str
    beats: List[Beat] = field(default_factory=list)
    cta_variants: List[str] = field(default_factory=list)
    broll: List[str] = field(default_factory=list)
    cutdowns: List[dict] = field(default_factory=list)
    drop_off_guards: List[str] = field(default_factory=list)
    verdict: str = ""

STYLE_BEATS = {
    "educational": [
        ("hook", "The counterintuitive claim", "State the thing everyone gets backwards about {topic}, with a number or visual proof."),
        ("promise", "The payoff contract", "'In the next N minutes you'll know X, Y, and the one mistake that costs the most.'"),
        ("context", "Why you should care", "One concrete failure/success story with stakes — not 'in today's world'."),
        ("core", "The mechanism", "Explain {topic} in 3 layers: what it looks like, what it actually is, what breaks it."),
        ("proof", "Receipts", "Show the demo/benchmark/data live. Narrate what the audience is seeing."),
        ("mistakes", "Top 3 mistakes", "Each mistake: name it, show the symptom, give the one-line fix."),
        ("payoff", "The summary they can repeat", "Compress everything into one sentence they could tell a colleague."),
        ("cta", "The loop-closer", "Point to the deeper resource; tease the adjacent question you deliberately didn't answer."),
    ],
    "entertaining": [
        ("hook", "Cold open mid-action", "Drop into the most chaotic moment of the {topic} story."),
        ("stakes", "What's at risk", "Make the audience need to know how it ends."),
        ("setup", "How we got here", "Fast context with jokes doing double duty as information."),
        ("twist", "The turn", "The moment the plan broke — replay it once for effect."),
        ("payoff", "Resolution", "Deliver the outcome + the lesson wearing a joke costume."),
        ("cta", "Callback + ask", "Callback the cold-open line; ask for the subscribe as a punchline."),
    ],
    "documentary": [
        ("hook", "The unexplained artifact", "Show the weirdest evidence about {topic} first; withhold the explanation."),
        ("question", "Frame the mystery", "Pose the question the whole film answers."),
        ("act1", "The origin", "Where {topic} began, told through one person."),
        ("act2", "The complication", "What went wrong / what nobody predicted."),
        ("act3", "The reckoning", "The consequences, with both sides given their strongest case."),
        ("resolution", "What we know now", "Answer the opening question; sit with what remains unknown."),
        ("cta", "Further down", "Point to primary sources; invite the audience to verify."),
    ],
    "promotional": [
        ("hook", "The problem in one scene", "Show the pain of not-solving {topic} — dramatize 10 seconds of it."),
        ("agitate", "The cost of the status quo", "Quantify what the problem costs per week/month."),
        ("solution", "The reveal", "Introduce the product as the mechanism, not the hero — 15 seconds max."),
        ("proof", "Social proof + demo", "One user's before/after with a number attached."),
        ("objection", "Handle the biggest doubt", "Name the skeptic's question and answer it honestly."),
        ("cta", "The low-friction ask", "One action, one link, one reason it's safe to try."),
    ],
}

class ScriptWriterEngine:
    """Retention is designed at the beat level, not hoped for in the edit."""

    @classmethod
    def write(cls, topic: str, duration_s: int = 480, style: str = "educational",
              platform: str = "youtube") -> Script:
        duration_s = max(30, min(duration_s, 3600))
        beats_tpl = STYLE_BEATS[style]

        # allocate time: hook gets fixed 5-15s; remainder weighted by beat role
        weights = []
        for label, name, _ in beats_tpl:
            w = 2.0 if label in ("hook", "cta") else 3.0 if label in ("core", "proof", "act2", "twist", "solution") else 1.6
            if platform in ("tiktok", "shorts") and label in ("context", "setup", "act1"):
                w = 0.8
            weights.append(w)
        total_w = sum(weights)
        avail = duration_s - (5 if duration_s < 90 else 12)  # hook time
        time_slices = [max(6, int(avail * w / total_w)) for w in weights]

        beats = []
        t = 0
        hook_line = beats_tpl[0][2].format(topic=topic)[:110]
        for (label, name, content), dur in zip(beats_tpl, time_slices):
            start, end = t, t + dur
            t = end
            ts = f"{start//60}:{start%60:02d}-{end//60}:{end%60:02d}"
            tactic = ""
            if label in ("hook",):
                tactic = "first 5s: visual change every beat; no logos, no intros"
            elif label in ("core", "act2", "proof", "solution"):
                tactic = "drop-off point: insert an open loop ('the third mistake is the expensive one')"
            elif label in ("mistakes", "payoff", "resolution"):
                tactic = "pattern break: change camera angle/location; speed up 5%"
            elif label == "cta":
                tactic = "end-screen pointing LEFT at the next video, not up at subscribe"
            beats.append(Beat(ts, name, content.format(topic=topic), tactic))

        promise = f"By the end you'll know: how {topic} actually works, the 3 mistakes that cost the most, and the 60-second fix."

        cta = {
            "youtube": [f"Full teardown of {topic} (the 2,000-word version) — link in description.",
                        "Next video: the {topic} failure nobody talks about — 2 minutes, worth it."],
            "tiktok": [f"Part 2 tomorrow: the {topic} mistake that cost me a week — follow so you don't miss it.",
                       "Comment '{topic}' and I'll send the checklist."],
            "shorts": [f"Longer version on the channel: the full {topic} teardown.",
                       "Comment which mistake you've made — I read all of them."],
            "linkedin": [f"I wrote the full {topic} playbook — link in comments (algorithms punish external links in body).",
                         "What did I miss about {topic}? Disagreements welcome in comments."],
        }[platform]

        broll = [
            "hook: fast-cut b-roll of the end state (destination-first editing)",
            "core: diagram building on-screen piece by piece (not a static slide)",
            "proof: real screen recording, cursor visible, speed-ramped boring parts",
            "mistakes: red-circle annotations on the exact failing line/value",
        ]

        cutdowns = []
        if platform == "youtube" and duration_s >= 240:
            cutdowns.append({"platform": "tiktok/shorts", "duration": "45-60s",
                             "cut": "hook + ONE mistake + payoff line; end with 'full version on channel'"})
            cutdowns.append({"platform": "linkedin", "duration": "90s text",
                             "cut": "hook + the counterintuitive chart + one-line CTA to the video"})
        elif platform in ("tiktok", "shorts"):
            cutdowns.append({"platform": "youtube long-form", "duration": "8-10 min",
                             "cut": "expand the open loop from the hook into the full teardown"})
        else:
            cutdowns.append({"platform": "x thread", "duration": "6 tweets",
                             "cut": "each beat becomes one tweet; the hook becomes tweet 1 verbatim"})

        guards = [
            f"Design check: at 0:{'30' if duration_s < 120 else '45'} the viewer must have received value ALREADY (no matter where they leave).",
            "Audio pattern break every 25-35s (music duck, sfx, or voice pace change).",
            f"Total script length target: ~{int(duration_s * 2.3)} words at conversational pace (~140 wpm).",
        ]

        verdict = f"{style} script for {platform} | {duration_s}s | {len(beats)} beats | cutdowns: {len(cutdowns)}"
        return Script(topic, hook_line, promise, beats, cta, broll, cutdowns, guards, verdict)

    @staticmethod
    def format_script(s: Script) -> str:
        out = ["=" * 62, "SCRIPT WRITER AGENT — SCRIPT", "=" * 62, s.verdict, "-" * 62,
               f"HOOK (first 5s): {s.hook}",
               f"PROMISE: {s.promise}", "-" * 62, "Beats:"]
        for b in s.beats:
            out.append(f"  [{b.timestamp}] {b.label.upper()} — {b.content[:90]}")
            if b.retention_tactic:
                out.append(f"      retention: {b.retention_tactic}")
        out += ["-" * 62, "CTA variants:"] + [f"  * {c}" for c in s.cta_variants]
        out += ["-" * 62, "B-roll cues:"] + [f"  * {b}" for b in s.broll]
        out += ["-" * 62, "Platform cutdowns:"]
        for c in s.cutdowns:
            out.append(f"  {c['platform']} ({c['duration']}): {c['cut']}")
        out += ["-" * 62, "Drop-off guards:"] + [f"  ! {g}" for g in s.drop_off_guards]
        out.append("=" * 62)
        return "\n".join(out)
