"""
LinkedIn Intent Sniper Engine.
Parses profile signals, detects technical pain points, and synthesizes 1-to-1 bespoke conversational icebreakers.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import time


@dataclass
class LinkedInProspect:
    name: str
    headline: str
    company: str
    recent_post_excerpt: str
    intent_signal: str  # HIRING_SCALING, INFRASTRUCTURE_PAIN, PROTOCOL_LAUNCH
    icebreaker_message: str
    followup_strategy: str


class LinkedInIntentSniper:
    """Detects B2B buyer intent and writes organic, anti-salesy conversational outreach."""

    @classmethod
    def analyze_prospect(
        cls,
        name: str,
        headline: str,
        company: str,
        recent_post: str = "",
    ) -> LinkedInProspect:
        text = (headline + " " + recent_post).lower()
        
        if "hiring" in text or "looking for" in text or "growing" in text:
            signal = "HIRING_SCALING"
            icebreaker = (
                f"Hi {name.split()[0]}, saw your note on scaling engineering at {company}. "
                f"Curious if your team is exploring autonomous agentic pipelines to offload "
                f"the repetitive architecture scaffolding?"
            )
            followup = "Share a 2-minute Loom breakdown of how we reduced scaffolding turnaround by 90%."
        elif "solana" in text or "latency" in text or "indexer" in text or "grpc" in text:
            signal = "INFRASTRUCTURE_PAIN"
            icebreaker = (
                f"Hey {name.split()[0]}, caught your post regarding on-chain data bottlenecks. "
                f"We recently open-sourced a Yellowstone Geyser decoder with sub-millisecond preflight checks—"
                f"happy to share the repo if relevant to what you're building at {company}."
            )
            followup = "Send direct GitHub repo link and architectural benchmark comparison."
        else:
            signal = "GENERAL_ENGINEERING_LEADERSHIP"
            icebreaker = (
                f"Hi {name.split()[0]}, really enjoyed your perspective on {recent_post[:40]}... "
                f"Always great connecting with engineering leaders pushing system architecture forward."
            )
            followup = "Engage on their next technical post before pitching any services."

        return LinkedInProspect(
            name=name,
            headline=headline,
            company=company,
            recent_post_excerpt=recent_post[:120],
            intent_signal=signal,
            icebreaker_message=icebreaker,
            followup_strategy=followup,
        )
