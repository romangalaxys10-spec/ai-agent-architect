"""
Retry, backoff and circuit-breaking for LLM + tool calls.

Doctrine (GeneArnold M4 + bryanyzhu Ch.17):
- Rate limits / transient timeouts: retry with exponential backoff + jitter.
- Logic errors / auth errors: fail fast, surface as message to the model.
- Circuit breaker prevents doom-retry against a dying dependency.
"""

from __future__ import annotations

import random
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, TypeVar

T = TypeVar("T")


class CircuitOpenError(RuntimeError):
    """Raised when the circuit breaker is open and the call is short-circuited."""


@dataclass
class RetryPolicy:
    max_attempts: int = 3
    base_delay: float = 0.05          # seconds; small for tests
    max_delay: float = 2.0
    jitter: bool = True
    retryable_check: Optional[Callable[[Exception], bool]] = None

    def delay_for(self, attempt: int) -> float:
        d = min(self.base_delay * (2 ** attempt), self.max_delay)
        if self.jitter:
            d *= 0.5 + random.random()
        return d


def with_retries(
    fn: Callable[[], T],
    policy: Optional[RetryPolicy] = None,
    sleep: Callable[[float], None] = time.sleep,
    on_error: Optional[Callable[[int, Exception], None]] = None,
) -> T:
    """Execute fn with bounded retry. Non-retryable errors raise immediately."""
    policy = policy or RetryPolicy()
    last_exc: Optional[Exception] = None
    for attempt in range(policy.max_attempts):
        try:
            return fn()
        except Exception as exc:
            last_exc = exc
            retryable = policy.retryable_check(exc) if policy.retryable_check else True
            if not retryable or attempt == policy.max_attempts - 1:
                raise
            if on_error:
                on_error(attempt, exc)
            sleep(policy.delay_for(attempt))
    raise last_exc  # unreachable, satisfies type-checkers


class CircuitBreaker:
    """
    Classic half-open circuit breaker keyed by dependency name.
    OPEN after `failure_threshold` consecutive failures within `window_seconds`;
    switches to HALF_OPEN after `reset_timeout`; one success closes it again.
    """

    def __init__(self, failure_threshold: int = 5, reset_timeout: float = 30.0, window_seconds: float = 60.0):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.window_seconds = window_seconds
        self._state: Dict[str, str] = {}
        self._failures: Dict[str, List[float]] = {}
        self._opened_at: Dict[str, float] = {}
        self._lock = threading.Lock()

    def state(self, name: str) -> str:
        with self._lock:
            if self._state.get(name) == "open":
                if time.time() - self._opened_at.get(name, 0) >= self.reset_timeout:
                    self._state[name] = "half-open"
                    self._failures[name] = []
                    return "half-open"
            return self._state.get(name, "closed")

    def record_success(self, name: str) -> None:
        with self._lock:
            self._state[name] = "closed"
            self._failures[name] = []

    def record_failure(self, name: str) -> None:
        with self._lock:
            now = time.time()
            fails = [t for t in self._failures.get(name, []) if now - t <= self.window_seconds]
            fails.append(now)
            self._failures[name] = fails
            if len(fails) >= self.failure_threshold:
                self._state[name] = "open"
                self._opened_at[name] = now

    def allow(self, name: str) -> bool:
        return self.state(name) != "open"

    def call(self, name: str, fn: Callable[[], T]) -> T:
        if not self.allow(name):
            raise CircuitOpenError(f"Circuit open for '{name}'; short-circuiting call.")
        try:
            result = fn()
        except CircuitOpenError:
            raise
        except Exception:
            self.record_failure(name)
            raise
        self.record_success(name)
        return result
