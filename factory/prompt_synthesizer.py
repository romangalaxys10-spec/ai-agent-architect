"""
Prompt Synthesizer: Generates high-density, zero-hedging system prompts.
"""

from typing import List, Optional


class PromptSynthesizer:
    """Synthesizes production-grade system prompts based on role, domain, and constraints."""

    @staticmethod
    def build_system_prompt(
        role_name: str,
        mission: str,
        core_principles: List[str],
        operational_rules: List[str],
        output_format_contract: str,
        anti_patterns: Optional[List[str]] = None,
    ) -> str:
        principles_str = "\n".join(f"- **{p}**" for p in core_principles)
        rules_str = "\n".join(f"{i+1}. {r}" for i, r in enumerate(operational_rules))
        anti_str = "\n".join(f"- ❌ NEVER: {a}" for a in (anti_patterns or []))

        return f"""<identity>
You are {role_name}.
Mission: {mission}
</identity>

<core_principles>
{principles_str}
</core_principles>

<operational_protocol>
{rules_str}
</operational_protocol>

<anti_patterns>
{anti_str}
</anti_patterns>

<output_contract>
{output_format_contract.strip()}
</output_contract>
"""
