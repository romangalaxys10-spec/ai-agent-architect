"""Contract + functional tests for the 90 SysAdmin series.

Every agent: sysadmin-grade offline engine + CLI + SKILL.md contract.
"""
import importlib.util
import os
import subprocess
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AGENTS_DIR = os.path.join(REPO_ROOT, "agents")

SYS90 = [
    ("solana-validator-ops-agent", "solana_validator_ops", "SolanaValidatorOpsEngine"),
    ("solana-rpc-surgeon-agent", "solana_rpc_surgeon", "SolanaRpcSurgeonEngine"),
    ("solana-program-deployer-agent", "solana_program_deployer", "SolanaProgramDeployerEngine"),
    ("solana-indexer-architect-agent", "solana_indexer_architect", "SolanaIndexerArchitectEngine"),
    ("solana-token-ops-agent", "solana_token_ops", "SolanaTokenOpsEngine"),
    ("solana-staking-governance-agent", "solana_staking_governance", "SolanaStakingGovernanceEngine"),
    ("solana-mev-shield-agent", "solana_mev_shield", "SolanaMevShieldEngine"),
    ("solana-ledger-forensics-agent", "solana_ledger_forensics", "SolanaLedgerForensicsEngine"),
    ("solana-payments-pilot-agent", "solana_payments_pilot", "SolanaPaymentsPilotEngine"),
    ("solana-nft-ops-agent", "solana_nft_ops", "SolanaNftOpsEngine"),
    ("evm-node-ops-agent", "evm_node_ops", "EvmNodeOpsEngine"),
    ("smart-contract-auditor-agent", "smart_contract_auditor", "SmartContractAuditorEngine"),
    ("chain-indexer-general-agent", "chain_indexer_general", "ChainIndexerGeneralEngine"),
    ("cross-chain-bridge-agent", "cross_chain_bridge", "CrossChainBridgeEngine"),
    ("wallet-ops-agent", "wallet_ops", "WalletOpsEngine"),
    ("gas-optimizer-agent", "gas_optimizer", "GasOptimizerEngine"),
    ("dao-governance-agent", "dao_governance", "DaoGovernanceEngine"),
    ("oracle-keeper-agent", "oracle_keeper", "OracleKeeperEngine"),
    ("block-explorer-agent", "block_explorer", "BlockExplorerEngine"),
    ("crypto-compliance-keeper-agent", "crypto_compliance_keeper", "CryptoComplianceKeeperEngine"),
    ("linux-boot-rescue-agent", "linux_boot_rescue", "LinuxBootRescueEngine"),
    ("linux-filesystem-surgeon-agent", "linux_filesystem_surgeon", "LinuxFilesystemSurgeonEngine"),
    ("linux-net-debug-agent", "linux_net_debug", "LinuxNetDebugEngine"),
    ("linux-perf-flame-agent", "linux_perf_flame", "LinuxPerfFlameEngine"),
    ("linux-selinux-guardian-agent", "linux_selinux_guardian", "LinuxSelinuxGuardianEngine"),
    ("linux-package-resolver-agent", "linux_package_resolver", "LinuxPackageResolverEngine"),
    ("linux-log-forensics-agent", "linux_log_forensics", "LinuxLogForensicsEngine"),
    ("linux-cron-orchestrator-agent", "linux_cron_orchestrator", "LinuxCronOrchestratorEngine"),
    ("linux-user-governance-agent", "linux_user_governance", "LinuxUserGovernanceEngine"),
    ("linux-dist-upgrade-agent", "linux_dist_upgrade", "LinuxDistUpgradeEngine"),
    ("bare-metal-provisioner-agent", "bare_metal_provisioner", "BareMetalProvisionerEngine"),
    ("server-monitoring-stack-agent", "server_monitoring_stack", "ServerMonitoringStackEngine"),
    ("server-backup-dr-agent", "server_backup_dr", "ServerBackupDrEngine"),
    ("server-capacity-planner-agent", "server_capacity_planner", "ServerCapacityPlannerEngine"),
    ("server-incident-commander-agent", "server_incident_commander", "ServerIncidentCommanderEngine"),
    ("server-config-drift-agent", "server_config_drift", "ServerConfigDriftEngine"),
    ("server-patching-orchestrator-agent", "server_patching_orchestrator", "ServerPatchingOrchestratorEngine"),
    ("server-loadbalancer-tuner-agent", "server_loadbalancer_tuner", "ServerLoadbalancerTunerEngine"),
    ("server-dns-ops-agent", "server_dns_ops", "ServerDnsOpsEngine"),
    ("server-virtualization-agent", "server_virtualization", "ServerVirtualizationEngine"),
    ("vuln-triage-agent", "vuln_triage", "VulnTriageEngine"),
    ("threat-hunter-agent", "threat_hunter", "ThreatHunterEngine"),
    ("siem-ops-agent", "siem_ops", "SiemOpsEngine"),
    ("cspm-governance-agent", "cspm_governance", "CspmGovernanceEngine"),
    ("zero-trust-architect-agent", "zero_trust_architect", "ZeroTrustArchitectEngine"),
    ("perf-bottleneck-agent", "perf_bottleneck", "PerfBottleneckEngine"),
    ("memory-leak-hunter-agent", "memory_leak_hunter", "MemoryLeakHunterEngine"),
    ("cpu-profiler-agent", "cpu_profiler", "CpuProfilerEngine"),
    ("io-tuner-agent", "io_tuner", "IoTunerEngine"),
    ("cdn-optimizer-global-agent", "cdn_optimizer_global", "CdnOptimizerGlobalEngine"),
    ("deep-debugger-agent", "deep_debugger", "DeepDebuggerEngine"),
    ("log-trace-correlator-agent", "log_trace_correlator", "LogTraceCorrelatorEngine"),
    ("flaky-test-hunter-agent", "flaky_test_hunter", "FlakyTestHunterEngine"),
    ("static-analysis-orchestrator-agent", "static_analysis_orchestrator", "StaticAnalysisOrchestratorEngine"),
    ("code-review-verdict-agent", "code_review_verdict", "CodeReviewVerdictEngine"),
    ("pr-risk-scorer-agent", "pr_risk_scorer", "PrRiskScorerEngine"),
    ("regression-bisector-agent", "regression_bisector", "RegressionBisectorEngine"),
    ("heap-dump-analyzer-agent", "heap_dump_analyzer", "HeapDumpAnalyzerEngine"),
    ("race-condition-hunter-agent", "race_condition_hunter", "RaceConditionHunterEngine"),
    ("api-contract-tester-agent", "api_contract_tester", "ApiContractTesterEngine"),
    ("llm-local-deployer-agent", "llm_local_deployer", "LlmLocalDeployerEngine"),
    ("model-quantizer-agent", "model_quantizer", "ModelQuantizerEngine"),
    ("vllm-optimizer-agent", "vllm_optimizer", "VllmOptimizerEngine"),
    ("ollama-fleet-agent", "ollama_fleet", "OllamaFleetEngine"),
    ("gpu-scheduler-agent", "gpu_scheduler", "GpuSchedulerEngine"),
    ("inference-benchmark-agent", "inference_benchmark", "InferenceBenchmarkEngine"),
    ("kv-cache-tuner-agent", "kv_cache_tuner", "KvCacheTunerEngine"),
    ("model-router-perf-agent", "model_router_perf", "ModelRouterPerfEngine"),
    ("gguf-converter-agent", "gguf_converter", "GgufConverterEngine"),
    ("llm-eval-perf-agent", "llm_eval_perf", "LlmEvalPerfEngine"),
    ("figma-to-code-agent", "figma_to_code", "FigmaToCodeEngine"),
    ("ux-wireframer-agent", "ux_wireframer", "UxWireframerEngine"),
    ("design-token-manager-agent", "design_token_manager", "DesignTokenManagerEngine"),
    ("accessibility-design-auditor-agent", "accessibility_design_auditor", "AccessibilityDesignAuditorEngine"),
    ("motion-design-agent", "motion_design", "MotionDesignEngine"),
    ("brand-system-agent", "brand_system", "BrandSystemEngine"),
    ("landing-page-designer-agent", "landing_page_designer", "LandingPageDesignerEngine"),
    ("design-handoff-agent", "design_handoff", "DesignHandoffEngine"),
    ("visual-qa-agent", "visual_qa", "VisualQaEngine"),
    ("design-performance-auditor-agent", "design_performance_auditor", "DesignPerformanceAuditorEngine"),
    ("frontend-scaffold-agent", "frontend_scaffold", "FrontendScaffoldEngine"),
    ("backend-api-builder-agent", "backend_api_builder", "BackendApiBuilderEngine"),
    ("fullstack-integrator-agent", "fullstack_integrator", "FullstackIntegratorEngine"),
    ("jamstack-deployer-agent", "jamstack_deployer", "JamstackDeployerEngine"),
    ("ssr-optimizer-agent", "ssr_optimizer", "SsrOptimizerEngine"),
    ("web-perf-auditor-agent", "web_perf_auditor", "WebPerfAuditorEngine"),
    ("web-security-hardener-agent", "web_security_hardener", "WebSecurityHardenerEngine"),
    ("cms-orchestrator-agent", "cms_orchestrator", "CmsOrchestratorEngine"),
    ("ecommerce-stack-agent", "ecommerce_stack", "EcommerceStackEngine"),
    ("realtime-collab-agent", "realtime_collab", "RealtimeCollabEngine"),
]

def _load(slug, module, cls_name):
    path=os.path.join(AGENTS_DIR, slug, "core", f"{module}_engine.py")
    spec=importlib.util.spec_from_file_location(f"{slug}_{module}", path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, cls_name)

class TestSys90Structure(unittest.TestCase):
    def test_exactly_ninety(self):
        self.assertEqual(len(SYS90), 90)
        self.assertEqual(len({s for s,_,_ in SYS90}), 90)
    def test_every_agent_has_skill_core_cli(self):
        for slug, module, _ in SYS90:
            base=os.path.join(AGENTS_DIR, slug)
            self.assertTrue(os.path.isfile(os.path.join(base, "SKILL.md")), f"{slug}: SKILL.md")
            self.assertTrue(os.path.isfile(os.path.join(base, "core", f"{module}_engine.py")), f"{slug}: engine")
            self.assertTrue(os.path.isfile(os.path.join(base, "cli", f"{module}.py")), f"{slug}: CLI")
    def test_skill_md_frontmatter_parses(self):
        import yaml
        for slug, _, _ in SYS90:
            content=open(os.path.join(AGENTS_DIR, slug, "SKILL.md"), encoding="utf-8").read()
            self.assertTrue(content.startswith("---"), f"{slug}: no frontmatter")
            meta=yaml.safe_load(content.split("---",2)[1])
            for key in ("name","description","version"):
                self.assertIn(key, meta, f"{slug}: missing {key}")
    def test_registry_discovers(self):
        sys.path.insert(0, REPO_ROOT)
        from core.registry import AgentRegistry
        agents=AgentRegistry.discover_agents()
        for slug,_,_ in SYS90:
            self.assertIn(slug, agents, f"{slug} not discovered")

class TestSys90CLIs(unittest.TestCase):
    def test_every_cli_help_from_neutral_cwd(self):
        failures=[]
        for slug, module, _ in SYS90:
            cli=os.path.join(AGENTS_DIR, slug, "cli", f"{module}.py")
            proc=subprocess.run([sys.executable, cli, "--help"], capture_output=True, text=True, timeout=60, cwd="/tmp")
            if proc.returncode!=0:
                failures.append((slug, proc.stderr.strip()[-200:]))
            elif "usage:" not in proc.stdout.lower():
                failures.append((slug, "no usage"))
        self.assertEqual(failures, [], f"CLI failures: {failures}")

class TestSys90Engines(unittest.TestCase):
    def test_all_engines_analyze_and_format(self):
        for slug, module, cls_name in SYS90:
            with self.subTest(agent=slug):
                Engine=_load(slug, module, cls_name)
                text=f"Sample for {slug}: solana linux server security debug llm web design web dev with enough words to avoid thin check.\n- bullet: value\nMore content for depth."
                result=Engine.analyze(text)
                self.assertIn(result.verdict, ["PASS","PASS_WITH_NOTES","NEEDS_REVIEW","BLOCKED","NEEDS_INPUT"])
                self.assertGreaterEqual(result.score, 0)
                self.assertLessEqual(result.score, 100)
                self.assertIn("sys_signals", result.metrics)
                report=Engine.format_report(result)
                self.assertIn(result.verdict, report)

if __name__=="__main__":
    unittest.main()
