"""Unit tests for AgentEngine, Memory, and ToolRegistry"""

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.engine import AgentEngine, AgentState
from core.memory import HierarchicalMemory
from core.tool_registry import ToolRegistry


class TestAgentEngine(unittest.TestCase):
    def test_agent_engine_lifecycle(self):
        agent = AgentEngine(name="TestAgent", system_prompt="Test Prompt")
        result = agent.run_lifecycle("Build and verify microservice")
        
        self.assertEqual(result["agent"], "TestAgent")
        self.assertTrue(result["verified"])
        self.assertEqual(result["state"], AgentState.COMPLETED.value)
        self.assertEqual(result["steps_executed"], 3)

    def test_hierarchical_memory(self):
        mem = HierarchicalMemory()
        mem.working.set("active_task", "deploy")
        self.assertEqual(mem.working.get("active_task"), "deploy")
        
        mem.semantic.store_fact("rule_1", "Never leak keys")
        self.assertEqual(mem.semantic.retrieve("rule_1"), "Never leak keys")
        
        mem.episodic.record("tool_call", {"tool": "ping", "status": 200})
        self.assertEqual(len(mem.episodic._episodes), 1)

    def test_tool_registry(self):
        registry = ToolRegistry()
        registry.register("add", "Adds two numbers", lambda a, b: int(a) + int(b))
        
        res = registry.execute("add", a=5, b=7)
        self.assertTrue(res.success)
        self.assertEqual(res.output, 12)


if __name__ == "__main__":
    unittest.main()
