"""Unit tests for DepthCognitiveEngine and Depth Conductor Agent"""

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.depth_cognitive_engine import DepthCognitiveEngine
from core.registry import AgentRegistry


class TestDepthCognitiveEngine(unittest.TestCase):
    def test_high_complexity_depth_analysis(self):
        profile = DepthCognitiveEngine.analyze_cognitive_depth("Architect a zero-credit high-frequency Solana streaming engine")
        self.assertEqual(profile.task_complexity, "HIGH")
        self.assertEqual(profile.depth_score, 10)
        self.assertIn("conductor", profile.selected_depth_skills)
        self.assertIn("adversary", profile.selected_depth_skills)
        self.assertGreaterEqual(len(profile.excavated_assumptions), 2)
        self.assertGreaterEqual(len(profile.contrarian_paths), 2)
        self.assertIn("Day 1 (Immediate)", profile.temporal_horizons)

    def test_low_complexity_depth_analysis(self):
        profile = DepthCognitiveEngine.analyze_cognitive_depth("Format this string")
        self.assertEqual(profile.task_complexity, "LOW")
        self.assertIn("shallow", profile.selected_depth_skills)

    def test_format_depth_report(self):
        profile = DepthCognitiveEngine.analyze_cognitive_depth("Architect a distributed AI agent cluster")
        report = DepthCognitiveEngine.format_depth_report(profile)
        self.assertIn("Cognitive Depth Audit", report)
        self.assertIn("ds-excavate", report)
        self.assertIn("ds-adversary", report)

    def test_agent_registry_discovers_depth_conductor(self):
        agents = AgentRegistry.discover_agents()
        self.assertIn("depth-conductor-agent", agents)
        conductor = agents["depth-conductor-agent"]
        self.assertIn("depth", conductor.name.lower())


if __name__ == "__main__":
    unittest.main()
