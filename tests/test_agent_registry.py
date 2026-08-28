"""Unit tests for AgentRegistry and Sub-Agents Hub"""

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.registry import AgentRegistry


class TestAgentRegistry(unittest.TestCase):
    def test_discover_sub_agents(self):
        agents = AgentRegistry.discover_agents()
        self.assertIn("superdesign-agent", agents)
        self.assertIn("senior-architect-agent", agents)
        self.assertIn("steve-jobs-agent", agents)
        self.assertIn("skill-factory-agent", agents)

        superdesign = agents["superdesign-agent"]
        self.assertTrue(superdesign.has_cli)
        self.assertIn("superdesign", superdesign.name.lower())


if __name__ == "__main__":
    unittest.main()
