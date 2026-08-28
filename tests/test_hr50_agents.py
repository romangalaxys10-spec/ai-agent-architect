"""Contract + functional tests for the 50 HR/HRBP/L&D deep series.

Every agent: HR-grade offline engine + CLI + SKILL.md contract (PII/bias guardrails).
"""
import importlib.util
import os
import subprocess
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AGENTS_DIR = os.path.join(REPO_ROOT, "agents")

HR50 = [
    ("hrbp-strategic-partner-agent", "hrbp_strategic_partner", "HrbpStrategicPartnerEngine"),
    ("org-effectiveness-agent", "org_effectiveness", "OrgEffectivenessEngine"),
    ("change-champion-agent", "change_champion", "ChangeChampionEngine"),
    ("business-alignment-agent", "business_alignment", "BusinessAlignmentEngine"),
    ("stakeholder-influence-agent", "stakeholder_influence", "StakeholderInfluenceEngine"),
    ("workforce-shaping-agent", "workforce_shaping", "WorkforceShapingEngine"),
    ("hrbp-coaching-agent", "hrbp_coaching", "HrbpCoachingEngine"),
    ("transformation-lead-agent", "transformation_lead", "TransformationLeadEngine"),
    ("people-analytics-storyteller-agent", "people_analytics_storyteller", "PeopleAnalyticsStorytellerEngine"),
    ("strategic-workforce-advisor-agent", "strategic_workforce_advisor", "StrategicWorkforceAdvisorEngine"),
    ("hr-risk-compliance-agent", "hr_risk_compliance", "HrRiskComplianceEngine"),
    ("future-of-work-architect-agent", "future_of_work_architect", "FutureOfWorkArchitectEngine"),
    ("talent-intelligence-agent", "talent_intelligence", "TalentIntelligenceEngine"),
    ("employer-value-agent", "employer_value", "EmployerValueEngine"),
    ("candidate-experience-agent", "candidate_experience", "CandidateExperienceEngine"),
    ("hiring-manager-enablement-agent", "hiring_manager_enablement", "HiringManagerEnablementEngine"),
    ("assessment-validation-agent", "assessment_validation", "AssessmentValidationEngine"),
    ("internal-mobility-marketplace-agent", "internal_mobility_marketplace", "InternalMobilityMarketplaceEngine"),
    ("performance-enablement-agent", "performance_enablement", "PerformanceEnablementEngine"),
    ("goal-alignment-agent", "goal_alignment", "GoalAlignmentEngine"),
    ("feedback-culture-agent", "feedback_culture", "FeedbackCultureEngine"),
    ("nine-box-talent-agent", "nine_box_talent", "NineBoxTalentEngine"),
    ("succession-risk-agent", "succession_risk", "SuccessionRiskEngine"),
    ("career-mobility-agent", "career_mobility", "CareerMobilityEngine"),
    ("talent-calibration-agent", "talent_calibration", "TalentCalibrationEngine"),
    ("learning-needs-diagnostician-agent", "learning_needs_diagnostician", "LearningNeedsDiagnosticianEngine"),
    ("skills-ontology-agent", "skills_ontology", "SkillsOntologyEngine"),
    ("capability-planner-agent", "capability_planner", "CapabilityPlannerEngine"),
    ("learning-strategy-architect-agent", "learning_strategy_architect", "LearningStrategyArchitectEngine"),
    ("learning-ecosystem-agent", "learning_ecosystem", "LearningEcosystemEngine"),
    ("future-skills-scout-agent", "future_skills_scout", "FutureSkillsScoutEngine"),
    ("instructional-architect-agent", "instructional_architect", "InstructionalArchitectEngine"),
    ("blended-learning-agent", "blended_learning", "BlendedLearningEngine"),
    ("cohort-learning-agent", "cohort_learning", "CohortLearningEngine"),
    ("social-learning-agent", "social_learning", "SocialLearningEngine"),
    ("microlearning-crafter-agent", "microlearning_crafter", "MicrolearningCrafterEngine"),
    ("scenario-simulation-agent", "scenario_simulation", "ScenarioSimulationEngine"),
    ("video-learning-producer-agent", "video_learning_producer", "VideoLearningProducerEngine"),
    ("facilitation-master-agent", "facilitation_master", "FacilitationMasterEngine"),
    ("learning-analytics-agent", "learning_analytics", "LearningAnalyticsEngine"),
    ("kirkpatrick-evaluator-agent", "kirkpatrick_evaluator", "KirkpatrickEvaluatorEngine"),
    ("learning-roi-agent", "learning_roi", "LearningRoiEngine"),
    ("lms-ops-agent", "lms_ops", "LmsOpsEngine"),
    ("learning-vendor-agent", "learning_vendor", "LearningVendorEngine"),
    ("listening-strategy-agent", "listening_strategy", "ListeningStrategyEngine"),
    ("recognition-rituals-agent", "recognition_rituals", "RecognitionRitualsEngine"),
    ("inclusion-belonging-agent", "inclusion_belonging", "InclusionBelongingEngine"),
    ("wellbeing-strategist-agent", "wellbeing_strategist", "WellbeingStrategistEngine"),
    ("resilience-burnout-agent", "resilience_burnout", "ResilienceBurnoutEngine"),
    ("team-effectiveness-agent", "team_effectiveness", "TeamEffectivenessEngine"),
]

def _load(slug, module, cls_name):
    path=os.path.join(AGENTS_DIR, slug, "core", f"{module}_engine.py")
    spec=importlib.util.spec_from_file_location(f"{slug}_{module}", path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, cls_name)

class TestHR50Structure(unittest.TestCase):
    def test_exactly_fifty(self):
        self.assertEqual(len(HR50), 50)
        self.assertEqual(len({s for s,_,_ in HR50}), 50)
    def test_every_agent_has_skill_core_cli(self):
        for slug, module, _ in HR50:
            base=os.path.join(AGENTS_DIR, slug)
            self.assertTrue(os.path.isfile(os.path.join(base, "SKILL.md")), f"{slug}: SKILL.md")
            self.assertTrue(os.path.isfile(os.path.join(base, "core", f"{module}_engine.py")), f"{slug}: engine")
            self.assertTrue(os.path.isfile(os.path.join(base, "cli", f"{module}.py")), f"{slug}: CLI")
    def test_skill_md_frontmatter_parses(self):
        import yaml
        for slug, _, _ in HR50:
            content=open(os.path.join(AGENTS_DIR, slug, "SKILL.md"), encoding="utf-8").read()
            self.assertTrue(content.startswith("---"), f"{slug}: no frontmatter")
            meta=yaml.safe_load(content.split("---",2)[1])
            for key in ("name","description","version"):
                self.assertIn(key, meta, f"{slug}: missing {key}")
    def test_registry_discovers(self):
        sys.path.insert(0, REPO_ROOT)
        from core.registry import AgentRegistry
        agents=AgentRegistry.discover_agents()
        for slug,_,_ in HR50:
            self.assertIn(slug, agents, f"{slug} not discovered")

class TestHR50CLIs(unittest.TestCase):
    def test_every_cli_help_from_neutral_cwd(self):
        failures=[]
        for slug, module, _ in HR50:
            cli=os.path.join(AGENTS_DIR, slug, "cli", f"{module}.py")
            proc=subprocess.run([sys.executable, cli, "--help"], capture_output=True, text=True, timeout=60, cwd="/tmp")
            if proc.returncode!=0:
                failures.append((slug, proc.stderr.strip()[-200:]))
            elif "usage:" not in proc.stdout.lower():
                failures.append((slug, "no usage"))
        self.assertEqual(failures, [], f"CLI failures: {failures}")

class TestHR50Engines(unittest.TestCase):
    def test_all_engines_analyze_and_format(self):
        for slug, module, cls_name in HR50:
            with self.subTest(agent=slug):
                Engine=_load(slug, module, cls_name)
                text=f"Sample for {slug}: HRBP talent learning performance skills succession with action and metric.\n- bullet: value\n- bullet2: value\nMore content for depth and measure."
                result=Engine.analyze(text)
                self.assertIn(result.verdict, ["PASS","PASS_WITH_NOTES","NEEDS_REVIEW","BLOCKED","NEEDS_INPUT"])
                self.assertGreaterEqual(result.score, 0)
                self.assertLessEqual(result.score, 100)
                self.assertIn("hr_signal_hits", result.metrics)
                report=Engine.format_report(result)
                self.assertIn(result.verdict, report)

if __name__=="__main__":
    unittest.main()
