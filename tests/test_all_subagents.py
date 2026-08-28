"""Unit tests for all specialized sub-agents in the agents/ hub"""

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

solana_mod = load_module("stream_engine", os.path.join(base, "agents/solana-stream-sentinel/core/stream_engine.py"))
career_mod = load_module("career_engine", os.path.join(base, "agents/career-hunter-orchestrator/core/career_engine.py"))
router_mod = load_module("router_engine", os.path.join(base, "agents/model-bridge-router/core/router_engine.py"))
binary_mod = load_module("binary_engine", os.path.join(base, "agents/binary-reverse-sentinel/core/binary_engine.py"))
billing_mod = load_module("billing_engine", os.path.join(base, "agents/invoice-billing-sentinel/core/billing_engine.py"))

SolanaStreamSentinel = solana_mod.SolanaStreamSentinel
CareerHunterEngine = career_mod.CareerHunterEngine
ModelBridgeRouter = router_mod.ModelBridgeRouter
BinaryReverseSentinel = binary_mod.BinaryReverseSentinel
InvoiceBillingEngine = billing_mod.InvoiceBillingEngine


class TestAllSubAgents(unittest.TestCase):
    def test_solana_stream_sentinel(self):
        event = SolanaStreamSentinel.decode_transaction_event(
            program_id="LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo",
            accounts=["TokenA", "TokenB", "PoolAddr"],
            data_hex="0x18be821703f274a1"
        )
        self.assertEqual(event.dex_type, "Meteora DLMM")
        sim = SolanaStreamSentinel.simulate_swap_preflight(event, amount_sol=1.0)
        self.assertEqual(sim["preflight_status"], "APPROVED")

    def test_career_hunter_orchestrator(self):
        lead = CareerHunterEngine.analyze_job_posting("Senior AI Engineer", "Python Solana Rust", "ScaleCorp")
        self.assertGreater(lead.match_score, 0.6)
        resume = CareerHunterEngine.generate_ats_resume(lead)
        self.assertIn("Core Competencies", resume)

    def test_model_bridge_router(self):
        dec = ModelBridgeRouter.route_request("Architect a zero-trust multi-agent mesh", requires_code=False)
        self.assertEqual(dec.selected_model, "claude-3.7-sonnet")
        schema = ModelBridgeRouter.normalize_tool_schema({"name": "fetch", "description": "Fetch data"}, target_provider="Z.AI")
        self.assertEqual(schema["type"], "function")

    def test_binary_reverse_sentinel(self):
        raw_text = "Connecting to AWS AKIAIOSFODNN7EXAMPLE and https://api.secret.io/v1/auth"
        report = BinaryReverseSentinel.audit_binary_bundle("TestBinary", raw_text)
        self.assertEqual(len(report.secrets_found), 1)
        self.assertIn("https://api.secret.io/v1/auth", report.endpoints_found)

    def test_invoice_billing_sentinel(self):
        inv = InvoiceBillingEngine.create_invoice(
            invoice_num="INV-001",
            client_name="Solana Foundation",
            client_email="finance@solana.com",
            items_data=[{"desc": "Security Audit", "hours": 10.0, "rate": 200.0}],
            currency="SOL"
        )
        self.assertEqual(inv.total, 2000.0)
        html = InvoiceBillingEngine.render_invoice_html(inv)
        self.assertIn("INV-001", html)

    def test_agent_registry_discovers_all(self):
        agents = AgentRegistry.discover_agents()
        self.assertGreaterEqual(len(agents), 6)
        self.assertIn("solana-stream-sentinel", agents)
        self.assertIn("career-hunter-orchestrator", agents)
        self.assertIn("model-bridge-router", agents)
        self.assertIn("binary-reverse-sentinel", agents)
        self.assertIn("invoice-billing-sentinel", agents)


if __name__ == "__main__":
    unittest.main()
