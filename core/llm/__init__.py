"""
LLM Provider Abstraction Layer.
Model-agnostic chat completion interface with:
- OpenAI-compatible + Anthropic + deterministic Echo (offline/mock) providers
- Usage/cost metering on every call
- Streaming support
- ModelRouter with cheap-to-capable cascade (Anthropic routing pattern)
- 2024-2025 doctrine: "model profiles, not model names" (profile = tier + params + cost)
"""
from .providers import (
    Message,
    Role,
    Usage,
    LLMResponse,
    LLMProvider,
    LLMError,
    OpenAICompatibleProvider,
    AnthropicProvider,
    EchoProvider,
    ScriptedProvider,
    ModelProfile,
    MODEL_CATALOG,
    ModelRouter,
    create_provider,
)
from .retry import RetryPolicy, with_retries, CircuitBreaker, CircuitOpenError
from .structured import StructuredOutputError, generate_structured, validate_json

__all__ = [
    "Message", "Role", "Usage", "LLMResponse", "LLMProvider", "LLMError",
    "OpenAICompatibleProvider", "AnthropicProvider", "EchoProvider", "ScriptedProvider",
    "ModelProfile", "MODEL_CATALOG", "ModelRouter", "create_provider",
    "RetryPolicy", "with_retries", "CircuitBreaker", "CircuitOpenError",
    "StructuredOutputError", "generate_structured", "validate_json",
]
