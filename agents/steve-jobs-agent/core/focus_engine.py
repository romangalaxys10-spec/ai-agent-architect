"""
Steve Jobs Focus Engine.
Wraps the SteveJobsLens with the Focus Filter (say NO to 1,000 things),
Rule of Three feature triage, pitch clarity linting, and binary verdicts.
"""

from dataclasses import dataclass
from typing import Dict, List, Any
import os
import sys

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def _load_repo_module(name: str, relpath: str):
    """Load a repo-level module by explicit path (avoids 'core' package name clash)."""
    import importlib.util

    path = os.path.join(_REPO_ROOT, relpath)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_lens_mod = _load_repo_module("steve_jobs_lens", "core/steve_jobs_lens.py")
SteveJobsLens = _lens_mod.SteveJobsLens
QualityVerdict = _lens_mod.QualityVerdict
ProductReview = _lens_mod.ProductReview

BUZZWORDS = [
    "synergistic", "paradigm", "hyper-scalable", "leveraging", "next-gen",
    "disruptive", "revolutionary", "game-changing", "cutting-edge", "seamless",
]


@dataclass
class FocusAudit:
    product_name: str
    pitch: str
    feature_count: int
    kept_pillars: List[str]
    cut_list: List[str]
    pitch_buzzwords: List[str]
    pitch_word_count: int
    binary_verdict: str
    rationale: str


class SteveJobsFocusEngine:
    """Focus filter + Rule of Three + binary quality verdicts."""

    @classmethod
    def audit(cls, product_name: str, pitch: str, features: List[str]) -> FocusAudit:
        review: ProductReview = SteveJobsLens.evaluate_product(
            product_name=product_name,
            feature_list=features,
            one_sentence_pitch=pitch,
            user_journey_steps=3,
            controls_whole_stack=True,
        )
        found_buzz = [b for b in BUZZWORDS if b in pitch.lower()]
        return FocusAudit(
            product_name=product_name,
            pitch=pitch,
            feature_count=len(features),
            kept_pillars=review.three_core_pillars,
            cut_list=review.focus_cut_list,
            pitch_buzzwords=found_buzz,
            pitch_word_count=len(pitch.split()),
            binary_verdict=review.quality_verdict.value,
            rationale=review.verdict_rationale,
        )

    @classmethod
    def format_audit(cls, audit: FocusAudit) -> str:
        lines = [
            f"# Steve Jobs Focus Audit: {audit.product_name}",
            f"Pitch ({audit.pitch_word_count} words): \"{audit.pitch}\"",
            f"Binary Verdict: {audit.binary_verdict}",
            "",
            f"## The Three Pillars (everything else is cut)",
        ]
        lines += [f"{i + 1}. {p}" for i, p in enumerate(audit.kept_pillars)]
        if audit.cut_list:
            lines.append("\n## Focus Cut List (saying NO)")
            lines += [f"- CUT: {c}" for c in audit.cut_list]
        if audit.pitch_buzzwords:
            lines.append("\n## Pitch Lint")
            lines += [f"- Buzzword detected: '{b}'" for b in audit.pitch_buzzwords]
        else:
            lines.append("\n## Pitch Lint\n- Clean: zero buzzwords.")
        if audit.pitch_word_count > 15:
            lines.append(f"- Too long: {audit.pitch_word_count} words (max 15).")
        lines.append(f"\n## Rationale\n{audit.rationale}")
        return "\n".join(lines)
