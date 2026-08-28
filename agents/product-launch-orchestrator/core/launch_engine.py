"""
Product Launch Orchestrator Engine.
Generates full multi-channel launch campaigns for GitHub repositories, Show HN, Product Hunt, and developer forums.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


@dataclass
class LaunchCampaign:
    product_name: str
    tagline: str
    show_hn_post: str
    product_hunt_pitch: Dict[str, str]
    reddit_developer_post: str
    three_day_timeline: List[Dict[str, str]]


class ProductLaunchOrchestrator:
    """Coordinates and crafts multi-platform launch campaigns."""

    @classmethod
    def generate_launch_package(
        cls,
        product_name: str,
        github_url: str,
        core_differentiator: str = "100% Credit-Free Local Design Engine with Zero AI Slop",
    ) -> LaunchCampaign:
        # 1. Show HN
        show_hn = f"""Show HN: {product_name} – {core_differentiator}

Hey HN,

I built {product_name} because I was tired of existing AI design tools charging monthly subscriptions for metered credits and outputting the same generic purple-gradient Inter-font slop.

What it does:
• 100% Free & Local: Standalone Python engine generating responsive Tailwind sites, 16:9 keynote decks, and hardware telemetry HUDs.
• Built-in Anti-Slop Linter: Rejects generic AI clichés and enforces Swiss Bauhaus typography and tactile depth.
• Complete Parity: Includes codebase context scanning and React TSX component export.

Source code and live demos: {github_url}

Would love feedback on the architecture!"""

        # 2. Product Hunt
        ph_pitch = {
            "tagline": "The Anti-AI-Slop Autonomous Design & Presentation Engine",
            "maker_comment": f"Hey Product Hunt! 👋 We built {product_name} to give developers an autonomous design engine that requires zero paid credits and enforces uncompromising aesthetic taste. Check out the open-source repo: {github_url}",
            "topics": "Developer Tools, Open Source, Artificial Intelligence, Web Design"
        }

        # 3. Reddit Post
        reddit_post = f"""[Open Source] Built a tool to generate websites and keynote decks without AI slop

Tired of cookie-cutter AI designs that look identical? 

I open-sourced {product_name} — an autonomous engine that uses Swiss Bauhaus asymmetric grids, Teenage Engineering hardware layouts, and bespoke typography pairings instead of generic Dribbble gradients.

GitHub: {github_url}
Zero credits required, runs 100% locally."""

        # 4. 3-Day Schedule
        timeline = [
            {"day": "Day -1 (Teaser)", "action": "Post short 15-second benchmark video on X showing zero-credit site generation."},
            {"day": "Day 0 (Launch Blitz)", "action": "Submit Show HN (08:00 EST), Product Hunt launch, publish X announcement thread."},
            {"day": "Day +1 (Follow-up)", "action": "Post technical architecture breakdown on r/LocalLLaMA and LinkedIn with benchmark graphs."},
        ]

        return LaunchCampaign(
            product_name=product_name,
            tagline=core_differentiator,
            show_hn_post=show_hn,
            product_hunt_pitch=ph_pitch,
            reddit_developer_post=reddit_post,
            three_day_timeline=timeline,
        )
