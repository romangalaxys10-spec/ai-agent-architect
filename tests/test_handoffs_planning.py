"""Tests: handoff protocol + planning (Planner, PlanExecutor, ReAct scaffold)."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from core.handoffs import Handoff, HandoffRegistry, HandoffRequest, InputFilter, HandoffScope
from core.llm.providers import Message, Role
from core.planning import Planner, PlanExecutor, PlanShape, ReActScaffold


class TestHandoffs(unittest.TestCase):
    def test_tool_declaration_names_transfer_tool(self):
        h = Handoff(destination="billing", description="Escalate billing issues",
                    input_type={"type": "object", "properties": {"reason": {"type": "string"}}})
        decl = h.to_tool_declaration()
        self.assertEqual(decl["name"], "transfer_to_billing")
        self.assertIn("reason", decl["parameters"]["properties"])

    def test_handoff_executes_with_callback_and_filter(self):
        fired = []
        reg = HandoffRegistry()
        reg.add("triage", Handoff(
            destination="specialist",
            on_handoff=lambda req: fired.append(req.to_agent),
            input_filter=InputFilter(drop_tool_messages=True, max_messages=2),
        ))
        history = [
            Message.user("q1"), Message(role=Role.TOOL, content="tool output", tool_call_id="t"),
            Message.user("q2"), Message.user("q3"), Message.user("q4"),
        ]
        req = HandoffRequest(from_agent="triage", to_agent="specialist", history=history)
        result = reg.execute(req)
        self.assertTrue(result.accepted)
        self.assertEqual(fired, ["specialist"])
        # filter dropped tool messages and elided old ones
        roles = [m.role for m in req.history]
        self.assertNotIn(Role.TOOL, roles)

    def test_unknown_handoff_rejected(self):
        reg = HandoffRegistry()
        req = HandoffRequest(from_agent="a", to_agent="nowhere")
        result = reg.execute(req)
        self.assertFalse(result.accepted)
        self.assertEqual(len(reg.trail), 1)

    def test_audit_trail_recorded(self):
        reg = HandoffRegistry()
        reg.add("a", Handoff(destination="b"))
        reg.execute(HandoffRequest(from_agent="a", to_agent="b", input_data={"reason": "x"}))
        entry = reg.trail[0]
        self.assertEqual(entry["from"], "a")
        self.assertEqual(entry["to"], "b")
        self.assertEqual(entry["input_keys"], ["reason"])


class TestPlanning(unittest.TestCase):
    def test_heuristic_plan_shapes(self):
        planner = Planner()
        plan = planner.plan("research and build a production agent", PlanShape.PLAN_EXECUTE_REPLAN)
        self.assertGreaterEqual(len(plan.steps), 3)
        self.assertEqual(plan.shape, PlanShape.PLAN_EXECUTE_REPLAN)

    def test_dependency_graph_links_steps(self):
        plan = Planner().plan("build deploy test verify", PlanShape.DEPENDENCY_GRAPH)
        self.assertTrue(any(s.depends_on for s in plan.steps))

    def test_executor_completes_plan(self):
        plan = Planner().plan("research build verify")
        executed = []

        def executor(step):
            executed.append(step.step_id)
            return f"ok:{step.description}"

        result = PlanExecutor(executor).run(plan)
        self.assertTrue(all(s.status == "DONE" for s in result.steps))
        self.assertEqual(len(executed), len(plan.steps))

    def test_executor_retries_then_escalates(self):
        plan = Planner().plan("build the thing")
        calls = {"n": 0}
        escalations = []

        def flaky(step):
            calls["n"] += 1
            raise RuntimeError("transient failure")

        ex = PlanExecutor(flaky, max_step_attempts=2, on_escalate=lambda step, kind: escalations.append(step.step_id))
        result = ex.run(plan)
        # every step retried up to max attempts before escalation
        for s in result.steps:
            self.assertEqual(s.attempts, 2)
        self.assertEqual(calls["n"], 2 * len(result.steps))
        self.assertTrue(escalations)  # escalated to human

    def test_replan_on_blocked(self):
        plan = Planner().plan("research build verify")
        replans = []

        def replanner(old_plan, blocked):
            replans.append(blocked.step_id)
            new_plan = Planner().plan("research build verify take two")
            return new_plan

        def executor(step):
            if "take two" not in plan_marker[0]:
                raise RuntimeError("always fails first version")
            return "ok"

        plan_marker = [""]
        original_plan = plan

        def tracked_executor(step):
            return executor(step)

        # simpler: fail everything on v1, succeed on v2
        def executor_v2(step):
            return "ok"

        def failing(step):
            raise RuntimeError("block")

        state = {"version": 1}

        def smart(step):
            if state["version"] == 1:
                raise RuntimeError("blocked")
            return "ok"

        def replanner2(old, blocked):
            state["version"] = 2
            return Planner().plan("research build verify v2")

        ex = PlanExecutor(smart, max_step_attempts=1, max_replans=1, replanner=replanner2)
        result = ex.run(plan)
        self.assertEqual(state["version"], 2)

    def test_react_parse(self):
        text = 'Thought: I should search\nAction: search\nAction Input: {"q": "test"}\nObservation: results\nFinal Answer: done'
        actions = ReActScaffold.parse(text)
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]["tool"], "search")
        self.assertEqual(actions[0]["arguments"]["q"], "test")

    def test_react_render_lists_tools(self):
        scaffold_text = ReActScaffold.render("goal", ["search", "calc"])
        self.assertIn("search", scaffold_text)
        self.assertIn("Final Answer", scaffold_text)


if __name__ == "__main__":
    unittest.main()
