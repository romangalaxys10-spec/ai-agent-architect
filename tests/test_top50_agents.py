"""Contract + functional tests for the Top-50 demand-driven agent suite.

Covers: structural completeness (SKILL.md/core/cli), frontmatter validity,
CLI executability from a neutral cwd, and engine-level functional smoke tests
with representative inputs for every one of the 50 agents.
"""
import importlib.util
import json
import os
import subprocess
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AGENTS_DIR = os.path.join(REPO_ROOT, "agents")

TOP50 = [
    # slug, module, engine class
    ("code-review-sentinel", "code_review", "CodeReviewSentinelEngine"),
    ("test-forge-agent", "test_forge", "TestForgeEngine"),
    ("bug-triage-agent", "bug_triage", "BugTriageEngine"),
    ("ci-surgeon-agent", "ci_surgeon", "CISurgeonEngine"),
    ("refactor-pilot-agent", "refactor_pilot", "RefactorPilotEngine"),
    ("doc-scribe-agent", "doc_scribe", "DocScribeEngine"),
    ("sast-sentinel-agent", "sast_sentinel", "SASTSentinelEngine"),
    ("dep-guardian-agent", "dep_guardian", "DepGuardianEngine"),
    ("migration-planner-agent", "migration_planner", "MigrationPlannerEngine"),
    ("commit-crafter-agent", "commit_crafter", "CommitCrafterEngine"),
    ("ticket-router-agent", "ticket_router", "TicketRouterEngine"),
    ("kb-curator-agent", "kb_curator", "KBCuratorEngine"),
    ("escalation-shield-agent", "escalation_shield", "EscalationShieldEngine"),
    ("voice-of-customer-agent", "voice_of_customer", "VoiceOfCustomerEngine"),
    ("sla-sentinel-agent", "sla_sentinel", "SLASentinelEngine"),
    ("lead-qualifier-agent", "lead_qualifier", "LeadQualifierEngine"),
    ("outreach-personalizer-agent", "outreach_personalizer", "OutreachPersonalizerEngine"),
    ("meeting-brief-agent", "meeting_brief", "MeetingBriefEngine"),
    ("crm-hygiene-agent", "crm_hygiene", "CRMHygieneEngine"),
    ("competitor-radar-agent", "competitor_radar", "CompetitorRadarEngine"),
    ("seo-content-strategist-agent", "seo_content", "SEOContentStrategistEngine"),
    ("ad-campaign-optimizer-agent", "ad_campaign", "AdCampaignOptimizerEngine"),
    ("deep-research-agent", "deep_research", "DeepResearchEngine"),
    ("data-analyst-agent", "data_analyst", "DataAnalystEngine"),
    ("fact-check-agent", "fact_check", "FactCheckEngine"),
    ("market-scout-agent", "market_scout", "MarketScoutEngine"),
    ("literature-review-agent", "literature_review", "LiteratureReviewEngine"),
    ("email-triage-agent", "email_triage", "EmailTriageEngine"),
    ("calendar-architect-agent", "calendar_architect", "CalendarArchitectEngine"),
    ("meeting-scribe-agent", "meeting_scribe", "MeetingScribeEngine"),
    ("trip-compass-agent", "trip_compass", "TripCompassEngine"),
    ("deal-hunter-agent", "deal_hunter", "DealHunterEngine"),
    ("invoice-intake-agent", "invoice_intake", "InvoiceIntakeEngine"),
    ("expense-auditor-agent", "expense_auditor", "ExpenseAuditorEngine"),
    ("finstat-analyst-agent", "finstat", "FinStatAnalystEngine"),
    ("portfolio-scout-agent", "portfolio_scout", "PortfolioScoutEngine"),
    ("resume-screener-agent", "resume_screener", "ResumeScreenerEngine"),
    ("interview-coach-agent", "interview_coach", "InterviewCoachEngine"),
    ("onboarding-guide-agent", "onboarding_guide", "OnboardingGuideEngine"),
    ("culture-pulse-agent", "culture_pulse", "CulturePulseEngine"),
    ("content-calendar-agent", "content_calendar", "ContentCalendarEngine"),
    ("script-writer-agent", "script_writer", "ScriptWriterEngine"),
    ("social-media-manager-agent", "social_media", "SocialMediaManagerEngine"),
    ("copy-editor-agent", "copy_editor", "CopyEditorEngine"),
    ("cloud-cost-optimizer-agent", "cloud_cost", "CloudCostOptimizerEngine"),
    ("incident-commander-agent", "incident_commander", "IncidentCommanderEngine"),
    ("access-review-agent", "access_review", "AccessReviewEngine"),
    ("socratic-tutor-agent", "socratic_tutor", "SocraticTutorEngine"),
    ("language-coach-agent", "language_coach", "LanguageCoachEngine"),
    ("contract-reviewer-agent", "contract_reviewer", "ContractReviewerEngine"),
]

def _load(slug, module, cls_name):
    path = os.path.join(AGENTS_DIR, slug, "core", f"{module}_engine.py")
    spec = importlib.util.spec_from_file_location(f"{slug}_{module}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, cls_name)


class TestTop50Structure(unittest.TestCase):
    def test_exactly_fifty_agents_in_suite(self):
        self.assertEqual(len(TOP50), 50)
        self.assertEqual(len({s for s, _, _ in TOP50}), 50)

    def test_every_agent_has_skill_core_cli(self):
        for slug, module, _ in TOP50:
            base = os.path.join(AGENTS_DIR, slug)
            self.assertTrue(os.path.isfile(os.path.join(base, "SKILL.md")), f"{slug}: SKILL.md missing")
            self.assertTrue(os.path.isfile(os.path.join(base, "core", f"{module}_engine.py")),
                            f"{slug}: engine missing")
            self.assertTrue(os.path.isfile(os.path.join(base, "cli", f"{module}.py")),
                            f"{slug}: CLI missing")

    def test_skill_md_frontmatter_parses(self):
        import yaml
        for slug, _, _ in TOP50:
            content = open(os.path.join(AGENTS_DIR, slug, "SKILL.md"), encoding="utf-8").read()
            self.assertTrue(content.startswith("---"), f"{slug}: no frontmatter")
            meta = yaml.safe_load(content.split("---", 2)[1])
            for key in ("name", "description", "version"):
                self.assertIn(key, meta, f"{slug}: frontmatter missing {key}")

    def test_registry_discovers_top50(self):
        sys.path.insert(0, REPO_ROOT)
        from core.registry import AgentRegistry
        agents = AgentRegistry.discover_agents()
        for slug, _, _ in TOP50:
            self.assertIn(slug, agents, f"{slug} not auto-discovered by registry")


class TestTop50CLIs(unittest.TestCase):
    def test_every_cli_help_from_neutral_cwd(self):
        failures = []
        for slug, module, _ in TOP50:
            cli = os.path.join(AGENTS_DIR, slug, "cli", f"{module}.py")
            proc = subprocess.run([sys.executable, cli, "--help"],
                                  capture_output=True, text=True, timeout=60, cwd="/tmp")
            if proc.returncode != 0:
                failures.append((slug, proc.stderr.strip()[-120:]))
        self.assertEqual(failures, [], f"CLI failures: {failures}")


class TestTop50Engines(unittest.TestCase):
    """One functional smoke test per agent with a representative input."""

    def _smoke(self, slug, module, cls_name, fn):
        engine = _load(slug, module, cls_name)
        fn(engine)

    def test_code_review_sentinel(self):
        def fn(E):
            r = E.review("def f(x=[]):\n    try:\n        return eval(x)\n    except:\n        pass\n")
            rules = {f.rule for f in r.findings}
            self.assertIn("mutable-default-arg", rules)
            self.assertIn("bare-except", rules)
            self.assertIn("eval-use", rules)
            self.assertEqual(r.verdict, "NEEDS_CHANGES")
            self.assertIn("VERDICT", E.format_report(r))
        self._smoke("code-review-sentinel", "code_review", "CodeReviewSentinelEngine", fn)

    def test_test_forge(self):
        def fn(E):
            src = "def add(a, b):\n    if a > 0:\n        return a + b\n    return 0\n"
            p = E.forge(src, target_coverage=80)
            self.assertTrue(p.callables)
            self.assertGreater(len(p.tests), 0)
            self.assertIn("def test_add", p.test_code)
        self._smoke("test-forge-agent", "test_forge", "TestForgeEngine", fn)

    def test_bug_triage(self):
        def fn(E):
            r = E.triage("Steps: 1. upload file. Expected: preview. Actual: Traceback ValueError. "
                         "Happens for all users after deploy v2.3.")
            self.assertEqual(r.defect_class, "crash")
            self.assertTrue(r.hypotheses[0]["probability"] > 0)
            self.assertTrue(r.checklist)
        self._smoke("bug-triage-agent", "bug_triage", "BugTriageEngine", fn)

    def test_ci_surgeon(self):
        def fn(E):
            d = E.diagnose("FAILED tests/test_x.py::test_y AssertionError: Expected 4 got 5\n"
                           "Killed process (OOM) exit code 137")
            self.assertIn(d.failure_class, ("assertion_failure", "oom"))
            self.assertIn("DETERMINISTIC", d.flaky_verdict)
            self.assertTrue(d.playbooks)
        self._smoke("ci-surgeon-agent", "ci_surgeon", "CISurgeonEngine", fn)

    def test_refactor_pilot(self):
        def fn(E):
            src = "\n".join([f"    x{i} = {i} + {i}" for i in range(80)]) + "\n"
            src = "def f(a, b, c, d, e, f, g, h):\n" + src
            p = E.plan(src)
            kinds = {s.kind for s in p.smells}
            self.assertIn("long_param_list", kinds)
            self.assertTrue(p.steps)
        self._smoke("refactor-pilot-agent", "refactor_pilot", "RefactorPilotEngine", fn)

    def test_doc_scribe(self):
        def fn(E):
            src = '"""Module."""\n\n\ndef public_fn(a):\n    """Does things."""\n    return a\n\n\ndef _private():\n    pass\n'
            d = E.document(src)
            self.assertTrue(any(s.name == "public_fn" for s in d.symbols))
            self.assertNotIn("public_fn", d.undocumented_public)
        self._smoke("doc-scribe-agent", "doc_scribe", "DocScribeEngine", fn)

    def test_sast_sentinel(self):
        def fn(E):
            r = E.scan('cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")\n'
                       'API_KEY = "sk-1234567890abcdef"\n')
            rules = {f.rule for f in r.findings}
            self.assertIn("SQL_INJECTION", rules)
            self.assertIn("HARDCODED_SECRET", rules)
            self.assertEqual(r.verdict, "FAIL_SECURITY_GATE")
        self._smoke("sast-sentinel-agent", "sast_sentinel", "SASTSentinelEngine", fn)

    def test_dep_guardian(self):
        def fn(E):
            a = E.audit("django==2.2\nrequests>=2.20\nflask\npyyaml==5.3\n")
            risky = {d.name for d in a.deps if d.risk_score >= 3.5}
            self.assertIn("django", risky)
            self.assertIn("pyyaml", risky)
            self.assertEqual(a.verdict, "SUPPLY_CHAIN_RISK")
        self._smoke("dep-guardian-agent", "dep_guardian", "DepGuardianEngine", fn)

    def test_migration_planner(self):
        def fn(E):
            p = E.plan("Python 3.9", "Python 3.12", "main.py\nutils/api.py\nmodels.py")
            self.assertEqual(len(p.phases), 4)
            self.assertTrue(p.phases[2].requires_hitl)
            self.assertIn("MIGRATION_VIABLE", p.verdict)
        self._smoke("migration-planner-agent", "migration_planner", "MigrationPlannerEngine", fn)

    def test_commit_crafter(self):
        def fn(E):
            p = E.craft("diff --git a/src/api.py b/src/api.py\n+++ b/src/api.py\n+def new_endpoint():\n+    return data\n")
            self.assertIn(p.commit_type, ("feat", "chore"))
            self.assertIn(p.semver_bump, ("minor", "patch"))
        self._smoke("commit-crafter-agent", "commit_crafter", "CommitCrafterEngine", fn)

    def test_ticket_router(self):
        def fn(E):
            d = E.route("URGENT: site is down, all users get error 500, we cannot access anything")
            self.assertEqual(d.category, "outage")
            self.assertEqual(d.priority, "P1")
            self.assertIn("Incident", d.queue)
        self._smoke("ticket-router-agent", "ticket_router", "TicketRouterEngine", fn)

    def test_kb_curator(self):
        def fn(E):
            kb = [
                {"id": "a1", "title": "How to reset password", "body": "reset password steps here", "updated": "2024-01-01"},
                {"id": "a2", "title": "Password reset guide", "body": "reset password steps here", "updated": "2023-01-01"},
            ]
            r = E.curate(kb, ticket_themes=["billing refund"])
            self.assertTrue(r.duplicates)
            self.assertIn("billing refund", r.gaps)
        self._smoke("kb-curator-agent", "kb_curator", "KBCuratorEngine", fn)

    def test_escalation_shield(self):
        def fn(E):
            a = E.assess({"account": "Acme", "tickets_30d": 9, "tickets_prev_30d": 3,
                          "open_tickets": 5, "oldest_open_days": 12, "sentiment": "angry",
                          "usage_drop_pct": 45, "mrr": 5000})
            self.assertGreaterEqual(a.churn_score, 60)
            self.assertIn("CRITICAL", a.tier)
            self.assertTrue(a.save_play)
        self._smoke("escalation-shield-agent", "escalation_shield", "EscalationShieldEngine", fn)

    def test_voice_of_customer(self):
        def fn(E):
            r = E.analyze(["The app is slow and crashes constantly", "Love the new UI, so fast",
                           "Support response time is terrible", "Pricing is too expensive"])
            themes = {t["theme"] for t in r.themes}
            self.assertIn("performance", themes)
            self.assertTrue(r.top_pain_points)
        self._smoke("voice-of-customer-agent", "voice_of_customer", "VoiceOfCustomerEngine", fn)

    def test_sla_sentinel(self):
        def fn(E):
            p = E.project([
                {"id": "T1", "priority": "P1", "age_hours": 3.8, "sla_hours": 4},
                {"id": "T2", "priority": "P2", "age_hours": 5, "sla_hours": 24},
                {"id": "T3", "priority": "P3", "age_hours": 80, "sla_hours": 72},
            ])
            self.assertIn("T3", p.breached)
            self.assertTrue(any("T1" in o for o in p.intervention_order))
        self._smoke("sla-sentinel-agent", "sla_sentinel", "SLASentinelEngine", fn)

    def test_lead_qualifier(self):
        def fn(E):
            v = E.qualify("Jane is VP Engineering at ScaleCo. They raised Series B. "
                          "Need to fix incident response this quarter, budget of $50k approved.")
            self.assertIn(v.tier, ("SQL", "MQL"))
            self.assertGreaterEqual(v.total_score, 55)
            self.assertTrue(v.next_actions)
        self._smoke("lead-qualifier-agent", "lead_qualifier", "LeadQualifierEngine", fn)

    def test_outreach_personalizer(self):
        def fn(E):
            p = E.personalize("John is CTO at DataPipe, scaling after Series A, hiring 10 engineers")
            self.assertEqual(len(p.variants), 3)
            self.assertLess(p.spam_score, 0.3)
            self.assertTrue(p.sequence)
        self._smoke("outreach-personalizer-agent", "outreach_personalizer", "OutreachPersonalizerEngine", fn)

    def test_meeting_brief(self):
        def fn(E):
            b = E.brief("renewal negotiation", ["Sarah (VP Eng)", "Tom (CFO)"], "renewal in 30 days")
            self.assertTrue(b.attendees)
            self.assertTrue(b.agenda)
            self.assertTrue(b.objections)
        self._smoke("meeting-brief-agent", "meeting_brief", "MeetingBriefEngine", fn)

    def test_crm_hygiene(self):
        def fn(E):
            r = E.audit([
                {"name": "Acme Corp", "email": "a@acme.com", "company": "Acme", "stage": "demo", "value": 100, "owner": "j", "last_touch": 5},
                {"name": "Acme Corp", "email": "a@acme.com", "company": "Acme", "stage": "", "value": None, "owner": "", "last_touch": 120},
                {"name": "Globex", "email": "bad-email", "company": "Globex", "stage": "lead", "value": 50, "owner": "k", "last_touch": 10},
            ])
            self.assertTrue(r.duplicates)
            self.assertTrue(r.invalid_contacts)
            self.assertTrue(r.stale)
        self._smoke("crm-hygiene-agent", "crm_hygiene", "CRMHygieneEngine", fn)

    def test_competitor_radar(self):
        def fn(E):
            r = E.analyze(["2026-01 | RivalCo | cuts pricing 20% across all plans",
                           "2026-02 | RivalCo | launches new API feature"])
            cats = {e.category for e in r.events}
            self.assertIn("pricing", cats)
            self.assertTrue(r.top_threats)
        self._smoke("competitor-radar-agent", "competitor_radar", "CompetitorRadarEngine", fn)

    def test_seo_content_strategist(self):
        def fn(E):
            s = E.strategy("ai agent testing", "engineering leaders")
            self.assertEqual(s.intent, "informational")
            self.assertTrue(any(c["type"] == "PILLAR" for c in s.cluster))
            self.assertTrue(s.outline)
        self._smoke("seo-content-strategist-agent", "seo_content", "SEOContentStrategistEngine", fn)

    def test_ad_campaign_optimizer(self):
        def fn(E):
            p = E.optimize([
                {"name": "search-brand", "spend": 1000, "impressions": 100000, "clicks": 5000, "conversions": 200, "revenue": 6000},
                {"name": "display-junk", "spend": 800, "impressions": 200000, "clicks": 800, "conversions": 5, "revenue": 100},
            ], breakeven_roas=2.0)
            by_name = {r.name: r for r in p.rows}
            self.assertEqual(by_name["search-brand"].verdict, "SCALE")
            self.assertEqual(by_name["display-junk"].verdict, "PAUSE")
        self._smoke("ad-campaign-optimizer-agent", "ad_campaign", "AdCampaignOptimizerEngine", fn)

    def test_deep_research(self):
        def fn(E):
            s = E.synthesize("Does remote work reduce productivity?", [
                "A 2023 study found remote workers were 13% more productive. Data shows output increased.",
                "Another 2023 study found remote productivity increased by 13 percent across teams.",
                "However, one report says collaboration networks weakened, with unspecified effects.",
            ])
            self.assertTrue(s.corroboration)
            self.assertIn(s.confidence_band, ("HIGH", "MEDIUM", "LOW"))
        self._smoke("deep-research-agent", "deep_research", "DeepResearchEngine", fn)

    def test_data_analyst(self):
        def fn(E):
            csv = "x,y,c\n1,10,a\n2,20,a\n3,31,a\n4,39,a\n5,52,a\n6,58,a\n"
            a = E.analyze(csv)
            self.assertEqual(a.n_rows, 6)
            corr = {(x, y): r for x, y, r in a.correlations}
            self.assertTrue(any(abs(r) > 0.9 for r in corr.values()))
        self._smoke("data-analyst-agent", "data_analyst", "DataAnalystEngine", fn)

    def test_fact_check(self):
        def fn(E):
            r = E.verify("The company has 500 employees",
                         ["The report confirms the company has 500 employees on staff."])
            self.assertEqual(r.verdict, "CONFIRMED")
            r2 = E.verify("the sky is green", [])
            self.assertEqual(r2.verdict, "UNVERIFIED")
        self._smoke("fact-check-agent", "fact_check", "FactCheckEngine", fn)

    def test_market_scout(self):
        def fn(E):
            s = E.size("AI agent testing tools", {
                "population": 50000, "price": 1200, "share": 10,
                "growth": 30, "competitors": 5})
            self.assertIn("M", s.tam["value"] + s.sam["value"] + s.som["value"])
            self.assertIn(s.entry_verdict.split(" ")[0], ("ENTER", "NICHE", "PASS"))
        self._smoke("market-scout-agent", "market_scout", "MarketScoutEngine", fn)

    def test_literature_review(self):
        def fn(E):
            r = E.review([
                "Title: LLM agents in prod. We conducted a randomized evaluation with N=200. Results show agents improve throughput by 15%. Published 2024.",
                "Title: Agent failures. Survey of N=85 teams. We found no significant improvement in reliability. Published 2025.",
            ])
            self.assertEqual(len(r.papers), 2)
            self.assertTrue(r.clusters)
            self.assertTrue(r.gaps)
        self._smoke("literature-review-agent", "literature_review", "LiteratureReviewEngine", fn)

    def test_email_triage(self):
        def fn(E):
            p = E.triage([
                {"from": "ceo@corp.com", "subject": "URGENT: approve contract by EOD", "body": "need your approval urgently, decision required today"},
                {"from": "noreply@github.com", "subject": "weekly digest", "body": "automated notification fyi"},
            ])
            self.assertEqual(p.items[0].quadrant, "Q1_DO_NOW")
            self.assertEqual(p.items[1].quadrant, "Q4_READ_LATER")
        self._smoke("email-triage-agent", "email_triage", "EmailTriageEngine", fn)

    def test_calendar_architect(self):
        def fn(E):
            s = E.schedule({"work_start": 540, "work_end": 1020,
                            "meetings": [{"start": 600, "duration_min": 60, "title": "standup"}],
                            "tasks": [{"name": "report", "duration_min": 90, "deadline_hour": 900, "priority": 1}]})
            self.assertEqual(s.tasks_scheduled, 1)
            self.assertTrue(any(sl.kind == "focus" for sl in s.slots))
        self._smoke("calendar-architect-agent", "calendar_architect", "CalendarArchitectEngine", fn)

    def test_meeting_scribe(self):
        def fn(E):
            d = E.extract("We decided to ship v2 on Friday. Sarah will write the release notes by Thursday. "
                          "Open question: rollback plan?")
            self.assertEqual(len(d.decisions), 1)
            self.assertTrue(any(a.owner == "Sarah" for a in d.actions))
        self._smoke("meeting-scribe-agent", "meeting_scribe", "MeetingScribeEngine", fn)

    def test_trip_compass(self):
        def fn(E):
            it = E.plan("Tokyo", 3, ["culture", "food"], 1500, pace="balanced")
            self.assertEqual(len(it.days), 3)
            self.assertEqual(sum(it.budget_split.values()), 1500)
        self._smoke("trip-compass-agent", "trip_compass", "TripCompassEngine", fn)

    def test_deal_hunter(self):
        def fn(E):
            v = E.evaluate([
                {"name": "laptop-pro", "price": 800, "reference_price": 1200, "rating": 4.5, "reviews": 500,
                 "features": ["16gb ram", "ssd"]},
                {"name": "laptop-cheap", "price": 590, "reference_price": 600, "rating": 3.2, "reviews": 10,
                 "features": ["4gb ram"]},
            ], needs=["16gb ram"])
            by_name = {c.name: c for c in v.candidates}
            self.assertEqual(by_name["laptop-pro"].verdict, "BUY")
            self.assertEqual(by_name["laptop-cheap"].verdict, "PASS")
        self._smoke("deal-hunter-agent", "deal_hunter", "DealHunterEngine", fn)

    def test_invoice_intake(self):
        def fn(E):
            r = E.process("From: Acme Corp | Invoice #INV-1001 | Date: 2026-01-15 | Due: net 30 | "
                          "Consulting services 3 x $500.00 = $1500.00 | Subtotal: $1500.00 | "
                          "Tax 10%: $150.00 | Total: $1650.00", history=["INV-1000"])
            self.assertEqual(r.invoice_no, "INV-1001")
            self.assertEqual(r.total, 1650.0)
            self.assertEqual(r.exceptions, [])
            self.assertIn("APPROVE", r.posting_recommendation)
        self._smoke("invoice-intake-agent", "invoice_intake", "InvoiceIntakeEngine", fn)

    def test_expense_auditor(self):
        def fn(E):
            r = E.audit([
                {"merchant": "Fancy Grill restaurant", "amount": 120.0, "category": "meal", "date": "2026-01-06", "receipt": True},
                {"merchant": "Hotel Grand", "amount": 300.0, "category": "hotel", "date": "2026-01-07", "receipt": True},
                {"merchant": "Staples", "amount": 60.0, "category": "office", "date": "2026-01-08", "receipt": False},
            ])
            flagged_merchants = {f.merchant for f in r.flags}
            self.assertIn("Fancy Grill restaurant", flagged_merchants)
            self.assertIn("Hotel Grand", flagged_merchants)
        self._smoke("expense-auditor-agent", "expense_auditor", "ExpenseAuditorEngine", fn)

    def test_finstat_analyst(self):
        def fn(E):
            a = E.analyze({"periods": ["Q1", "Q2", "Q3", "Q4"],
                           "items": {"revenue": [100, 120, 145, 180],
                                     "cogs": [40, 47, 56, 68],
                                     "opex": [200, 210, 220, 230],
                                     "cash": [500, 460, 415, 365],
                                     "receivables": [20, 24, 30, 44]}})
            self.assertTrue(a.ratios)
            self.assertLess(a.runway_months, 12)  # burning
            self.assertTrue(a.red_flags)
        self._smoke("finstat-analyst-agent", "finstat", "FinStatAnalystEngine", fn)

    def test_portfolio_scout(self):
        def fn(E):
            r = E.analyze([
                {"symbol": "AAPL", "value": 40000, "sector": "technology", "asset_class": "equity"},
                {"symbol": "MSFT", "value": 35000, "sector": "technology", "asset_class": "equity"},
                {"symbol": "BTC", "value": 30000, "sector": "crypto", "asset_class": "crypto"},
            ])
            self.assertGreater(r.hhi, 0.3)
            self.assertTrue(r.risks)
        self._smoke("portfolio-scout-agent", "portfolio_scout", "PortfolioScoutEngine", fn)

    def test_resume_screener(self):
        def fn(E):
            res = ("Senior engineer, 8 years. Python, Django, Kubernetes, AWS. "
                   "Led team of 5. Shipped ML pipeline. BSc Computer Science.")
            job = "Requires Python, Kubernetes, AWS, system design. 5+ years. Nice to have: Rust, ML."
            r = E.screen(res, job)
            matched = {s.skill for s in r.skills if s.required and s.matched}
            self.assertIn("python", matched)
            self.assertIn("kubernetes", matched)
            self.assertGreaterEqual(r.fit_score, 60)
        self._smoke("resume-screener-agent", "resume_screener", "ResumeScreenerEngine", fn)

    def test_interview_coach(self):
        def fn(E):
            k = E.design("Backend Engineer", "senior", ["coding", "system design", "ownership"])
            self.assertGreater(len(k.questions), 2)
            self.assertTrue(k.rubric)
            self.assertTrue(k.illegal_avoid)
        self._smoke("interview-coach-agent", "interview_coach", "InterviewCoachEngine", fn)

    def test_onboarding_guide(self):
        def fn(E):
            p = E.plan("Software Engineer", "Platform", "Monday")
            self.assertEqual(len(p.gates), 3)
            self.assertTrue(p.week1)
            self.assertTrue(p.access_checklist)
        self._smoke("onboarding-guide-agent", "onboarding_guide", "OnboardingGuideEngine", fn)

    def test_culture_pulse(self):
        def fn(E):
            r = E.analyze([
                {"segment": "eng", "score": 9, "comment": "great growth and learning"},
                {"segment": "eng", "score": 7, "comment": ""},
                {"segment": "sales", "score": 4, "comment": "overworked and understaffed, meetings chaos"},
                {"segment": "sales", "score": 7, "comment": "unclear priorities"},
                {"segment": "eng", "score": 9, "comment": "trust and autonomy"},
            ])
            self.assertGreater(r.enps, 0)
            seg = {s["segment"]: s for s in r.segments}
            self.assertEqual(seg["sales"]["flag"], "investigate")
        self._smoke("culture-pulse-agent", "culture_pulse", "CulturePulseEngine", fn)

    def test_content_calendar(self):
        def fn(E):
            c = E.generate("AI agent testing", "eng leaders", ["blog", "linkedin", "x"], weeks=4)
            self.assertEqual(len(c.entries) >= 12, True)
            self.assertTrue(c.pillars)
        self._smoke("content-calendar-agent", "content_calendar", "ContentCalendarEngine", fn)

    def test_script_writer(self):
        def fn(E):
            s = E.write("RAG evaluation", duration_s=480, style="educational", platform="youtube")
            self.assertTrue(s.beats)
            self.assertTrue(s.hook)
            self.assertTrue(s.cutdowns)
        self._smoke("script-writer-agent", "script_writer", "ScriptWriterEngine", fn)

    def test_social_media_manager(self):
        def fn(E):
            p = E.generate("context engineering for agents", "x", "technical, direct")
            self.assertEqual(len(p.variants), 3)
            self.assertTrue(all(v.char_count <= 280 for v in p.variants))
            self.assertTrue(p.reply_kit)
        self._smoke("social-media-manager-agent", "social_media", "SocialMediaManagerEngine", fn)

    def test_copy_editor(self):
        def fn(E):
            text = ("The report was written by the team. It was very basically decided that the synergies "
                    "of the new paradigm would be leveraged in order to move the needle on our deliverables.")
            r = E.edit(text)
            self.assertGreater(r.filler_count, 0)
            self.assertTrue(r.jargon_hits)
            self.assertNotIn("in order to", r.rewrite)
        self._smoke("copy-editor-agent", "copy_editor", "CopyEditorEngine", fn)

    def test_cloud_cost_optimizer(self):
        def fn(E):
            p = E.optimize([
                {"id": "i-001", "type": "vm", "size": "xlarge", "cpu_util": 1, "running_hours_per_day": 24, "monthly_cost": 140},
                {"id": "i-002", "type": "vm", "size": "large", "cpu_util": 5, "running_hours_per_day": 24, "monthly_cost": 70},
                {"id": "i-003", "type": "vm", "size": "medium", "cpu_util": 60, "running_hours_per_day": 24, "monthly_cost": 35, "env": "prod"},
                {"id": "vol-9", "type": "volume", "attached": 0, "monthly_cost": 20},
            ])
            kinds = {a.kind for a in p.actions}
            self.assertIn("stop", kinds)
            self.assertIn("downsize", kinds)
            self.assertGreater(p.projected_savings, 100)
        self._smoke("cloud-cost-optimizer-agent", "cloud_cost", "CloudCostOptimizerEngine", fn)

    def test_incident_commander(self):
        def fn(E):
            p = E.command("Alert: checkout API down, 100% of users affected, error rate 5xx. "
                          "Possible data loss on orders table.")
            self.assertEqual(p.severity, "SEV1")
            self.assertTrue(any("FREEZE" in r for r in p.runbook))
            self.assertTrue(p.comms_templates)
        self._smoke("incident-commander-agent", "incident_commander", "IncidentCommanderEngine", fn)

    def test_access_review(self):
        def fn(E):
            r = E.review([
                {"user": "alice", "role": "admin", "resource": "prod-database", "last_used_days": 120, "mfa": True},
                {"user": "bob", "role": "read", "resource": "reports", "last_used_days": 5, "mfa": True},
                {"user": "carol", "role": "write", "resource": "prod-secrets", "last_used_days": 200, "mfa": False},
            ])
            risky_users = {u.user for u in r.users_at_risk}
            self.assertIn("alice", risky_users)
            self.assertIn("carol", risky_users)
            self.assertNotIn("bob", risky_users)
        self._smoke("access-review-agent", "access_review", "AccessReviewEngine", fn)

    def test_socratic_tutor(self):
        def fn(E):
            s = E.tutor("recursion", "beginner")
            self.assertTrue(s.ladder)
            self.assertEqual(s.ladder[0].level, "recall")
            self.assertEqual(len(s.ladder[0].hint_ladder), 3)
        self._smoke("socratic-tutor-agent", "socratic_tutor", "SocraticTutorEngine", fn)

    def test_language_coach(self):
        def fn(E):
            p = E.coach("I have an information about this. She depend of the result. "
                        "He go to school. Many student is here.", level="unknown")
            kinds = {e.kind for e in p.errors}
            self.assertIn("article_errors", kinds)
            self.assertIn("preposition_errors", kinds)
            self.assertIn(p.estimated_cefr, ("A1", "A2", "B1", "B2", "C1", "C2"))
        self._smoke("language-coach-agent", "language_coach", "LanguageCoachEngine", fn)

    def test_contract_reviewer(self):
        def fn(E):
            r = E.review("Provider owns all work product. Customer shall indemnify provider for any and all claims. "
                         "This agreement renews automatically. Governing law: Delaware.", side="buyer")
            grades = {c.clause: c.grade for c in r.clauses}
            self.assertEqual(grades["indemnity"], "one-sided")
            self.assertIn("liability_cap", r.missing)
            self.assertTrue(r.risky_terms)
        self._smoke("contract-reviewer-agent", "contract_reviewer", "ContractReviewerEngine", fn)


if __name__ == "__main__":
    unittest.main()
