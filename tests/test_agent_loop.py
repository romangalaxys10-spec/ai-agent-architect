"""Tests: the real agent loop (tool calling, budgets, HITL, loop detection, stop conditions)."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import json

from core.agent_loop import AgentLoop, StopReason
from core.context_engineering import ContextEngine
from core.hitl import ApprovalPolicy, ApprovalRule, HumanApprovalFlow, Decision
from core.llm.providers import ScriptedProvider, EchoProvider, Message
from core.reliability import BudgetPortfolio, LoopDetector, TerminationCriteria
from core.tool_registry import ToolRegistry


def make_loop(script, tools=None, **kwargs):
    provider = ScriptedProvider(script)
    registry = tools or ToolRegistry()
    return AgentLoop(name="t", provider=provider, registry=registry, **kwargs), provider


class TestAgentLoop(unittest.TestCase):
    def test_direct_answer_stops_immediately(self):
        loop, _ = make_loop([{"content": "The answer is 42."}])
        result = loop.run("meaning of life")
        self.assertEqual(result.stop_reason, StopReason.MODEL_STOP)
        self.assertEqual(result.steps, 1)
        self.assertIn("42", result.final_answer)

    def test_tool_call_then_answer(self):
        registry = ToolRegistry()
        registry.register("add", "Add numbers", lambda a, b: a + b, parameters_schema={
            "type": "object", "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
            "required": ["a", "b"],
        })
        script = [
            {"content": None, "tool_calls": [{"id": "c1", "name": "add", "arguments": '{"a": 2, "b": 3}'}],
             "finish_reason": "tool_calls"},
            {"content": "2 + 3 = 5"},
        ]
        loop, _ = make_loop(script, tools=registry)
        result = loop.run("compute 2+3")
        self.assertTrue(result.success)
        self.assertEqual(result.turns[0].tool_results[0]["tool"], "add")
        self.assertIn("5", result.final_answer)

    def test_tool_error_flows_back_as_message(self):
        registry = ToolRegistry()
        registry.register("boom", "Always fails", lambda: 1 / 0)
        script = [
            {"content": None, "tool_calls": [{"id": "c1", "name": "boom", "arguments": "{}"}]},
            {"content": "The tool failed; I report the error gracefully."},
        ]
        loop, _ = make_loop(script, tools=registry)
        result = loop.run("use boom")
        self.assertTrue(result.success)
        tool_msg = [m for m in result.transcript if m.role.value == "tool"][0]
        self.assertIn("TOOL_ERROR", tool_msg.content)

    def test_parallel_tool_calls_fan_out(self):
        registry = ToolRegistry()
        calls = {"n": 0}

        def slow(x: int) -> int:
            import time
            calls["n"] += 1
            time.sleep(0.05)
            return x * 2

        registry.register("slow", "slow double", slow, parameters_schema={
            "type": "object", "properties": {"x": {"type": "integer"}}, "required": ["x"]})
        script = [
            {"content": None, "tool_calls": [
                {"id": f"c{i}", "name": "slow", "arguments": json.dumps({"x": i})} for i in range(3)
            ]},
            {"content": "all done"},
        ]
        loop, _ = make_loop(script, tools=registry)
        result = loop.run("parallel")
        self.assertEqual(calls["n"], 3)
        self.assertEqual(len(result.turns[0].tool_results), 3)

    def test_budget_exhaustion_stops_run(self):
        script = [{"content": None, "tool_calls": [{"id": "c", "name": "noop", "arguments": "{}"}]}
                  for _ in range(50)]
        registry = ToolRegistry()
        registry.register("noop", "noop", lambda: None)
        budgets = BudgetPortfolio(max_steps=3, max_tokens=10_000_000, max_seconds=60)
        loop, _ = make_loop(script, tools=registry, budgets=budgets)
        result = loop.run("loop forever")
        self.assertEqual(result.stop_reason, StopReason.BUDGET_EXHAUSTED)
        self.assertLessEqual(result.steps, 3)

    def test_success_predicate_termination(self):
        flag = {"done": False}
        script = [
            {"content": None, "tool_calls": [{"id": "c1", "name": "work", "arguments": "{}"}]},
            {"content": "working more"},
            {"content": "still going"},
        ]
        registry = ToolRegistry()
        registry.register("work", "work", lambda: flag.update(done=True))
        termination = TerminationCriteria(success_predicate=lambda: flag["done"])
        loop, _ = make_loop(script, tools=registry, termination=termination)
        result = loop.run("do work")
        self.assertEqual(result.stop_reason, StopReason.SUCCESS_PREDICATE)

    def test_hitl_approval_reject_blocks_tool(self):
        registry = ToolRegistry()
        executed = []

        def dangerous(target: str) -> str:
            executed.append(target)
            return "deleted"

        registry.register("delete", "dangerous delete", dangerous,
                          requires_approval=True, is_safe=False,
                          parameters_schema={"type": "object", "properties": {"target": {"type": "string"}},
                                             "required": ["target"]})
        flow = HumanApprovalFlow(policy=ApprovalPolicy(default_mode="ask"))
        flow.set_resolver(lambda intr: Decision.REJECT)

        script = [
            {"content": None, "tool_calls": [{"id": "c1", "name": "delete", "arguments": '{"target": "prod"}'}]},
            {"content": "understood, deletion was rejected by policy."},
        ]
        loop, _ = make_loop(script, tools=registry, approval_flow=flow)
        result = loop.run("delete prod")
        self.assertEqual(executed, [])  # never executed
        self.assertTrue(result.success)  # loop itself completed gracefully
        self.assertEqual(len(flow.audit_trail), 1)
        self.assertEqual(flow.audit_trail[0]["decision"], "reject")

    def test_hitl_edit_modifies_arguments(self):
        registry = ToolRegistry()
        seen = []

        def deploy(env: str) -> str:
            seen.append(env)
            return "deployed"

        registry.register("deploy", "deploy", deploy, requires_approval=True,
                          parameters_schema={"type": "object", "properties": {"env": {"type": "string"}},
                                             "required": ["env"]})
        flow = HumanApprovalFlow(policy=ApprovalPolicy(default_mode="ask"))

        def editor(intr):
            from core.hitl import Interrupt
            return Decision.EDIT

        # Simulate EDIT via direct resolution flow
        script = [
            {"content": None, "tool_calls": [{"id": "c1", "name": "deploy", "arguments": '{"env": "prod"}'}]},
            {"content": "deployed"},
        ]
        loop, _ = make_loop(script, tools=registry, approval_flow=flow)
        # patch auto_resolve to approve-with-edit
        original = flow.auto_resolve

        def edit_resolver(intr):
            intr.resolve(Decision.EDIT, edited_arguments={"env": "staging"})
            flow.audit_trail.append({"decision": "edit"})
            return intr

        flow.auto_resolve = edit_resolver
        result = loop.run("deploy to prod")
        self.assertEqual(seen, ["staging"])  # argument was edited before execution

    def test_loop_detection_terminates(self):
        registry = ToolRegistry()
        registry.register("same", "same call", lambda q: "result")
        same_call = {"id": "c", "name": "same", "arguments": '{"q": "x"}'}
        script = [{"content": None, "tool_calls": [same_call]} for _ in range(10)]
        loop, _ = make_loop(script, tools=registry, loop_detector=LoopDetector(repeat_threshold=3))
        result = loop.run("loop")
        self.assertEqual(result.stop_reason, StopReason.LOOP_DETECTED)

    def test_transcript_records_everything(self):
        script = [
            {"content": None, "tool_calls": [{"id": "c1", "name": "t", "arguments": "{}"}],
             "usage": {"prompt_tokens": 100, "completion_tokens": 20}},
            {"content": "final", "usage": {"prompt_tokens": 120, "completion_tokens": 10}},
        ]
        registry = ToolRegistry()
        registry.register("t", "t", lambda: "ok")
        loop, _ = make_loop(script, tools=registry)
        result = loop.run("x")
        roles = [m.role.value for m in result.transcript]
        self.assertIn("user", roles)
        self.assertIn("assistant", roles)
        self.assertIn("tool", roles)
        self.assertGreater(result.total_tokens, 0)


if __name__ == "__main__":
    unittest.main()
