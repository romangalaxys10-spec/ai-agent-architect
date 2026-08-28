"""
Multi-LLM Model Bridge & Adaptive Router.
Routes tasks intelligently across GLM-4.7/5.3, Claude 3.7, and free local tiers with unified tool schema translation.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import time


@dataclass
class RoutingDecision:
    task_type: str  # CODE_REFACTOR, ARCHITECTURE, BULK_LOOKUP, CHAT
    selected_model: str
    provider: str  # Z.AI, Anthropic, OpenAI, Local
    estimated_cost_usd: float
    reasoning: str
    token_budget: int


class ModelBridgeRouter:
    """Intelligent adaptive multi-model gateway."""

    MODEL_REGISTRY = {
        "glm-4.7": {"provider": "Z.AI", "cost_per_1k": 0.001, "specialty": "Coding & Fast Pipelines"},
        "glm-5.3": {"provider": "Z.AI", "cost_per_1k": 0.003, "specialty": "Complex Full-Stack Synthesis"},
        "claude-3.7-sonnet": {"provider": "Anthropic", "cost_per_1k": 0.015, "specialty": "Deep Architecture & Reasoning"},
        "local-hermes": {"provider": "Local", "cost_per_1k": 0.000, "specialty": "Bulk Lookups & Extraction"},
    }

    @classmethod
    def route_request(cls, prompt: str, requires_code: bool = True, max_latency_ms: int = 1500) -> RoutingDecision:
        length = len(prompt.split())
        
        if "architect" in prompt.lower() or "security audit" in prompt.lower() or length > 500:
            model = "claude-3.7-sonnet"
            task = "ARCHITECTURE_DEEP_REASONING"
            reason = "High reasoning and structural integrity demanded."
            tokens = 8192
        elif requires_code or "refactor" in prompt.lower() or "write test" in prompt.lower():
            model = "glm-4.7"
            task = "CODE_REFACTOR_HIGH_VELOCITY"
            reason = "Optimal coding speed, tool-calling precision, and cost efficiency."
            tokens = 4096
        else:
            model = "local-hermes"
            task = "BULK_LOOKUP_AND_TEXT"
            reason = "Zero cost local execution."
            tokens = 2048

        meta = cls.MODEL_REGISTRY[model]
        cost = (tokens / 1000) * meta["cost_per_1k"]

        return RoutingDecision(
            task_type=task,
            selected_model=model,
            provider=meta["provider"],
            estimated_cost_usd=round(cost, 5),
            reasoning=reason,
            token_budget=tokens,
        )

    @classmethod
    def normalize_tool_schema(cls, tool_def: Dict[str, Any], target_provider: str = "Z.AI") -> Dict[str, Any]:
        """Translates tool call schemas seamlessly between Anthropic and OpenAI/Z.AI formats."""
        name = tool_def.get("name", "custom_tool")
        description = tool_def.get("description", "")
        params = tool_def.get("parameters", {"type": "object", "properties": {}})

        if target_provider.lower() in {"z.ai", "openai"}:
            return {
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": params,
                }
            }
        else:  # Anthropic format
            return {
                "name": name,
                "description": description,
                "input_schema": params,
            }
