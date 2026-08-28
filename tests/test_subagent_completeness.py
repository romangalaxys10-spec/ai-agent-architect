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
    "anti-slop-content-engine", "binary-reverse-sentinel", "career-hunter-orchestrator", "cold-outreach-dealflow", "depth-conductor-agent", 
    "discord-community-radar", "invoice-billing-sentinel", "linkedin-intent-sniper", "model-bridge-router", "product-launch-orchestrator", 
    "senior-architect-agent", "skill-factory-agent", "solana-stream-sentinel", "steve-jobs-agent", "superdesign-agent", 
    "code-review-sentinel", "test-forge-agent", "bug-triage-agent", "ci-surgeon-agent", "refactor-pilot-agent", 
    "doc-scribe-agent", "sast-sentinel-agent", "dep-guardian-agent", "migration-planner-agent", "commit-crafter-agent", 
    "ticket-router-agent", "kb-curator-agent", "escalation-shield-agent", "voice-of-customer-agent", "sla-sentinel-agent", 
    "lead-qualifier-agent", "outreach-personalizer-agent", "meeting-brief-agent", "crm-hygiene-agent", "competitor-radar-agent", 
    "seo-content-strategist-agent", "ad-campaign-optimizer-agent", "deep-research-agent", "data-analyst-agent", "fact-check-agent", 
    "market-scout-agent", "literature-review-agent", "email-triage-agent", "calendar-architect-agent", "meeting-scribe-agent", 
    "trip-compass-agent", "deal-hunter-agent", "invoice-intake-agent", "expense-auditor-agent", "finstat-analyst-agent", 
    "portfolio-scout-agent", "resume-screener-agent", "interview-coach-agent", "onboarding-guide-agent", "culture-pulse-agent", 
    "content-calendar-agent", "script-writer-agent", "social-media-manager-agent", "copy-editor-agent", "cloud-cost-optimizer-agent", 
    "incident-commander-agent", "access-review-agent", "socratic-tutor-agent", "language-coach-agent", "contract-reviewer-agent", 
    "api-architect-agent", "perf-surgeon-agent", "log-detective-agent", "infra-as-code-agent", "db-migration-agent", 
    "qa-oracle-agent", "release-train-agent", "feature-flag-agent", "chaos-lab-agent", "oncall-buddy-agent", 
    "sdk-forge-agent", "git-historian-agent", "code-migration-agent", "env-doctor-agent", "secrets-vault-agent", 
    "build-optimizer-agent", "api-mock-agent", "licensing-guardian-agent", "prompt-ops-agent", "agent-eval-harness-agent", 
    "ml-pipeline-agent", "feature-store-agent", "model-risk-agent", "vector-db-architect-agent", "etl-surgeon-agent", 
    "dashboard-crafter-agent", "anomaly-hunter-agent", "forecast-oracle-agent", "nlp-pipeline-agent", "label-ops-agent", 
    "synthetic-data-agent", "data-governance-agent", "experiment-tracker-agent", "rag-architect-agent", "agent-memory-architect-agent", 
    "threat-model-agent", "pen-test-scribe-agent", "soc-triage-agent", "privacy-shield-agent", "compliance-mapper-agent", 
    "red-team-agent", "forensics-timeline-agent", "identity-governance-agent", "supply-chain-guard-agent", "crypto-audit-agent", 
    "bug-bounty-triage-agent", "incident-legal-bridge-agent", "pricing-strategist-agent", "sales-coach-agent", "proposal-forge-agent", 
    "revenue-ops-agent", "churn-prophet-agent", "partner-ecosystem-agent", "sales-enablement-agent", "gong-clone-agent", 
    "account-plan-agent", "forecast-radar-agent", "win-loss-analyst-agent", "event-roi-agent", "growth-loops-agent", 
    "influencer-scout-agent", "brand-voice-agent", "lifecycle-marketer-agent", "community-builder-agent", "web-analytics-agent", 
    "paid-social-surgeon-agent", "affiliate-ops-agent", "pr-pitch-agent", "launch-telemetry-agent", "referral-architect-agent", 
    "local-seo-agent", "video-growth-agent", "ux-research-agent", "roadmap-architect-agent", "spec-writer-agent", 
    "design-system-agent", "user-journey-agent", "ab-test-architect-agent", "accessibility-auditor-agent", "localization-pilot-agent", 
    "feedback-miner-agent", "jobs-to-be-done-agent", "procurement-scout-agent", "contract-lifecycle-agent", "tax-navigator-agent", 
    "treasury-ops-agent", "audit-trail-agent", "vendor-risk-agent", "kpi-ledger-agent", "okr-coach-agent", 
    "meeting-ops-agent", "policy-drafter-agent", "real-estate-scout-agent", "insurance-advisor-agent", "talent-sourcer-agent", 
    "performance-review-agent", "compensation-benchmark-agent", "learning-path-agent", "workforce-planner-agent", "exit-insight-agent", 
    "dei-auditor-agent", "manager-coach-agent", "csat-surgeon-agent", "knowledge-ops-agent", "support-qa-agent", 
    "renewal-orchestrator-agent", "community-support-agent", "nps-driver-agent", "self-serve-architect-agent", "podcast-producer-agent", 
    "newsletter-architect-agent", "ugc-curator-agent", "meme-ops-agent", "press-kit-agent", "course-builder-agent", 
    "event-producer-agent", "creator-monetization-agent", "healthcare-scribe-agent", "legal-ops-agent", "proptech-analyst-agent", 
    "edtech-coach-agent", "fintech-compliance-agent", "climate-risk-agent", "supply-chain-optimizer-agent", "retail-merchandiser-agent", 
    "hospitality-ops-agent", "manufacturing-qa-agent", "energy-ops-agent", "gov-procurement-agent", "nonprofit-impact-agent", 
    "autonomous-researcher-agent", "eval-judge-agent", "tool-smith-agent", "orchestration-designer-agent", "memory-ops-agent", 
    "adversarial-tester-agent", "cost-optimizer-agent", "skills-librarian-agent", "workflow-miner-agent", "digital-twin-agent", 
    "x-growth-hacker-agent", "linkedin-authority-agent", "youtube-growth-agent", "tiktok-virality-agent", "smm-command-center-agent", 
    "influencer-ops-agent", "social-listening-agent", "content-repurposer-agent", "community-growth-agent", "paid-growth-ops-agent", 
    "computer-vision-agent", "desktop-automation-agent", "screen-recorder-agent", "accessibility-pilot-agent", "keyboard-maestro-agent", 
    "mouse-precision-agent", "clipboard-ops-agent", "file-explorer-agent", "notification-center-agent", "system-prefs-agent", 
    "spotlight-search-agent", "window-tiling-agent", "menubar-tray-agent", "screenshot-assert-agent", "drag-drop-orchestrator-agent", 
    "touch-gesture-agent", "ocr-reader-agent", "audio-router-agent", "camera-mic-governor-agent", "power-battery-agent", 
    "display-color-agent", "input-device-agent", "browser-pilot-agent", "cdp-bridge-agent", "playwright-orchestrator-agent", 
    "puppeteer-forge-agent", "selenium-grid-agent", "browser-extension-agent", "dom-forensics-agent", "web-scraper-agent", 
    "form-autofill-agent", "cookie-consent-agent", "storage-inspector-agent", "network-har-agent", "performance-audit-agent", 
    "accessibility-web-agent", "visual-regression-agent", "auth-session-agent", "download-manager-agent", "pdf-renderer-agent", 
    "webrtc-media-agent", "service-worker-agent", "web-security-agent", "browser-profile-agent", "shell-pilot-agent", 
    "pty-bridge-agent", "tmux-orchestrator-agent", "terminal-renderer-agent", "cli-scaffold-agent", "prompt-engineer-agent", 
    "history-forensics-agent", "autocomplete-intel-agent", "env-shell-agent", "ssh-remote-agent", "terminal-recorder-agent", 
    "log-tail-agent", "job-control-agent", "keybinding-doctor-agent", "terminal-security-agent", "repl-bridge-agent", 
    "man-help-agent", "shell-benchmark-agent", "linux-admin-agent", "systemd-surgeon-agent", "package-manager-agent", 
    "kernel-tuner-agent", "network-ops-agent", "storage-raid-agent", "log-rotation-agent", "backup-restore-agent", 
    "sec-hardening-agent", "container-ops-agent", "k8s-pilot-agent", "nginx-ops-agent", "macos-admin-agent", 
    "brew-ops-agent", "xcode-ops-agent", "macos-security-agent", "windows-admin-agent", "powershell-forge-agent", 
    "winget-choco-agent", "windows-security-agent", "ad-identity-agent", "ci-cd-orchestrator-agent", "observability-stack-agent", 
    "infra-provisioner-agent", "ansible-pilot-agent", "tls-cert-agent", "db-ops-agent", "queue-ops-agent", 
    "cdn-edge-agent", "incident-ops-agent", "cost-ops-agent", "compliance-ops-agent", "secrets-ops-agent", 
    "gitops-pilot-agent", "edge-iot-agent", "perf-lab-agent", "disaster-recovery-agent", "migration-ops-agent", 
    "hrbp-strategic-partner-agent", "org-effectiveness-agent", "change-champion-agent", "business-alignment-agent", "stakeholder-influence-agent", 
    "workforce-shaping-agent", "hrbp-coaching-agent", "transformation-lead-agent", "people-analytics-storyteller-agent", "strategic-workforce-advisor-agent", 
    "hr-risk-compliance-agent", "future-of-work-architect-agent", "talent-intelligence-agent", "employer-value-agent", "candidate-experience-agent", 
    "hiring-manager-enablement-agent", "assessment-validation-agent", "internal-mobility-marketplace-agent", "performance-enablement-agent", "goal-alignment-agent", 
    "feedback-culture-agent", "nine-box-talent-agent", "succession-risk-agent", "career-mobility-agent", "talent-calibration-agent", 
    "learning-needs-diagnostician-agent", "skills-ontology-agent", "capability-planner-agent", "learning-strategy-architect-agent", "learning-ecosystem-agent", 
    "future-skills-scout-agent", "instructional-architect-agent", "blended-learning-agent", "cohort-learning-agent", "social-learning-agent", 
    "microlearning-crafter-agent", "scenario-simulation-agent", "video-learning-producer-agent", "facilitation-master-agent", "learning-analytics-agent", 
    "kirkpatrick-evaluator-agent", "learning-roi-agent", "lms-ops-agent", "learning-vendor-agent", "listening-strategy-agent", 
    "recognition-rituals-agent", "inclusion-belonging-agent", "wellbeing-strategist-agent", "resilience-burnout-agent", "team-effectiveness-agent",
]


class TestSubAgentCompleteness(unittest.TestCase):
    def test_all_sixtyfive_agents_present(self):
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
