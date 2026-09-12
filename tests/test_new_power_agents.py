"""Unit tests for the 4 newly deployed power agents:
1. code-review-refactor-sentinel
2. agent-studio-dashboard
3. defi-arbitrage-sentinel
4. motion-video-orchestrator
"""

import unittest
import sys
import os
import importlib.util

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.registry import AgentRegistry


def load_module(file_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
review_mod = load_module(os.path.join(base_dir, "agents/code-review-refactor-sentinel/core/review_engine.py"), "review_engine")
studio_mod = load_module(os.path.join(base_dir, "agents/agent-studio-dashboard/core/studio_server.py"), "studio_server")
defi_mod = load_module(os.path.join(base_dir, "agents/defi-arbitrage-sentinel/core/arbitrage_engine.py"), "arbitrage_engine")
video_mod = load_module(os.path.join(base_dir, "agents/motion-video-orchestrator/core/video_engine.py"), "video_engine")


class TestNewPowerAgents(unittest.TestCase):
    def test_code_review_engine_detects_secrets_and_bare_except(self):
        bad_code = """
api_key = "sk_live_1234567890abcdef123456"
try:
    eval("1 + 1")
except:
    pass
"""
        report = review_mod.CodeReviewEngine.analyze_code(bad_code)
        self.assertEqual(report.verdict, "FAIL")
        rule_ids = [i.rule_id for i in report.issues]
        self.assertIn("SEC-001", rule_ids)
        self.assertIn("SEC-002", rule_ids)
        self.assertIn("QUAL-001", rule_ids)
        self.assertIsNotNone(report.diff_patch)

    def test_studio_server_html_template(self):
        self.assertIn("Agent Architect Studio", studio_mod.HTML_TEMPLATE)
        self.assertIn("OpenTelemetry", studio_mod.HTML_TEMPLATE)

    def test_defi_arbitrage_engine(self):
        prices = {
            "Meteora DLMM": 145.0,
            "Raydium CLMM": 140.0,
            "Orca Whirlpool": 142.5
        }
        opps = defi_mod.DefiArbitrageEngine.scan_opportunities("SOL/USDC", prices, capital_usd=10000.0)
        self.assertGreater(len(opps), 0)
        best = opps[0]
        self.assertEqual(best.dex_buy, "Raydium CLMM")
        self.assertEqual(best.dex_sell, "Meteora DLMM")
        self.assertTrue(best.is_profitable)
        self.assertGreater(best.net_profit_usd, 0.0)

    def test_motion_video_engine(self):
        manifest = video_mod.MotionVideoEngine.compile_project(
            "DemoVideo",
            ["Scene One Hook", "Scene Two Architecture", "Scene Three Finale"]
        )
        self.assertEqual(len(manifest.scenes), 3)
        self.assertEqual(manifest.fps, 30)
        self.assertEqual(manifest.total_frames, 270)
        self.assertIn("import { Composition, Sequence", manifest.remotion_composition_jsx)

    def test_registry_discovers_all_four_agents(self):
        agents = AgentRegistry.discover_agents()
        self.assertIn("code-review-refactor-sentinel", agents)
        self.assertIn("agent-studio-dashboard", agents)
        self.assertIn("defi-arbitrage-sentinel", agents)
        self.assertIn("motion-video-orchestrator", agents)


if __name__ == "__main__":
    unittest.main()
