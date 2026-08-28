"""
Production Reliability Kit.

Doctrine (2024-2025 SOTA synthesis):
- Three non-convertible budget currencies: steps, tokens, wall-clock seconds.
  Advertised budget (told to the model) + enforced ceiling (hard runtime cap).
- Loop detection distinguishes repetition / stagnation / cycling, using
  canonicalized tool-call fingerprints (volatile keys stripped).
- Idempotency keys + a dedup ledger make side-effecting tool calls replay-safe.
- Per-tool failure policies: compensate / reconcile / refuse (never blind retry).
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Budgets: three non-convertible currencies
# ---------------------------------------------------------------------------

class BudgetExceededError(RuntimeError):
    def __init__(self, currency: str, spent: float, ceiling: float):
        super().__init__(f"Budget exceeded [{currency}]: {spent} > {ceiling}")
        self.currency = currency
        self.spent = spent
        self.ceiling = ceiling


@dataclass
class Budget:
    """One currency: advertised (shown to model) + enforced (hard ceiling)."""
    currency: str  # "steps" | "tokens" | "seconds"
    advertised: float
    enforced: float
    _spent: float = 0.0

    @property
    def spent(self) -> float:
        return self._spent

    @property
    def exceeded(self) -> bool:
        return self._spent > self.enforced

    @property
    def near_limit(self) -> bool:
        return self._spent >= self.advertised

    def spend(self, amount: float) -> None:
        self._spent += amount
        if self.exceeded:
            raise BudgetExceededError(self.currency, self._spent, self.enforced)

    def summary(self) -> Dict[str, Any]:
        return {
            "currency": self.currency,
            "spent": self._spent,
            "advertised": self.advertised,
            "enforced": self.enforced,
            "near_limit": self.near_limit,
            "exceeded": self.exceeded,
        }


@dataclass
class BudgetPortfolio:
    """
    The three-currency budget portfolio with an advertised-prompt fragment so
    the model can pace itself, plus a hard backstop that kills runaway runs.
    """
    max_steps: int = 25
    max_tokens: int = 200_000
    max_seconds: float = 600.0
    _budgets: Dict[str, Budget] = field(default_factory=dict, init=False)
    started_at: float = field(default_factory=time.time, init=False)

    def __post_init__(self) -> None:
        self._budgets = {
            "steps": Budget("steps", advertised=self.max_steps * 0.8, enforced=self.max_steps),
            "tokens": Budget("tokens", advertised=self.max_tokens * 0.8, enforced=self.max_tokens),
            "seconds": Budget("seconds", advertised=self.max_seconds * 0.8, enforced=self.max_seconds),
        }

    def tick_step(self) -> None:
        self._budgets["steps"].spend(1)

    def tick_tokens(self, n: int) -> None:
        self._budgets["tokens"].spend(n)

    def tick_wallclock(self) -> None:
        self._budgets["seconds"].spend(time.time() - self.started_at - self._budgets["seconds"].spent)

    def check(self) -> None:
        self.tick_wallclock()
        for b in self._budgets.values():
            if b.exceeded:
                raise BudgetExceededError(b.currency, b.spent, b.enforced)

    def advertised_prompt_fragment(self) -> str:
        return (
            f"Budget: you have approximately {self._budgets['steps'].advertised:.0f} steps, "
            f"{self._budgets['tokens'].advertised:.0f} tokens and "
            f"{self._budgets['seconds'].advertised:.0f} seconds. Wind down gracefully and "
            "summarize what remains before exhaustion."
        )

    def summary(self) -> Dict[str, Any]:
        self.tick_wallclock()
        return {b.currency: b.summary() for b in self._budgets.values()}


# ---------------------------------------------------------------------------
# Loop detection: repetition / stagnation / cycling
# ---------------------------------------------------------------------------

VOLATILE_KEYS = {"request_id", "timestamp", "attempt", "trace_id", "nonce", "ts", "time", "idempotency_key"}


def canonicalize_call(name: str, arguments: Dict[str, Any]) -> str:
    """Strip volatile keys, sort keys — aggressive canonicalization so models
    cannot evade fingerprints by shuffling noise fields."""
    cleaned = {k: v for k, v in arguments.items() if k not in VOLATILE_KEYS}
    blob = json.dumps({"name": name, "args": cleaned}, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


class LoopDetector:
    """
    Graduated response ladder (Inform -> Constrain -> Escalate) over a sliding
    window of canonicalized tool-call fingerprints.
    """

    def __init__(self, window: int = 8, repeat_threshold: int = 3, stagnation_limit: int = 6):
        self.window = window
        self.repeat_threshold = repeat_threshold
        self.stagnation_limit = stagnation_limit
        self._recent: List[str] = []
        self._progress_updates: int = 0
        self._inject_messages: List[str] = []

    def observe(self, tool_name: str, arguments: Dict[str, Any]) -> None:
        fp = canonicalize_call(tool_name, arguments)
        self._recent.append(fp)
        if len(self._recent) > self.window:
            self._recent.pop(0)

    def note_progress(self) -> None:
        """Call when externally-checkable progress occurs (new artifacts, state deltas)."""
        self._progress_updates += 1

    @property
    def repetition(self) -> bool:
        if len(self._recent) < self.repeat_threshold:
            return False
        return self._recent[-1] == self._recent[-2] == self._recent[-3]

    @property
    def stagnation(self) -> bool:
        """No progress predicate flips AND same fingerprints keep rotating."""
        if len(self._recent) < self.stagnation_limit:
            return False
        return len(set(self._recent[-self.stagnation_limit :])) <= 2 and self._progress_updates == 0

    @property
    def cycling(self) -> bool:
        """State hash repeats: A B A B pattern in fingerprints."""
        if len(self._recent) < 4:
            return False
        tail = self._recent[-4:]
        return tail[0] == tail[2] and tail[1] == tail[3] and tail[0] != tail[1]

    def verdict(self) -> Optional[Dict[str, str]]:
        """Returns {'level': 'inform|constrain|escalate', 'reason': ...} or None.
        Priority: escalation-worthy conditions checked first — a repetition
        'inform' must never mask a stagnation 'escalate'."""
        if self.stagnation:
            return {
                "level": "escalate",
                "reason": "No measurable progress across recent steps. Terminating before budget waste.",
            }
        if self.cycling:
            return {
                "level": "constrain",
                "reason": "Cyclical tool pattern detected (A,B,A,B). The alternating calls cannot converge.",
            }
        if self.repetition:
            return {
                "level": "inform",
                "reason": f"You have called this tool {self.repeat_threshold}+ times with identical arguments. "
                "Change strategy or arguments.",
            }
        return None

    def drain_injections(self) -> List[str]:
        msgs = self._inject_messages
        self._inject_messages = []
        return msgs


# ---------------------------------------------------------------------------
# Idempotency ledger
# ---------------------------------------------------------------------------

class IdempotencyLedger:
    """Dedup store for side-effecting calls: same key -> replay cached result."""

    def __init__(self) -> None:
        self._store: Dict[str, Any] = {}

    @staticmethod
    def key(tool_name: str, arguments: Dict[str, Any]) -> str:
        return f"{tool_name}:{canonicalize_call(tool_name, arguments)}"

    def seen(self, key: str) -> bool:
        return key in self._store

    def record(self, key: str, result: Any) -> None:
        self._store[key] = {"result": result, "ts": time.time()}

    def cached(self, key: str) -> Any:
        return self._store.get(key, {}).get("result")


# ---------------------------------------------------------------------------
# Per-tool failure policy
# ---------------------------------------------------------------------------

class FailurePolicy(str, Enum):
    COMPENSATE = "compensate"  # semantic inverse exists (needs own retries)
    RECONCILE = "reconcile"    # read world state and converge
    REFUSE = "refuse"          # irreversible (email sent, payment cleared) — never auto-retry


@dataclass
class ToolFailure:
    tool: str
    error: str
    policy: FailurePolicy
    action_taken: str


class FailurePolicyEngine:
    """
    Applies the per-tool policy on failure:
    - compensate: invoke registered inverse, then report
    - reconcile: invoke registered convergence check
    - refuse: never auto-retry, escalate to human
    """

    def __init__(self) -> None:
        self._policies: Dict[str, FailurePolicy] = {}
        self._compensators: Dict[str, Callable[[Dict[str, Any]], Any]] = {}
        self._reconcilers: Dict[str, Callable[[], Any]] = {}
        self.failures: List[ToolFailure] = []

    def register(
        self,
        tool: str,
        policy: FailurePolicy,
        compensator: Optional[Callable[[Dict[str, Any]], Any]] = None,
        reconciler: Optional[Callable[[], Any]] = None,
    ) -> None:
        self._policies[tool] = policy
        if compensator:
            self._compensators[tool] = compensator
        if reconciler:
            self._reconcilers[tool] = reconciler

    def handle(self, tool: str, error: str, arguments: Dict[str, Any]) -> ToolFailure:
        policy = self._policies.get(tool, FailurePolicy.REFUSE)
        if policy == FailurePolicy.COMPENSATE and tool in self._compensators:
            try:
                self._compensators[tool](arguments)
                action = "compensation executed"
            except Exception as exc:
                action = f"compensation failed: {exc}"
        elif policy == FailurePolicy.RECONCILE and tool in self._reconcilers:
            try:
                state = self._reconcilers[tool]()
                action = f"reconciled world state: {state}"
            except Exception as exc:
                action = f"reconciliation failed: {exc}"
        else:
            action = "escalated to human (irreversible or uncompensated failure)"
        failure = ToolFailure(tool=tool, error=error, policy=policy, action_taken=action)
        self.failures.append(failure)
        return failure


# ---------------------------------------------------------------------------
# Termination: externally checkable success predicate
# ---------------------------------------------------------------------------

@dataclass
class TerminationCriteria:
    """
    Goal satisfaction must be an externally checkable predicate over observable
    state ("file exists and parses"), never the agent's self-report.
    Three independent endings: success predicate, budget exhaustion, guard trip.
    """
    success_predicate: Optional[Callable[[], bool]] = None
    on_budget_exhausted: str = "degrade"  # degrade | escalate | abort
    on_guard_tripped: str = "abort"

    def evaluate(self) -> Optional[str]:
        if self.success_predicate and self.success_predicate():
            return "success"
        return None
