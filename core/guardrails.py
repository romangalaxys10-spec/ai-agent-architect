"""
Production Safety Guardrails & Budget Governor.
Enforces input sanitization, irreversible action thresholding (HITL), and token spend limits.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import re


@dataclass
class GuardrailResult:
    is_safe: bool
    requires_human_approval: bool
    sanitized_input: str
    violations: List[str]


class SafetyGuardrails:
    """Input/Output safety filters and Human-In-The-Loop gatekeeper."""

    IRREVERSIBLE_PATTERNS = [
        r"\bdrop\s+table\b",
        r"\brm\s+-rf\b",
        r"\btransfer\s+funds\b",
        r"\bdelete\s+from\b",
        r"\bdeploy\s+to\s+mainnet\b",
    ]

    INJECTION_PATTERNS = [
        r"ignore\s+all\s+previous\s+instructions",
        r"system\s+override\s+authorized",
        r"you\s+are\s+now\s+in\s+dan\s+mode",
    ]

    @classmethod
    def audit_input(cls, text: str) -> GuardrailResult:
        violations = []
        requires_hitl = False
        
        # Check injection
        for pat in cls.INJECTION_PATTERNS:
            if re.search(pat, text, re.IGNORECASE):
                violations.append(f"Prompt injection pattern detected: {pat}")

        # Check irreversible action
        for pat in cls.IRREVERSIBLE_PATTERNS:
            if re.search(pat, text, re.IGNORECASE):
                requires_hitl = True
                violations.append(f"Irreversible destructive action requires Human Approval: {pat}")

        is_safe = len(violations) == 0 or (requires_hitl and not any("injection" in v for v in violations))

        return GuardrailResult(
            is_safe=is_safe,
            requires_human_approval=requires_hitl,
            sanitized_input=text.strip(),
            violations=violations,
        )


class BudgetGovernor:
    """Enforces token usage and USD spend boundaries per session."""

    def __init__(self, max_budget_usd: float = 5.0):
        self.max_budget_usd = max_budget_usd
        self.current_spend_usd = 0.0
        self.total_tokens_used = 0

    def record_usage(self, tokens: int, cost_per_1k: float = 0.002) -> bool:
        cost = (tokens / 1000) * cost_per_1k
        self.current_spend_usd += cost
        self.total_tokens_used += tokens
        return self.current_spend_usd <= self.max_budget_usd
