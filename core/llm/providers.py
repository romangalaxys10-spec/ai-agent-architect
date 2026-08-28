"""
Provider-agnostic chat completion interface.

Design doctrine (bryanyzhu Ch.11 "provider abstraction and its leaks"):
- One narrow internal interface; provider quirks absorbed at the adapter boundary.
- Every response carries Usage (tokens + USD) so cost is a first-class runtime metric.
- An offline deterministic EchoProvider guarantees the framework is fully runnable
  and testable with zero API keys (GeneArnold mock-LLM testing doctrine).
- ModelRouter implements the Anthropic "routing" pattern: classify difficulty,
  cascade cheap model -> flagship model.
"""

from __future__ import annotations

import json
import os
import re
import time
import uuid
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence

try:  # Pydantic v2 is a project dependency; degrade gracefully if absent.
    from pydantic import BaseModel

    _HAS_PYDANTIC = True
except Exception:  # pragma: no cover
    BaseModel = object  # type: ignore
    _HAS_PYDANTIC = False


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass
class Message:
    """Universal chat message. Tool calls use OpenAI-style shape internally."""
    role: Role
    content: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None  # [{id, name, arguments}]
    tool_call_id: Optional[str] = None
    name: Optional[str] = None

    def to_openai(self) -> Dict[str, Any]:
        msg: Dict[str, Any] = {"role": self.role.value}
        if self.content is not None:
            msg["content"] = self.content
        if self.tool_calls:
            msg["tool_calls"] = [
                {
                    "id": tc["id"],
                    "type": "function",
                    "function": {"name": tc["name"], "arguments": tc["arguments"]},
                }
                for tc in self.tool_calls
            ]
        if self.tool_call_id is not None:
            msg["tool_call_id"] = self.tool_call_id
        if self.name is not None:
            msg["name"] = self.name
        return msg

    @staticmethod
    def system(text: str) -> "Message":
        return Message(role=Role.SYSTEM, content=text)

    @staticmethod
    def user(text: str) -> "Message":
        return Message(role=Role.USER, content=text)

    @staticmethod
    def assistant(text: str) -> "Message":
        return Message(role=Role.ASSISTANT, content=text)


@dataclass
class Usage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cost_usd: float = 0.0
    model: str = ""

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


@dataclass
class LLMResponse:
    content: Optional[str] = None
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    finish_reason: str = "stop"  # stop | tool_calls | length | content_filter
    usage: Usage = field(default_factory=Usage)
    model: str = ""
    raw: Optional[Any] = None


class LLMError(RuntimeError):
    """Provider failure. Errors are messages, not crashes: callers convert to tool text."""

    def __init__(self, message: str, retryable: bool = False, provider: str = ""):
        super().__init__(message)
        self.retryable = retryable
        self.provider = provider


# ---------------------------------------------------------------------------
# Tool declaration helpers (shared JSON-schema shape, provider-neutral)
# ---------------------------------------------------------------------------

def tool_declaration(name: str, description: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Provider-neutral tool declaration: JSON-Schema `parameters` object."""
    return {"name": name, "description": description, "parameters": parameters}


# ---------------------------------------------------------------------------
# Model profiles: "model profiles, not model names"
# ---------------------------------------------------------------------------

@dataclass
class ModelProfile:
    """A profile bundles a model id + tier + pricing so routing/cost logic is declarative."""
    name: str
    tier: str  # nano | small | workhorse | flagship | local
    input_cost_per_1k: float = 0.0
    output_cost_per_1k: float = 0.0
    context_window: int = 128_000
    supports_tools: bool = True

    def cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        return (
            prompt_tokens / 1000 * self.input_cost_per_1k
            + completion_tokens / 1000 * self.output_cost_per_1k
        )


MODEL_CATALOG: Dict[str, ModelProfile] = {
    p.name: p
    for p in [
        ModelProfile("echo-local", "local", 0.0, 0.0, 1_000_000),
        ModelProfile("gpt-4o-mini", "small", 0.00015, 0.0006),
        ModelProfile("gpt-4o", "workhorse", 0.0025, 0.01),
        ModelProfile("claude-sonnet", "workhorse", 0.003, 0.015),
        ModelProfile("claude-opus", "flagship", 0.015, 0.075),
        ModelProfile("glm-4.7", "workhorse", 0.001, 0.003),
        ModelProfile("glm-5.3", "flagship", 0.004, 0.012),
        ModelProfile("deepseek-chat", "small", 0.00014, 0.00028),
    ]
}


# ---------------------------------------------------------------------------
# Base provider
# ---------------------------------------------------------------------------

class LLMProvider:
    """Minimal chat-completion interface every provider must implement."""

    name = "base"

    def complete(
        self,
        messages: Sequence[Message],
        model: str = "echo-local",
        tools: Optional[Sequence[Dict[str, Any]]] = None,
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> LLMResponse:
        raise NotImplementedError

    def stream(
        self,
        messages: Sequence[Message],
        model: str = "echo-local",
        tools: Optional[Sequence[Dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> Iterable[str]:
        """Default: yield the full completion as one chunk."""
        resp = self.complete(messages, model=model, tools=tools, **kwargs)
        if resp.content:
            yield resp.content


# ---------------------------------------------------------------------------
# Offline deterministic providers (test/mock doctrine — zero API keys)
# ---------------------------------------------------------------------------

class EchoProvider(LLMProvider):
    """
    Deterministic offline provider. Echoes the last user message and meters
    pseudo-tokens so the entire framework (loop, memory, budgets, evals,
    observability) runs with no network and no keys.
    """

    name = "echo"

    def complete(
        self,
        messages: Sequence[Message],
        model: str = "echo-local",
        tools: Optional[Sequence[Dict[str, Any]]] = None,
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> LLMResponse:
        last_user = next((m for m in reversed(messages) if m.role == Role.USER), None)
        text = (last_user.content if last_user and last_user.content else "") or "ack"
        prompt_tokens = sum(len((m.content or "").split()) + 8 for m in messages)
        completion_tokens = len(text.split()) + 8
        profile = MODEL_CATALOG.get(model, MODEL_CATALOG["echo-local"])
        return LLMResponse(
            content=f"[echo:{model}] {text}",
            finish_reason="stop",
            usage=Usage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                cost_usd=profile.cost(prompt_tokens, completion_tokens),
                model=model,
            ),
            model=model,
        )


class ScriptedProvider(LLMProvider):
    """
    Canned-response provider for deterministic agent-loop testing: pops one
    scripted LLMResponse per complete() call; falls back to EchoProvider when
    the script is exhausted. This is the mock-LLM harness pattern that lets us
    unit-test orchestration, escalation and budget gates with zero API calls.
    """

    name = "scripted"

    def __init__(self, script: Sequence[Dict[str, Any]]):
        self.script: List[Dict[str, Any]] = list(script)
        self._cursor = 0
        self.calls: List[Dict[str, Any]] = []

    def complete(
        self,
        messages: Sequence[Message],
        model: str = "echo-local",
        tools: Optional[Sequence[Dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> LLMResponse:
        self.calls.append({"model": model, "tools": list(tools or [])})
        if self._cursor < len(self.script):
            entry = dict(self.script[self._cursor])
            self._cursor += 1
            usage = Usage(model=model, **entry.get("usage", {}))
            return LLMResponse(
                content=entry.get("content"),
                tool_calls=entry.get("tool_calls", []),
                finish_reason=entry.get("finish_reason", "stop"),
                usage=usage,
                model=model,
            )
        return EchoProvider().complete(messages, model=model, tools=tools)


# ---------------------------------------------------------------------------
# Live providers (network import deferred; degrade to clear errors)
# ---------------------------------------------------------------------------

class OpenAICompatibleProvider(LLMProvider):
    """
    Works with OpenAI, DeepSeek, GLM, Groq, Together, Ollama (/v1), vLLM ...
    Any OpenAI-compatible /chat/completions endpoint.
    """

    name = "openai-compatible"

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.base_url = base_url or os.environ.get("OPENAI_BASE_URL") or None

    def complete(
        self,
        messages: Sequence[Message],
        model: str = "gpt-4o-mini",
        tools: Optional[Sequence[Dict[str, Any]]] = None,
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> LLMResponse:
        try:
            from openai import OpenAI  # deferred import
        except ImportError as exc:
            raise LLMError("openai package not installed: pip install openai", retryable=False, provider=self.name) from exc

        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        payload: Dict[str, Any] = {
            "model": model,
            "messages": [m.to_openai() for m in messages],
            "temperature": temperature,
        }
        if max_tokens:
            payload["max_tokens"] = max_tokens
        if tools:
            payload["tools"] = [
                {"type": "function", "function": t} for t in tools
            ]
        try:
            resp = client.chat.completions.create(**payload)
        except Exception as exc:  # rate limits/timeouts are retryable class
            retryable = "rate" in str(exc).lower() or "timeout" in str(exc).lower()
            raise LLMError(str(exc), retryable=retryable, provider=self.name) from exc

        choice = resp.choices[0]
        tool_calls = []
        if choice.message.tool_calls:
            for tc in choice.message.tool_calls:
                tool_calls.append(
                    {"id": tc.id, "name": tc.function.name, "arguments": tc.function.arguments or "{}"}
                )
        usage = resp.usage
        profile = MODEL_CATALOG.get(model)
        cost = profile.cost(usage.prompt_tokens, usage.completion_tokens) if profile and usage else 0.0
        return LLMResponse(
            content=choice.message.content,
            tool_calls=tool_calls,
            finish_reason=choice.finish_reason or "stop",
            usage=Usage(
                prompt_tokens=usage.prompt_tokens if usage else 0,
                completion_tokens=usage.completion_tokens if usage else 0,
                cost_usd=cost,
                model=model,
            ),
            model=model,
            raw=resp,
        )


class AnthropicProvider(LLMProvider):
    """Native Anthropic Messages API adapter (absorbs its request/response shape)."""

    name = "anthropic"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")

    def complete(
        self,
        messages: Sequence[Message],
        model: str = "claude-sonnet",
        tools: Optional[Sequence[Dict[str, Any]]] = None,
        temperature: float = 0.2,
        max_tokens: int = 4096,
        **kwargs: Any,
    ) -> LLMResponse:
        try:
            import anthropic  # deferred import
        except ImportError as exc:
            raise LLMError("anthropic package not installed: pip install anthropic", retryable=False, provider=self.name) from exc

        client = anthropic.Anthropic(api_key=self.api_key)
        system = "\n".join(m.content or "" for m in messages if m.role == Role.SYSTEM)
        convo = [m.to_openai() for m in messages if m.role in (Role.USER, Role.ASSISTANT, Role.TOOL)]
        payload: Dict[str, Any] = {
            "model": model,
            "messages": convo,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if system:
            payload["system"] = system
        if tools:
            payload["tools"] = [
                {"name": t["name"], "description": t.get("description", ""), "input_schema": t.get("parameters", {})}
                for t in tools
            ]
        try:
            resp = client.messages.create(**payload)
        except Exception as exc:
            retryable = "rate" in str(exc).lower() or "overloaded" in str(exc).lower()
            raise LLMError(str(exc), retryable=retryable, provider=self.name) from exc

        text_parts, tool_calls = [], []
        for block in resp.content:
            if getattr(block, "type", "") == "text":
                text_parts.append(block.text)
            elif getattr(block, "type", "") == "tool_use":
                tool_calls.append(
                    {"id": block.id, "name": block.name, "arguments": json.dumps(block.input or {})}
                )
        usage = Usage(
            prompt_tokens=resp.usage.input_tokens,
            completion_tokens=resp.usage.output_tokens,
            model=model,
        )
        profile = MODEL_CATALOG.get(model)
        if profile:
            usage.cost_usd = profile.cost(usage.prompt_tokens, usage.completion_tokens)
        return LLMResponse(
            content="\n".join(text_parts) or None,
            tool_calls=tool_calls,
            finish_reason="tool_calls" if tool_calls else "stop",
            usage=usage,
            model=model,
            raw=resp,
        )


# ---------------------------------------------------------------------------
# Model router: cheap -> capable cascade (Anthropic routing pattern)
# ---------------------------------------------------------------------------

_DIFFICULTY_HINTS = re.compile(
    r"\b(architect|design|analyz|refactor|security|production|complex|debug|strategy|research)\b",
    re.IGNORECASE,
)


class ModelRouter:
    """
    Difficulty-classifying router: easy queries go to the cheap tier, hard ones
    cascade to the flagship. Configurable per-instance; deterministic for tests.
    """

    def __init__(
        self,
        provider: LLMProvider,
        small_model: str = "gpt-4o-mini",
        flagship_model: str = "gpt-4o",
    ):
        self.provider = provider
        self.small_model = small_model
        self.flagship_model = flagship_model
        self.routing_log: List[Dict[str, Any]] = []

    def classify_difficulty(self, prompt: str) -> str:
        return "hard" if _DIFFICULTY_HINTS.search(prompt) else "easy"

    def complete(self, messages: Sequence[Message], **kwargs: Any) -> LLMResponse:
        last_user = next((m for m in reversed(messages) if m.role == Role.USER), None)
        prompt = (last_user.content if last_user and last_user.content else "") or ""
        difficulty = self.classify_difficulty(prompt)
        model = self.flagship_model if difficulty == "hard" else self.small_model
        self.routing_log.append({"difficulty": difficulty, "model": model, "ts": time.time()})
        return self.provider.complete(messages, model=model, **kwargs)


def create_provider(kind: Optional[str] = None, **kwargs: Any) -> LLMProvider:
    """Factory: 'echo' (default, offline), 'scripted', 'openai', 'anthropic'.
    Auto-detects from env when kind is None."""
    kind = (kind or os.environ.get("AGENT_LLM_PROVIDER") or "echo").lower()
    if kind == "echo":
        return EchoProvider()
    if kind == "scripted":
        return ScriptedProvider(kwargs.get("script", []))
    if kind in ("openai", "openai-compatible"):
        return OpenAICompatibleProvider(**kwargs)
    if kind == "anthropic":
        return AnthropicProvider(**kwargs)
    raise ValueError(f"Unknown provider kind: {kind}")
