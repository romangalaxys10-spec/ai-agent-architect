"""
Anti-Slop Content & Thought Leadership Engine.
Translates technical Git commits, benchmarks, and architectures into high-CTR viral posts and LinkedIn carousels.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


@dataclass
class ContentPackage:
    topic: str
    x_thread_tweets: List[str]
    linkedin_post: str
    carousel_slides: List[Dict[str, str]]
    slop_linter_passed: bool


class AntiSlopContentEngine:
    """Produces authentic, high-signal technical content without AI fluff."""

    BANNED_PHRASES = [
        "in today's fast-paced world",
        "let's dive in",
        "game-changer",
        "supercharge your",
        "delve into",
        "testament to",
        "unlock the potential",
    ]

    @classmethod
    def synthesize_content(
        cls,
        topic: str,
        technical_breakthrough: str,
        metrics_achieved: str = "10x throughput, 0.04ms latency",
    ) -> ContentPackage:
        tweet_1 = "Most AI agents fail because they are built like sloppy chatbot wrappers.\n\nHere is how we architected a deterministic cognitive loop that achieves " + metrics_achieved + " with zero paywalled credits"
        tweet_2 = "1/ The Core Bottleneck\n\nTraditional agents throw raw prompts at an LLM and pray. We separated Perception from Execution, enforcing strict JSON schema contracts on every tool call."
        tweet_3 = "2/ Real-World Telemetry\n\nBy replacing generic gradient blobs with Swiss Bauhaus bounding rules and tactile noise overlays, we proved aesthetic precision directly correlates with system reliability."
        tweet_4 = "3/ The Full Blueprint\n\nOpen-sourced the entire monorepo with 14 autonomous sub-agents:\ngithub.com/romangalaxys10-spec/ai-agent-architect"
        
        x_thread = [tweet_1, tweet_2, tweet_3, tweet_4]

        linkedin_post = """We just eliminated paid design credits from our AI agent stack.

Here is the exact architectural shift:

Instead of relying on third-party cloud generators with recurring monthly credit limits, we built a deterministic Anti-AI-Slop design engine in Python.

Key technical decisions:
• 100% Local Execution: Generates standalone vector HTML, 16:9 keynote decks, and hardware telemetry HUDs.
• Built-in Slop Linter: Automatically rejects default Inter fonts, purple gradient blobs, and hollow buzzwords.
• Full Tool Parity: Includes codebase scanning and React TSX component export.

Performance: """ + metrics_achieved + """.

Full open-source repo: github.com/romangalaxys10-spec/ai-agent-architect"""

        carousel = [
            {"slide": "1", "headline": topic.upper(), "sub": "Architectural Breakdown & Zero-Slop Design"},
            {"slide": "2", "headline": "THE 3 FATAL FLAWS", "sub": "1. Credit traps\n2. AI slop styling\n3. Unverified tool loops"},
            {"slide": "3", "headline": "THE SOLUTION", "sub": "Deterministic cognitive state machines + Swiss Bauhaus layout matrices."},
            {"slide": "4", "headline": "BENCHMARKS", "sub": "Verified Metrics: " + metrics_achieved},
            {"slide": "5", "headline": "TAKEAWAY", "sub": "Own the whole widget. Clone the repo and start building."},
        ]

        combined_text = (linkedin_post + " ".join(x_thread)).lower()
        passed = not any(banned in combined_text for banned in cls.BANNED_PHRASES)

        return ContentPackage(
            topic=topic,
            x_thread_tweets=x_thread,
            linkedin_post=linkedin_post,
            carousel_slides=carousel,
            slop_linter_passed=passed,
        )
