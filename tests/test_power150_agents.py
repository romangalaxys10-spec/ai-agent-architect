"""Contract + functional tests for the 150 Power Expansion suite.

Every agent: offline deterministic engine + argparse CLI + SKILL.md contract.
Mirrors tests/test_top50_agents.py pattern but for the 150 global-demand agents.
"""
import importlib.util
import os
import subprocess
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AGENTS_DIR = os.path.join(REPO_ROOT, "agents")

POWER150 = [
    ("api-architect-agent", "api_architect", "ApiArchitectEngine"),
    ("perf-surgeon-agent", "perf_surgeon", "PerfSurgeonEngine"),
    ("log-detective-agent", "log_detective", "LogDetectiveEngine"),
    ("infra-as-code-agent", "infra_as_code", "InfraAsCodeEngine"),
    ("db-migration-agent", "db_migration", "DbMigrationEngine"),
    ("qa-oracle-agent", "qa_oracle", "QaOracleEngine"),
    ("release-train-agent", "release_train", "ReleaseTrainEngine"),
    ("feature-flag-agent", "feature_flag", "FeatureFlagEngine"),
    ("chaos-lab-agent", "chaos_lab", "ChaosLabEngine"),
    ("oncall-buddy-agent", "oncall_buddy", "OncallBuddyEngine"),
    ("sdk-forge-agent", "sdk_forge", "SdkForgeEngine"),
    ("git-historian-agent", "git_historian", "GitHistorianEngine"),
    ("code-migration-agent", "code_migration", "CodeMigrationEngine"),
    ("env-doctor-agent", "env_doctor", "EnvDoctorEngine"),
    ("secrets-vault-agent", "secrets_vault", "SecretsVaultEngine"),
    ("build-optimizer-agent", "build_optimizer", "BuildOptimizerEngine"),
    ("api-mock-agent", "api_mock", "ApiMockEngine"),
    ("licensing-guardian-agent", "licensing_guardian", "LicensingGuardianEngine"),
    ("prompt-ops-agent", "prompt_ops", "PromptOpsEngine"),
    ("agent-eval-harness-agent", "agent_eval_harness", "AgentEvalHarnessEngine"),
    ("ml-pipeline-agent", "ml_pipeline", "MlPipelineEngine"),
    ("feature-store-agent", "feature_store", "FeatureStoreEngine"),
    ("model-risk-agent", "model_risk", "ModelRiskEngine"),
    ("vector-db-architect-agent", "vector_db_architect", "VectorDbArchitectEngine"),
    ("etl-surgeon-agent", "etl_surgeon", "EtlSurgeonEngine"),
    ("dashboard-crafter-agent", "dashboard_crafter", "DashboardCrafterEngine"),
    ("anomaly-hunter-agent", "anomaly_hunter", "AnomalyHunterEngine"),
    ("forecast-oracle-agent", "forecast_oracle", "ForecastOracleEngine"),
    ("nlp-pipeline-agent", "nlp_pipeline", "NlpPipelineEngine"),
    ("label-ops-agent", "label_ops", "LabelOpsEngine"),
    ("synthetic-data-agent", "synthetic_data", "SyntheticDataEngine"),
    ("data-governance-agent", "data_governance", "DataGovernanceEngine"),
    ("experiment-tracker-agent", "experiment_tracker", "ExperimentTrackerEngine"),
    ("rag-architect-agent", "rag_architect", "RagArchitectEngine"),
    ("agent-memory-architect-agent", "agent_memory_architect", "AgentMemoryArchitectEngine"),
    ("threat-model-agent", "threat_model", "ThreatModelEngine"),
    ("pen-test-scribe-agent", "pen_test_scribe", "PenTestScribeEngine"),
    ("soc-triage-agent", "soc_triage", "SocTriageEngine"),
    ("privacy-shield-agent", "privacy_shield", "PrivacyShieldEngine"),
    ("compliance-mapper-agent", "compliance_mapper", "ComplianceMapperEngine"),
    ("red-team-agent", "red_team", "RedTeamEngine"),
    ("forensics-timeline-agent", "forensics_timeline", "ForensicsTimelineEngine"),
    ("identity-governance-agent", "identity_governance", "IdentityGovernanceEngine"),
    ("supply-chain-guard-agent", "supply_chain_guard", "SupplyChainGuardEngine"),
    ("crypto-audit-agent", "crypto_audit", "CryptoAuditEngine"),
    ("bug-bounty-triage-agent", "bug_bounty_triage", "BugBountyTriageEngine"),
    ("incident-legal-bridge-agent", "incident_legal_bridge", "IncidentLegalBridgeEngine"),
    ("pricing-strategist-agent", "pricing_strategist", "PricingStrategistEngine"),
    ("sales-coach-agent", "sales_coach", "SalesCoachEngine"),
    ("proposal-forge-agent", "proposal_forge", "ProposalForgeEngine"),
    ("revenue-ops-agent", "revenue_ops", "RevenueOpsEngine"),
    ("churn-prophet-agent", "churn_prophet", "ChurnProphetEngine"),
    ("partner-ecosystem-agent", "partner_ecosystem", "PartnerEcosystemEngine"),
    ("sales-enablement-agent", "sales_enablement", "SalesEnablementEngine"),
    ("gong-clone-agent", "gong_clone", "GongCloneEngine"),
    ("account-plan-agent", "account_plan", "AccountPlanEngine"),
    ("forecast-radar-agent", "forecast_radar", "ForecastRadarEngine"),
    ("win-loss-analyst-agent", "win_loss_analyst", "WinLossAnalystEngine"),
    ("event-roi-agent", "event_roi", "EventRoiEngine"),
    ("growth-loops-agent", "growth_loops", "GrowthLoopsEngine"),
    ("influencer-scout-agent", "influencer_scout", "InfluencerScoutEngine"),
    ("brand-voice-agent", "brand_voice", "BrandVoiceEngine"),
    ("lifecycle-marketer-agent", "lifecycle_marketer", "LifecycleMarketerEngine"),
    ("community-builder-agent", "community_builder", "CommunityBuilderEngine"),
    ("web-analytics-agent", "web_analytics", "WebAnalyticsEngine"),
    ("paid-social-surgeon-agent", "paid_social_surgeon", "PaidSocialSurgeonEngine"),
    ("affiliate-ops-agent", "affiliate_ops", "AffiliateOpsEngine"),
    ("pr-pitch-agent", "pr_pitch", "PrPitchEngine"),
    ("launch-telemetry-agent", "launch_telemetry", "LaunchTelemetryEngine"),
    ("referral-architect-agent", "referral_architect", "ReferralArchitectEngine"),
    ("local-seo-agent", "local_seo", "LocalSeoEngine"),
    ("video-growth-agent", "video_growth", "VideoGrowthEngine"),
    ("ux-research-agent", "ux_research", "UxResearchEngine"),
    ("roadmap-architect-agent", "roadmap_architect", "RoadmapArchitectEngine"),
    ("spec-writer-agent", "spec_writer", "SpecWriterEngine"),
    ("design-system-agent", "design_system", "DesignSystemEngine"),
    ("user-journey-agent", "user_journey", "UserJourneyEngine"),
    ("ab-test-architect-agent", "ab_test_architect", "AbTestArchitectEngine"),
    ("accessibility-auditor-agent", "accessibility_auditor", "AccessibilityAuditorEngine"),
    ("localization-pilot-agent", "localization_pilot", "LocalizationPilotEngine"),
    ("feedback-miner-agent", "feedback_miner", "FeedbackMinerEngine"),
    ("jobs-to-be-done-agent", "jobs_to_be_done", "JobsToBeDoneEngine"),
    ("procurement-scout-agent", "procurement_scout", "ProcurementScoutEngine"),
    ("contract-lifecycle-agent", "contract_lifecycle", "ContractLifecycleEngine"),
    ("tax-navigator-agent", "tax_navigator", "TaxNavigatorEngine"),
    ("treasury-ops-agent", "treasury_ops", "TreasuryOpsEngine"),
    ("audit-trail-agent", "audit_trail", "AuditTrailEngine"),
    ("vendor-risk-agent", "vendor_risk", "VendorRiskEngine"),
    ("kpi-ledger-agent", "kpi_ledger", "KpiLedgerEngine"),
    ("okr-coach-agent", "okr_coach", "OkrCoachEngine"),
    ("meeting-ops-agent", "meeting_ops", "MeetingOpsEngine"),
    ("policy-drafter-agent", "policy_drafter", "PolicyDrafterEngine"),
    ("real-estate-scout-agent", "real_estate_scout", "RealEstateScoutEngine"),
    ("insurance-advisor-agent", "insurance_advisor", "InsuranceAdvisorEngine"),
    ("talent-sourcer-agent", "talent_sourcer", "TalentSourcerEngine"),
    ("performance-review-agent", "performance_review", "PerformanceReviewEngine"),
    ("compensation-benchmark-agent", "compensation_benchmark", "CompensationBenchmarkEngine"),
    ("learning-path-agent", "learning_path", "LearningPathEngine"),
    ("workforce-planner-agent", "workforce_planner", "WorkforcePlannerEngine"),
    ("exit-insight-agent", "exit_insight", "ExitInsightEngine"),
    ("dei-auditor-agent", "dei_auditor", "DeiAuditorEngine"),
    ("manager-coach-agent", "manager_coach", "ManagerCoachEngine"),
    ("csat-surgeon-agent", "csat_surgeon", "CsatSurgeonEngine"),
    ("knowledge-ops-agent", "knowledge_ops", "KnowledgeOpsEngine"),
    ("support-qa-agent", "support_qa", "SupportQaEngine"),
    ("renewal-orchestrator-agent", "renewal_orchestrator", "RenewalOrchestratorEngine"),
    ("community-support-agent", "community_support", "CommunitySupportEngine"),
    ("nps-driver-agent", "nps_driver", "NpsDriverEngine"),
    ("self-serve-architect-agent", "self_serve_architect", "SelfServeArchitectEngine"),
    ("podcast-producer-agent", "podcast_producer", "PodcastProducerEngine"),
    ("newsletter-architect-agent", "newsletter_architect", "NewsletterArchitectEngine"),
    ("ugc-curator-agent", "ugc_curator", "UgcCuratorEngine"),
    ("meme-ops-agent", "meme_ops", "MemeOpsEngine"),
    ("press-kit-agent", "press_kit", "PressKitEngine"),
    ("course-builder-agent", "course_builder", "CourseBuilderEngine"),
    ("event-producer-agent", "event_producer", "EventProducerEngine"),
    ("creator-monetization-agent", "creator_monetization", "CreatorMonetizationEngine"),
    ("healthcare-scribe-agent", "healthcare_scribe", "HealthcareScribeEngine"),
    ("legal-ops-agent", "legal_ops", "LegalOpsEngine"),
    ("proptech-analyst-agent", "proptech_analyst", "ProptechAnalystEngine"),
    ("edtech-coach-agent", "edtech_coach", "EdtechCoachEngine"),
    ("fintech-compliance-agent", "fintech_compliance", "FintechComplianceEngine"),
    ("climate-risk-agent", "climate_risk", "ClimateRiskEngine"),
    ("supply-chain-optimizer-agent", "supply_chain_optimizer", "SupplyChainOptimizerEngine"),
    ("retail-merchandiser-agent", "retail_merchandiser", "RetailMerchandiserEngine"),
    ("hospitality-ops-agent", "hospitality_ops", "HospitalityOpsEngine"),
    ("manufacturing-qa-agent", "manufacturing_qa", "ManufacturingQaEngine"),
    ("energy-ops-agent", "energy_ops", "EnergyOpsEngine"),
    ("gov-procurement-agent", "gov_procurement", "GovProcurementEngine"),
    ("nonprofit-impact-agent", "nonprofit_impact", "NonprofitImpactEngine"),
    ("autonomous-researcher-agent", "autonomous_researcher", "AutonomousResearcherEngine"),
    ("eval-judge-agent", "eval_judge", "EvalJudgeEngine"),
    ("tool-smith-agent", "tool_smith", "ToolSmithEngine"),
    ("orchestration-designer-agent", "orchestration_designer", "OrchestrationDesignerEngine"),
    ("memory-ops-agent", "memory_ops", "MemoryOpsEngine"),
    ("adversarial-tester-agent", "adversarial_tester", "AdversarialTesterEngine"),
    ("cost-optimizer-agent", "cost_optimizer", "CostOptimizerEngine"),
    ("skills-librarian-agent", "skills_librarian", "SkillsLibrarianEngine"),
    ("workflow-miner-agent", "workflow_miner", "WorkflowMinerEngine"),
    ("digital-twin-agent", "digital_twin", "DigitalTwinEngine"),
    ("x-growth-hacker-agent", "x_growth_hacker", "XGrowthHackerEngine"),
    ("linkedin-authority-agent", "linkedin_authority", "LinkedinAuthorityEngine"),
    ("youtube-growth-agent", "youtube_growth", "YoutubeGrowthEngine"),
    ("tiktok-virality-agent", "tiktok_virality", "TiktokViralityEngine"),
    ("smm-command-center-agent", "smm_command_center", "SmmCommandCenterEngine"),
    ("influencer-ops-agent", "influencer_ops", "InfluencerOpsEngine"),
    ("social-listening-agent", "social_listening", "SocialListeningEngine"),
    ("content-repurposer-agent", "content_repurposer", "ContentRepurposerEngine"),
    ("community-growth-agent", "community_growth", "CommunityGrowthEngine"),
    ("paid-growth-ops-agent", "paid_growth_ops", "PaidGrowthOpsEngine"),
]

def _load(slug, module, cls_name):
    path = os.path.join(AGENTS_DIR, slug, "core", f"{module}_engine.py")
    spec = importlib.util.spec_from_file_location(f"{slug}_{module}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, cls_name)


class TestPower150Structure(unittest.TestCase):
    def test_exactly_one_hundred_fifty_agents(self):
        self.assertEqual(len(POWER150), 150)
        self.assertEqual(len({s for s, _, _ in POWER150}), 150)

    def test_every_agent_has_skill_core_cli(self):
        for slug, module, _ in POWER150:
            base = os.path.join(AGENTS_DIR, slug)
            self.assertTrue(os.path.isfile(os.path.join(base, "SKILL.md")), f"{slug}: SKILL.md missing")
            self.assertTrue(os.path.isfile(os.path.join(base, "core", f"{module}_engine.py")),
                            f"{slug}: engine missing")
            self.assertTrue(os.path.isfile(os.path.join(base, "cli", f"{module}.py")),
                            f"{slug}: CLI missing")

    def test_skill_md_frontmatter_parses(self):
        import yaml
        for slug, _, _ in POWER150:
            content = open(os.path.join(AGENTS_DIR, slug, "SKILL.md"), encoding="utf-8").read()
            self.assertTrue(content.startswith("---"), f"{slug}: no frontmatter")
            meta = yaml.safe_load(content.split("---", 2)[1])
            for key in ("name", "description", "version"):
                self.assertIn(key, meta, f"{slug}: frontmatter missing {key}")

    def test_registry_discovers_power150(self):
        sys.path.insert(0, REPO_ROOT)
        from core.registry import AgentRegistry
        agents = AgentRegistry.discover_agents()
        for slug, _, _ in POWER150:
            self.assertIn(slug, agents, f"{slug} not auto-discovered by registry")


class TestPower150CLIs(unittest.TestCase):
    def test_every_cli_help_from_neutral_cwd(self):
        failures = []
        for slug, module, _ in POWER150:
            cli = os.path.join(AGENTS_DIR, slug, "cli", f"{module}.py")
            proc = subprocess.run([sys.executable, cli, "--help"],
                                  capture_output=True, text=True, timeout=60, cwd="/tmp")
            if proc.returncode != 0:
                failures.append((slug, proc.stderr.strip()[-200:]))
            elif "usage:" not in proc.stdout.lower():
                failures.append((slug, "no usage in stdout"))
        self.assertEqual(failures, [], f"CLI failures: {failures}")


class TestPower150Engines(unittest.TestCase):
    def _smoke(self, slug, module, cls_name, fn):
        Engine = _load(slug, module, cls_name)
        fn(Engine)

    def test_all_engines_analyze_and_format(self):
        for slug, module, cls_name in POWER150:
            with self.subTest(agent=slug):
                Engine = _load(slug, module, cls_name)
                # representative input - should produce verdict and score
                text = f"Sample input for {slug}: this is a representative paragraph with enough content to exercise the deterministic heuristics. It includes domain keywords like {slug.replace('-agent','').replace('-',' ')} and a second sentence.\n- bullet one: value\n- bullet two: value"
                result = Engine.analyze(text)
                self.assertIn(result.verdict, ["PASS","PASS_WITH_NOTES","NEEDS_REVIEW","BLOCKED","NEEDS_INPUT"])
                self.assertGreaterEqual(result.score, 0)
                self.assertLessEqual(result.score, 100)
                report = Engine.format_report(result)
                self.assertIn(result.verdict, report)
                self.assertIn("score", report.lower())

if __name__ == "__main__":
    unittest.main()
