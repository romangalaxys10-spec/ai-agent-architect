"""Unit tests for the 5 Marketing, Discord & LinkedIn growth sub-agents"""

import unittest
import sys
import os
import importlib.util

base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base)

from core.registry import AgentRegistry

def load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

linkedin_mod = load_module("intent_engine", os.path.join(base, "agents/linkedin-intent-sniper/core/intent_engine.py"))
discord_mod = load_module("radar_engine", os.path.join(base, "agents/discord-community-radar/core/radar_engine.py"))
content_mod = load_module("content_engine", os.path.join(base, "agents/anti-slop-content-engine/core/content_engine.py"))
launch_mod = load_module("launch_engine", os.path.join(base, "agents/product-launch-orchestrator/core/launch_engine.py"))
outreach_mod = load_module("outreach_engine", os.path.join(base, "agents/cold-outreach-dealflow/core/outreach_engine.py"))

LinkedInIntentSniper = linkedin_mod.LinkedInIntentSniper
DiscordCommunityRadar = discord_mod.DiscordCommunityRadar
AntiSlopContentEngine = content_mod.AntiSlopContentEngine
ProductLaunchOrchestrator = launch_mod.ProductLaunchOrchestrator
ColdOutreachDealflow = outreach_mod.ColdOutreachDealflow


class TestMarketingAgents(unittest.TestCase):
    def test_linkedin_intent_sniper(self):
        prospect = LinkedInIntentSniper.analyze_prospect("Elena Rostova", "CTO at SolanaScale", "SolanaScale", "Looking for senior agent engineers")
        self.assertEqual(prospect.intent_signal, "HIRING_SCALING")
        self.assertIn("Elena", prospect.icebreaker_message)

    def test_discord_community_radar(self):
        sig = DiscordCommunityRadar.process_message("founder_bob", "#gigs", "Looking to hire someone for $3k bounty to build a gRPC indexer")
        self.assertEqual(sig.signal_category, "PAID_BOUNTY")
        self.assertEqual(sig.alert_priority, "HIGH")

    def test_anti_slop_content_engine(self):
        pkg = AntiSlopContentEngine.synthesize_content("Zero-Credit Design Engine", "Deterministic HTML/Tailwind generator")
        self.assertTrue(pkg.slop_linter_passed)
        self.assertEqual(len(pkg.carousel_slides), 5)
        self.assertGreater(len(pkg.x_thread_tweets), 2)

    def test_product_launch_orchestrator(self):
        camp = ProductLaunchOrchestrator.generate_launch_package("SuperDesign Agent", "https://github.com/romangalaxys10-spec/superdesign-agent")
        self.assertIn("Show HN", camp.show_hn_post)
        self.assertEqual(len(camp.three_day_timeline), 3)

    def test_cold_outreach_dealflow(self):
        touches = ColdOutreachDealflow.generate_sequence("Marcus Vance", "ScaleLabs", "Python & Rust")
        self.assertEqual(len(touches), 3)
        self.assertGreaterEqual(touches[0].deliverability_score, 0.90)
        sow = ColdOutreachDealflow.generate_sow("ScaleLabs", "Autonomous Streaming Pipeline", 9500.0)
        self.assertEqual(sow.total_fee_usd, 9500.0)

    def test_agent_registry_discovers_all_14_agents(self):
        agents = AgentRegistry.discover_agents()
        self.assertGreaterEqual(len(agents), 11)
        self.assertIn("linkedin-intent-sniper", agents)
        self.assertIn("discord-community-radar", agents)
        self.assertIn("anti-slop-content-engine", agents)
        self.assertIn("product-launch-orchestrator", agents)
        self.assertIn("cold-outreach-dealflow", agents)


if __name__ == "__main__":
    unittest.main()
