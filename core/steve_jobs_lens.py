"""
Steve Jobs Product Mindset Engine.
Implements the 6 Core Mental Models, 8 Decision Heuristics, Focus Filter (1000-to-1),
The Whole Widget (End-to-End Control), and Radical Binary Quality Verdicts.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Tuple


class QualityVerdict(str, Enum):
    INSANELY_GREAT = "INSANELY_GREAT"
    PASSABLE_BUT_NEEDS_RADICAL_SIMPLIFICATION = "NEEDS_RADICAL_SIMPLIFICATION"
    TOTAL_BULLSHIT = "TOTAL_BULLSHIT"


@dataclass
class ProductReview:
    one_sentence_headline: str
    quality_verdict: QualityVerdict
    focus_cut_list: List[str]
    whole_widget_integrity: float  # 0.0 to 1.0
    aesthetic_and_invisible_craft: str
    three_core_pillars: List[str]
    verdict_rationale: str


class SteveJobsLens:
    """
    Evaluates agents, codebases, APIs, and product designs through the Steve Jobs Mental Operating System.
    """

    @staticmethod
    def evaluate_product(
        product_name: str,
        feature_list: List[str],
        one_sentence_pitch: str,
        user_journey_steps: int,
        controls_whole_stack: bool,
    ) -> ProductReview:
        """
        Runs rigorous inspection:
        1. Focus: Does it say No to 1,000 things?
        2. Whole Widget: Does it control the user experience from end-to-end?
        3. One Sentence Clarity: Can a human understand it instantly without buzzwords?
        4. Simplicity: Are there extraneous user journey steps?
        """
        # 1. Evaluate Pitch Clarity
        buzzwords = ["synergistic", "paradigm", "hyper-scalable", "leveraging", "next-gen", "disruptive"]
        pitch_clean = not any(b in one_sentence_pitch.lower() for b in buzzwords)
        pitch_short = len(one_sentence_pitch.split()) <= 15

        # 2. Focus & Cut List
        # If there are more than 3 primary features, the rest MUST be cut.
        keep_features = feature_list[:3]
        cut_list = feature_list[3:] if len(feature_list) > 3 else []

        # 3. Whole Widget Integrity
        whole_widget_score = 1.0 if controls_whole_stack else 0.5
        if user_journey_steps > 3:
            whole_widget_score -= 0.2 * (user_journey_steps - 3)
        whole_widget_score = max(0.1, min(1.0, whole_widget_score))

        # 4. Verdict Assignment
        if pitch_clean and pitch_short and len(cut_list) == 0 and whole_widget_score >= 0.85:
            verdict = QualityVerdict.INSANELY_GREAT
            headline = f"Boom. {product_name} is pure, sharp, and revolutionary."
            rationale = "Radical focus achieved. Controls the whole widget with zero superfluous steps."
        elif whole_widget_score < 0.4 or len(feature_list) > 10:
            verdict = QualityVerdict.TOTAL_BULLSHIT
            headline = f"This is a bozo design. {product_name} is drowning in committee compromises."
            rationale = "Lacks taste. Too many features, fragmented stack control, and zero soul."
        else:
            verdict = QualityVerdict.PASSABLE_BUT_NEEDS_RADICAL_SIMPLIFICATION
            headline = f"{product_name} has a kernel of brilliance, but you must cut 80% of the clutter."
            rationale = f"Focus on the 3 core pillars: {', '.join(keep_features)}. Cut the remaining {len(cut_list)} distractions."

        pillars = keep_features if keep_features else [product_name]
        while len(pillars) < 3:
            pillars.append("Uncompromising Simplicity")

        return ProductReview(
            one_sentence_headline=headline,
            quality_verdict=verdict,
            focus_cut_list=cut_list,
            whole_widget_integrity=round(whole_widget_score, 2),
            aesthetic_and_invisible_craft="The back of the fence must be painted as beautifully as the front.",
            three_core_pillars=pillars[:3],
            verdict_rationale=rationale,
        )

    @staticmethod
    def format_review_markdown(review: ProductReview) -> str:
        """Renders review in signature Jobsian presentation style."""
        return f"""# Product Architecture Review

> **"{review.one_sentence_headline}"**

### Quality Verdict: `{review.quality_verdict.value}`
**Stack Integrity (The Whole Widget):** `{int(review.whole_widget_integrity * 100)}%`

---

### The Three Core Pillars (The Rule of Three):
1. **{review.three_core_pillars[0]}**
2. **{review.three_core_pillars[1]}**
3. **{review.three_core_pillars[2]}**

---

### What to Cut Immediately (Focus = Saying NO):
{chr(10).join(f"- ❌ Cut: `{f}`" for f in review.focus_cut_list) if review.focus_cut_list else "- ✅ No unnecessary bloat detected. Pure focus."}

---

### Craft & Invisible Details:
_{review.aesthetic_and_invisible_craft}_

**Verdict Rationale:**
{review.verdict_rationale}
"""
