"""Unit tests for RecencyRadarEngine and last30days-research-agent"""

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.recency_radar import RecencyRadarEngine
from core.registry import AgentRegistry


class TestLast30DaysResearch(unittest.TestCase):
    def test_recency_radar_curation(self):
        report = RecencyRadarEngine.curate_recent_intel("Solana Yellowstone gRPC and Agentic Frameworks")
        self.assertEqual(report.timeframe, "Trailing 30 Days")
        self.assertGreaterEqual(len(report.top_consensus_findings), 2)
        self.assertGreaterEqual(len(report.signals), 3)

    def test_agent_registry_discovers_last30days(self):
        agents = AgentRegistry.discover_agents()
        self.assertIn("last30days-research-agent", agents)
        agent = agents["last30days-research-agent"]
        self.assertIn("last30days", agent.name.lower())


if __name__ == "__main__":
    unittest.main()
