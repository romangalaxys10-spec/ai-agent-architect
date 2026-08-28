"""Tests: MCP server/client + A2A v2 (agent cards, task lifecycle, discovery) + orchestrator v2."""
import sys, os, json, io
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from core.tool_registry import ToolRegistry
from core.mcp import MCPServer, MCPClient, jsonrpc_request, jsonrpc_response, jsonrpc_error, PROTOCOL_VERSION
from core.a2a_protocol import (
    AgentCard, AgentSkill, A2AParticipant, A2ADiscovery, TaskState, TaskStore,
    A2AMessage, A2AMessageBus, WELL_KNOWN_PATH,
)
from core.orchestrator import MultiAgentOrchestrator, OrchestrationTopology


def make_registry():
    r = ToolRegistry()
    r.register("add", "Add numbers", lambda a, b: a + b, parameters_schema={
        "type": "object",
        "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
        "required": ["a", "b"],
    })
    r.register("greet", "Greet someone", lambda name: f"hello {name}", parameters_schema={
        "type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"],
    })
    return r


class TestMCPServer(unittest.TestCase):
    def setUp(self):
        self.server = MCPServer(make_registry())

    def test_initialize_handshake(self):
        resp = self.server.handle(jsonrpc_request("initialize", {}, req_id=1))
        result = resp["result"]
        self.assertEqual(result["protocolVersion"], PROTOCOL_VERSION)
        self.assertIn("tools", result["capabilities"])
        self.assertIn("serverInfo", result)

    def test_tools_list_with_declarations(self):
        resp = self.server.handle(jsonrpc_request("tools/list", {}, req_id=2))
        tools = resp["result"]["tools"]
        names = [t["name"] for t in tools]
        self.assertIn("add", names)
        self.assertIn("annotations", tools[0])

    def test_tools_call_success(self):
        resp = self.server.handle(jsonrpc_request("tools/call", {"name": "add", "arguments": {"a": 2, "b": 3}}, req_id=3))
        result = resp["result"]
        self.assertFalse(result["isError"])
        self.assertEqual(result["content"][0]["type"], "text")
        self.assertIn("5", result["content"][0]["text"])

    def test_tools_call_error_is_flagged(self):
        resp = self.server.handle(jsonrpc_request("tools/call", {"name": "add", "arguments": {"a": "x"}}, req_id=4))
        self.assertTrue(resp["result"]["isError"])

    def test_unknown_method_error(self):
        resp = self.server.handle(jsonrpc_request("bogus/method", {}, req_id=5))
        self.assertIn("error", resp)

    def test_stdio_loop(self):
        server = MCPServer(make_registry())
        stdin = io.StringIO(json.dumps(jsonrpc_request("tools/list", {}, req_id=1)) + "\n")
        stdout = io.StringIO()
        server.serve_stdio(stdin, stdout)
        resp = json.loads(stdout.getvalue().strip())
        self.assertIn("tools", resp["result"])


class TestMCPClient(unittest.TestCase):
    def test_connect_list_call(self):
        client = MCPClient(MCPServer(make_registry()))
        info = client.connect()
        self.assertIn("name", info)
        tools = client.list_tools()
        self.assertGreaterEqual(len(tools), 2)
        result = client.call_tool("greet", {"name": "ada"})
        self.assertIn("hello ada", result["content"][0]["text"])

    def test_tool_result_shows_schema_violation_as_message(self):
        client = MCPClient(MCPServer(make_registry()))
        client.connect()
        result = client.call_tool("greet", {})
        self.assertTrue(result["isError"])
        self.assertIn("missing required", result["content"][0]["text"])


class TestAgentCard(unittest.TestCase):
    def test_card_serialization_roundtrip(self):
        card = AgentCard(
            name="billing-agent", description="Handles invoicing", url="https://billing.internal",
            skills=[AgentSkill(id="inv", name="invoicing", description="create invoices", tags=["finance"], examples=["invoice for $500"])],
            capabilities={"streaming": True, "pushNotifications": False},
        )
        data = card.to_dict()
        self.assertEqual(data["skills"][0]["tags"], ["finance"])
        parsed = AgentCard.from_dict(json.loads(card.to_json()))
        self.assertEqual(parsed.name, "billing-agent")
        self.assertEqual(parsed.skills[0].id, "inv")

    def test_well_known_path(self):
        self.assertEqual(WELL_KNOWN_PATH, "/.well-known/agent-card.json")


class TestA2ATaskLifecycle(unittest.TestCase):
    def test_full_lifecycle(self):
        store = TaskStore()
        task = store.create("analyze the repo")
        self.assertEqual(task.state, TaskState.SUBMITTED)
        task.transition(TaskState.WORKING, "accepted")
        task.transition(TaskState.COMPLETED, "done")
        self.assertEqual(task.state, TaskState.COMPLETED)
        with self.assertRaises(ValueError):
            task.transition(TaskState.WORKING, "cannot reopen")

    def test_input_required_loop(self):
        store = TaskStore()
        task = store.create("ambiguous work")
        task.transition(TaskState.WORKING)
        task.transition(TaskState.INPUT_REQUIRED, "need human input")
        task.transition(TaskState.WORKING, "input received")
        task.transition(TaskState.COMPLETED)
        states = [h["to"] for h in task.history]
        self.assertIn("input-required", states)

    def test_artifacts_and_parts(self):
        store = TaskStore()
        task = store.create("produce report")
        art = task.add_artifact("report", parts=[__import__("core.a2a_protocol", fromlist=["Part"]).Part(kind="text", text="the report")])
        d = task.to_dict()
        self.assertEqual(d["artifacts"][0]["name"], "report")
        self.assertEqual(d["artifacts"][0]["parts"][0]["kind"], "text")


class TestA2AParticipant(unittest.TestCase):
    def _participant(self):
        card = AgentCard(
            name="research-agent", description="Deep research and analysis",
            url="https://research.internal",
            skills=[AgentSkill(id="res", name="research", description="web research", tags=["research", "analysis"])],
        )
        return A2AParticipant(card, handler=lambda task: {"summary": "found 3 sources"})

    def test_well_known_served(self):
        p = self._participant()
        card = p.well_known()
        self.assertEqual(card["name"], "research-agent")

    def test_task_execution_produces_artifact(self):
        p = self._participant()
        task = p.submit_task("research solana")
        p.execute(task)
        self.assertEqual(task.state, TaskState.COMPLETED)
        self.assertTrue(task.artifacts)

    def test_input_required_flow(self):
        card = AgentCard(name="asker", description="asks", url="https://asker")
        p = A2AParticipant(card, handler=lambda task: {"input_required": True, "reason": "ambiguous"})
        task = p.submit_task("do the thing")
        p.execute(task)
        self.assertEqual(task.state, TaskState.INPUT_REQUIRED)

    def test_handler_failure_fails_task(self):
        card = AgentCard(name="broken", description="broken", url="https://broken")
        p = A2AParticipant(card, handler=lambda task: 1 / 0)
        task = p.submit_task("explode")
        p.execute(task)
        self.assertEqual(task.state, TaskState.FAILED)


class TestA2ADiscovery(unittest.TestCase):
    def test_discovery_by_skill(self):
        discovery = A2ADiscovery()
        card1 = AgentCard(name="r", description="research", url="https://r",
                          skills=[AgentSkill(id="s", name="research", description="web research", tags=["research"])])
        card2 = AgentCard(name="c", description="coding", url="https://c",
                          skills=[AgentSkill(id="s2", name="code", description="writes code", tags=["code"])])
        discovery.register(A2AParticipant(card1))
        discovery.register(A2AParticipant(card2))
        self.assertEqual(len(discovery.find_by_skill("research")), 1)
        self.assertEqual(discovery.find_by_url("https://c").card.description, "coding")
        self.assertEqual(len(discovery.catalog()), 2)


class TestLegacyBusStillWorks(unittest.TestCase):
    def test_publish_subscribe(self):
        bus = A2AMessageBus()
        received = []
        bus.subscribe("worker", lambda msg: received.append(msg) or A2AMessage(
            sender_id="worker", recipient_id=msg.sender_id, intent="RETURN_RESULT", payload={"ok": True}))
        replies = bus.publish(A2AMessage(sender_id="boss", recipient_id="worker", intent="DELEGATE_TASK", payload={"task": "x"}))
        self.assertEqual(len(replies), 1)
        self.assertEqual(len(bus.history), 2)


class TestOrchestratorV2(unittest.TestCase):
    def test_mesh_topology(self):
        orch = MultiAgentOrchestrator(topology=OrchestrationTopology.MESH)
        orch.register_agent("alpha", "worker", ["search"], handler=lambda p: {"found": True})
        orch.register_agent("beta", "worker", ["build"], handler=lambda p: {"built": True})
        result = orch.run("broadcast", {"task": "do"}, origin="alpha")
        self.assertEqual(result["topology"], "MESH")
        self.assertEqual(len(result["replies"]), 1)

    def test_blackboard_converges(self):
        orch = MultiAgentOrchestrator(topology=OrchestrationTopology.BLACKBOARD)
        orch.register_agent("w1", "watcher", [], handler=lambda bb: {"a": 1})
        orch.register_agent("w2", "watcher", [], handler=lambda bb: {"b": bb.get("a", 0) + 1})
        result = orch.run("converge", {})
        self.assertEqual(result["final_state"]["a"], 1)
        self.assertEqual(result["final_state"]["b"], 2)
        self.assertLessEqual(len(result["rounds"]), orch.blackboard_max_rounds)

    def test_blackboard_stops_on_stagnation(self):
        orch = MultiAgentOrchestrator(topology=OrchestrationTopology.BLACKBOARD)
        orch.blackboard_max_rounds = 10
        orch.register_agent("static", "watcher", [], handler=lambda bb: None)  # contributes nothing
        result = orch.run("stall", {"x": 1})
        self.assertLessEqual(len(result["rounds"]), 2)  # no change -> stop fast

    def test_hierarchical_failure_isolation(self):
        orch = MultiAgentOrchestrator(topology=OrchestrationTopology.HIERARCHICAL)
        orch.register_agent("boss", "supervisor", [])
        orch.register_agent("crashy", "worker", ["boom"], handler=lambda p: 1 / 0)
        orch.register_agent("solid", "worker", ["build"], handler=lambda p: {"ok": True})
        result = orch.run("build something", {})
        self.assertIn("solid", result["worker_results"])
        self.assertTrue(any(not d.success for d in orch.dispatch_records))
        self.assertGreaterEqual(orch.health_summary()["success_rate"], 0.0)


if __name__ == "__main__":
    unittest.main()
