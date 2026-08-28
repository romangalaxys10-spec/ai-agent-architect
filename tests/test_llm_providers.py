"""Tests: LLM provider layer, model router, retry/circuit-breaker, structured output."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import json
import time

from core.llm.providers import (
    EchoProvider, ScriptedProvider, ModelRouter, OpenAICompatibleProvider,
    AnthropicProvider, Message, Role, Usage, MODEL_CATALOG, create_provider,
    tool_declaration,
)
from core.llm.retry import RetryPolicy, with_retries, CircuitBreaker, CircuitOpenError
from core.llm.structured import generate_structured, validate_json, extract_json, StructuredOutputError


class TestProviders(unittest.TestCase):
    def test_echo_provider_offline(self):
        p = EchoProvider()
        resp = p.complete([Message.user("hello world")], model="echo-local")
        self.assertIn("hello world", resp.content)
        self.assertGreater(resp.usage.total_tokens, 0)
        self.assertEqual(resp.usage.cost_usd, 0.0)  # local profile is free

    def test_scripted_provider_replays_script(self):
        script = [
            {"content": "first", "tool_calls": [], "usage": {"prompt_tokens": 5, "completion_tokens": 2}},
            {"content": "second", "tool_calls": [{"id": "1", "name": "t", "arguments": "{}"}]},
        ]
        p = ScriptedProvider(script)
        r1 = p.complete([Message.user("q")])
        r2 = p.complete([Message.user("q")])
        self.assertEqual(r1.content, "first")
        self.assertEqual(r2.content, "second")
        self.assertEqual(r2.tool_calls[0]["name"], "t")
        # exhausted script falls back to echo
        r3 = p.complete([Message.user("q")])
        self.assertIn("echo", r3.content)

    def test_model_router_cascades_by_difficulty(self):
        router = ModelRouter(EchoProvider(), small_model="gpt-4o-mini", flagship_model="gpt-4o")
        router.complete([Message.user("what is 2+2")])
        self.assertEqual(router.routing_log[-1]["difficulty"], "easy")
        router.complete([Message.user("architect a complex production system")])
        self.assertEqual(router.routing_log[-1]["difficulty"], "hard")

    def test_create_provider_factory(self):
        self.assertIsInstance(create_provider("echo"), EchoProvider)
        self.assertIsInstance(create_provider(None), EchoProvider)  # default offline
        with self.assertRaises(ValueError):
            create_provider("bogus")

    def test_tool_declaration_shape(self):
        d = tool_declaration("x", "does x", {"type": "object", "properties": {}})
        self.assertEqual(d["name"], "x")
        self.assertIn("parameters", d)


class TestRetry(unittest.TestCase):
    def test_retry_succeeds_after_transient_failure(self):
        calls = {"n": 0}

        def flaky():
            calls["n"] += 1
            if calls["n"] < 3:
                raise ConnectionError("timeout")
            return "ok"

        result = with_retries(flaky, RetryPolicy(max_attempts=5, base_delay=0.001), sleep=lambda s: None)
        self.assertEqual(result, "ok")
        self.assertEqual(calls["n"], 3)

    def test_retry_fails_fast_on_non_retryable(self):
        def bad():
            raise ValueError("auth error")

        with self.assertRaises(ValueError):
            with_retries(bad, RetryPolicy(max_attempts=5, retryable_check=lambda e: False), sleep=lambda s: None)

    def test_circuit_breaker_opens_and_recovers(self):
        cb = CircuitBreaker(failure_threshold=2, reset_timeout=0.05)
        for _ in range(2):
            try:
                cb.call("dep", lambda: (_ for _ in ()).throw(RuntimeError("boom")))
            except RuntimeError:
                pass
        self.assertEqual(cb.state("dep"), "open")
        with self.assertRaises(CircuitOpenError):
            cb.call("dep", lambda: "never")
        time.sleep(0.06)
        self.assertEqual(cb.state("dep"), "half-open")
        self.assertEqual(cb.call("dep", lambda: "back"), "back")
        self.assertEqual(cb.state("dep"), "closed")


class TestStructuredOutput(unittest.TestCase):
    SCHEMA = {
        "type": "object",
        "properties": {"name": {"type": "string"}, "score": {"type": "number"}},
        "required": ["name", "score"],
    }

    def test_extract_json_from_fenced_block(self):
        text = 'Sure! ```json\n{"name": "a", "score": 1}\n``` hope that helps'
        self.assertEqual(extract_json(text), {"name": "a", "score": 1})

    def test_extract_json_embedded(self):
        self.assertEqual(extract_json('prefix {"a": 1} suffix'), {"a": 1})

    def test_validate_json(self):
        self.assertEqual(validate_json({"name": "x", "score": 0.5}, self.SCHEMA)["name"], "x")
        with self.assertRaises(StructuredOutputError):
            validate_json({"name": "x"}, self.SCHEMA)  # missing required
        with self.assertRaises(StructuredOutputError):
            validate_json({"name": "x", "score": "high"}, self.SCHEMA)  # wrong type

    def test_generate_structured_with_repair(self):
        # Scripted provider: first broken, then fixed
        script = [
            {"content": '{"name": "agent"}'},  # missing score
            {"content": '{"name": "agent", "score": 9}'},
        ]
        provider = ScriptedProvider(script)
        out = generate_structured(provider, [Message.user("rate it")], self.SCHEMA)
        self.assertEqual(out["name"], "agent")
        self.assertEqual(out["score"], 9)


if __name__ == "__main__":
    unittest.main()
