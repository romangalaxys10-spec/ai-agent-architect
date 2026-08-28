"""End-to-end completeness contract: every sub-agent must be structurally complete
(SKILL.md + core engine + CLI) and its CLI must actually execute (the bug class
this test exists to prevent: 12/12 agent CLIs were broken at commit 6e11c41)."""
import os
import subprocess
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AGENTS_DIR = os.path.join(REPO_ROOT, "agents")

EXPECTED_AGENTS = [
    "anti-slop-content-engine", "binary-reverse-sentinel", "career-hunter-orchestrator",
    "cold-outreach-dealflow", "depth-conductor-agent", "discord-community-radar",
    "invoice-billing-sentinel", "linkedin-intent-sniper", "model-bridge-router",
    "product-launch-orchestrator", "senior-architect-agent", "skill-factory-agent",
    "solana-stream-sentinel", "steve-jobs-agent", "superdesign-agent",
]


class TestSubAgentCompleteness(unittest.TestCase):
    def test_all_fifteen_agents_present(self):
        present = sorted(d for d in os.listdir(AGENTS_DIR) if os.path.isdir(os.path.join(AGENTS_DIR, d)))
        for agent in EXPECTED_AGENTS:
            self.assertIn(agent, present, f"missing sub-agent directory: {agent}")

    def test_every_agent_has_skill_core_cli(self):
        for agent in EXPECTED_AGENTS:
            base = os.path.join(AGENTS_DIR, agent)
            self.assertTrue(os.path.isfile(os.path.join(base, "SKILL.md")),
                            f"{agent}: missing SKILL.md")
            self.assertTrue(os.path.isdir(os.path.join(base, "core")),
                            f"{agent}: missing core/ engine")
            self.assertTrue(os.path.isdir(os.path.join(base, "cli")),
                            f"{agent}: missing cli/ entrypoint")
            cli_files = [f for f in os.listdir(os.path.join(base, "cli")) if f.endswith(".py") and f != "__init__.py"]
            self.assertTrue(cli_files, f"{agent}: cli/ has no entrypoint script")

    def test_skill_md_frontmatter_parses(self):
        import yaml
        for agent in EXPECTED_AGENTS:
            path = os.path.join(AGENTS_DIR, agent, "SKILL.md")
            content = open(path, encoding="utf-8").read()
            self.assertTrue(content.startswith("---"), f"{agent}: SKILL.md missing frontmatter")
            parts = content.split("---", 2)
            meta = yaml.safe_load(parts[1])
            for key in ("name", "description", "version"):
                self.assertIn(key, meta, f"{agent}: frontmatter missing '{key}'")

    def test_every_cli_runs_from_any_cwd(self):
        failures = []
        for agent in EXPECTED_AGENTS:
            cli_dir = os.path.join(AGENTS_DIR, agent, "cli")
            cli_files = [f for f in os.listdir(cli_dir) if f.endswith(".py") and f != "__init__.py"]
            for cli in cli_files:
                # run from a NEUTRAL cwd to prove no reliance on repo-root cwd
                proc = subprocess.run(
                    [sys.executable, os.path.join(cli_dir, cli), "--help"],
                    capture_output=True, text=True, timeout=60, cwd="/tmp",
                )
                if proc.returncode != 0 or "usage:" not in proc.stdout:
                    failures.append(f"{agent}/cli/{cli}: rc={proc.returncode} err={proc.stderr[:200]}")
        self.assertEqual(failures, [], "broken agent CLIs:\n" + "\n".join(failures))


class TestCoreModulesImportable(unittest.TestCase):
    def test_full_surface_imports(self):
        from core.llm import EchoProvider, ModelRouter, CircuitBreaker, generate_structured  # noqa
        from core.agent_loop import AgentLoop  # noqa
        from core.workflows import PromptChain, RouterWorkflow, Parallelization, OrchestratorWorkers, EvaluatorOptimizer  # noqa
        from core.handoffs import HandoffRegistry  # noqa
        from core.planning import Planner, PlanExecutor, ReActScaffold  # noqa
        from core.memory import HierarchicalMemory  # noqa
        from core.rag import AgenticRAG  # noqa
        from core.guardrails import SafetyGuardrails  # noqa
        from core.hitl import HumanApprovalFlow  # noqa
        from core.evaluation import LLMAsJudge, TrajectoryEvaluator  # noqa
        from core.observability import TelemetryTracer, JSONLLogger, CostLedger  # noqa
        from core.mcp import MCPServer, MCPClient  # noqa
        from core.a2a_protocol import AgentCard, A2AParticipant, A2ADiscovery  # noqa
        from core.orchestrator import MultiAgentOrchestrator  # noqa
        from core.reliability import BudgetPortfolio, LoopDetector  # noqa
        from core.context_engineering import ContextEngine  # noqa
        from core.tool_registry import ToolRegistry  # noqa


if __name__ == "__main__":
    unittest.main()
