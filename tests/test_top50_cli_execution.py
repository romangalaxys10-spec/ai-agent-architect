"""CLI execution tests: run every Top-50 agent's CLI with real input
(not just --help) so format methods and arg wiring are exercised end-to-end.
Catches the 'engine works but CLI/format crashes' bug class."""
import os
import subprocess
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AGENTS_DIR = os.path.join(REPO_ROOT, "agents")

# slug -> CLI args that produce a valid, non-empty run
CLI_RUNS = {
    "code-review-sentinel": ["--code", "def f(x=[]):\n    try:\n        eval(x)\n    except:\n        pass\n"],
    "test-forge-agent": ["--source", "def add(a, b):\n    if a:\n        return a + b\n    return 0\n"],
    "bug-triage-agent": ["--report", "Traceback error for all users after deploy, expected preview"],
    "ci-surgeon-agent": ["--log", "FAILED test AssertionError: Expected 4 got 5. exit code 137 Killed"],
    "refactor-pilot-agent": ["--source", "def f(a,b,c,d,e,f,g,h):\n    return 1\n"],
    "doc-scribe-agent": ["--source", '"""Mod."""\ndef public_fn(a):\n    """Doc."""\n    return a\n'],
    "sast-sentinel-agent": ["--code", 'API_KEY = "sk-1234567890abcdef"\npickle.loads(data)\n'],
    "dep-guardian-agent": ["--deps", "django==2.2\nrequests>=2.20\nflask\n"],
    "migration-planner-agent": ["--from", "Python 3.9", "--to", "Python 3.12", "--inventory", "main.py\napi.py"],
    "commit-crafter-agent": ["--diff", "diff --git a/src/api.py b/src/api.py\n+++ b/src/api.py\n+def new():\n+    return 1\n"],
    "ticket-router-agent": ["--ticket", "URGENT site is down all users error 500 cannot access"],
    "kb-curator-agent": ["--kb", '[{"id":"a1","title":"reset password","body":"reset password steps","updated":"2024-01-01"}]',
                          "--ticket-themes", "billing refund"],
    "escalation-shield-agent": ["--signals", '{"account":"Acme","tickets_30d":9,"tickets_prev_30d":3,"open_tickets":5,"oldest_open_days":12,"sentiment":"angry","usage_drop_pct":45,"mrr":5000}'],
    "voice-of-customer-agent": ["--feedback", "the app is slow and crashes\nlove the new ui\nsupport is terrible"],
    "sla-sentinel-agent": ["--queue", '[{"id":"T1","priority":"P1","age_hours":3.8,"sla_hours":4},{"id":"T2","priority":"P3","age_hours":80,"sla_hours":72}]'],
    "lead-qualifier-agent": ["--lead", "VP Engineering at ScaleCo raised Series B need incident fix this quarter budget $50k"],
    "outreach-personalizer-agent": ["--prospect", "John is CTO at DataPipe, scaling after Series A, hiring 10 engineers"],
    "meeting-brief-agent": ["--topic", "renewal", "--attendees", "Sarah (VP Eng), Tom (CFO)", "--context", "renewal in 30 days"],
    "crm-hygiene-agent": ["--records", '[{"name":"Acme","email":"a@acme.com","company":"Acme","stage":"demo","value":100,"owner":"j","last_touch":5},{"name":"Acme","email":"a@acme.com","company":"Acme","stage":"","value":null,"owner":"","last_touch":120}]'],
    "competitor-radar-agent": ["--events", "2026-01 | RivalCo | cuts pricing 20% across plans"],
    "seo-content-strategist-agent": ["--keyword", "ai agent testing", "--audience", "eng leaders"],
    "ad-campaign-optimizer-agent": ["--campaigns", '[{"name":"brand","spend":1000,"impressions":100000,"clicks":5000,"conversions":200,"revenue":6000},{"name":"display","spend":800,"impressions":200000,"clicks":800,"conversions":5,"revenue":100}]'],
    "deep-research-agent": ["--question", "does it work?", "--sources", "A 2023 study found 13% gain.\n---\nAnother study found the same 13% improvement."],
    "data-analyst-agent": ["--data", "x,y\n1,10\n2,20\n3,31\n4,39\n5,52\n6,58\n"],
    "fact-check-agent": ["--claim", "the company has 500 employees", "--evidence", "confirms the company has 500 employees"],
    "market-scout-agent": ["--market", "AI testing tools", "--inputs", "population: 50000\nprice: 1200\nshare: 10\ngrowth: 30\ncompetitors: 5"],
    "literature-review-agent": ["--abstracts", "Title: agents prod. Randomized evaluation N=200. 2024.\n---\nTitle: agent failures. Survey N=85. 2025."],
    "email-triage-agent": ["--emails", '[{"from":"ceo@c.com","subject":"URGENT approve","body":"need approval today"},{"from":"noreply@x.com","subject":"digest","body":"fyi automated"}]'],
    "calendar-architect-agent": ["--day", '{"work_start":540,"work_end":1020,"meetings":[{"start":600,"duration_min":60,"title":"standup"}],"tasks":[{"name":"report","duration_min":90,"deadline_hour":900,"priority":1}]}'],
    "meeting-scribe-agent": ["--notes", "We decided to ship v2 Friday. Sarah will write notes by Thursday. Tom should schedule sync. Question: rollback?"],
    "trip-compass-agent": ["--destination", "Tokyo", "--days", "3", "--preferences", "culture, food", "--budget", "1500"],
    "deal-hunter-agent": ["--candidates", '[{"name":"pro","price":800,"reference_price":1200,"rating":4.5,"reviews":500,"features":["16gb ram"]}]', "--needs", "16gb ram"],
    "invoice-intake-agent": ["--invoice", "From: Acme | Invoice #INV-1001 | Due: net 30 | Consulting 3 x $500.00 = $1500.00 | Subtotal: $1500.00 | Tax 10%: $150.00 | Total: $1650.00"],
    "expense-auditor-agent": ["--expenses", '[{"merchant":"Grill","amount":120,"category":"meal","date":"2026-01-06","receipt":true},{"merchant":"Hotel","amount":300,"category":"hotel","date":"2026-01-07","receipt":true}]'],
    "finstat-analyst-agent": ["--data", '{"periods":["Q1","Q2","Q3","Q4"],"items":{"revenue":[100,120,145,180],"cogs":[40,47,56,68],"opex":[200,210,220,230],"cash":[500,460,415,365],"receivables":[20,24,30,44]}}'],
    "portfolio-scout-agent": ["--holdings", '[{"symbol":"AAPL","value":40000,"sector":"technology","asset_class":"equity"},{"symbol":"BTC","value":30000,"sector":"crypto","asset_class":"crypto"}]'],
    "resume-screener-agent": ["--resume", "Senior engineer 8 years. Python, Django, Kubernetes, AWS. Led team of 5.",
                               "--job", "Requires Python, Kubernetes, AWS. 5+ years. Nice to have: Rust."],
    "interview-coach-agent": ["--role", "Backend Engineer", "--level", "senior", "--competencies", "coding, system design"],
    "onboarding-guide-agent": ["--role", "Software Engineer", "--team", "Platform", "--start-date", "Monday"],
    "culture-pulse-agent": ["--survey", '[{"segment":"eng","score":9,"comment":"great growth"},{"segment":"sales","score":4,"comment":"overworked understaffed meetings chaos"}]'],
    "content-calendar-agent": ["--goal", "AI agent testing", "--audience", "eng leaders", "--channels", "blog, x", "--weeks", "2"],
    "script-writer-agent": ["--topic", "RAG evaluation", "--duration", "480", "--style", "educational", "--platform", "youtube"],
    "social-media-manager-agent": ["--topic", "context engineering", "--platform", "x", "--voice", "technical, direct"],
    "copy-editor-agent": ["--text", "The report was written by the team and it was very basically decided to leverage synergies."],
    "cloud-cost-optimizer-agent": ["--inventory", '[{"id":"i-1","type":"vm","size":"xlarge","cpu_util":1,"running_hours_per_day":24,"monthly_cost":140},{"id":"v-9","type":"volume","attached":0,"monthly_cost":20}]'],
    "incident-commander-agent": ["--signals", "Alert: checkout API down, 100% of users affected, 5xx errors, possible data loss"],
    "access-review-agent": ["--grants", '[{"user":"alice","role":"admin","resource":"prod-db","last_used_days":120,"mfa":true},{"user":"bob","role":"read","resource":"reports","last_used_days":5,"mfa":true}]'],
    "socratic-tutor-agent": ["--topic", "recursion", "--level", "beginner", "--goal", "core concepts"],
    "language-coach-agent": ["--text", "I have an information. She depend of result. He go to school."],
    "contract-reviewer-agent": ["--contract", "Provider owns all work product. Customer shall indemnify provider for any and all claims. This agreement renews automatically.", "--side", "buyer"],
}


class TestTop50CLIExecution(unittest.TestCase):
    def test_every_cli_runs_with_real_input(self):
        self.assertEqual(len(CLI_RUNS), 50, "expected exactly 50 CLI run specs")
        failures = []
        for slug, args in CLI_RUNS.items():
            cli = os.path.join(AGENTS_DIR, slug, "cli",
                               os.listdir(os.path.join(AGENTS_DIR, slug, "cli"))and
                               next(f for f in os.listdir(os.path.join(AGENTS_DIR, slug, "cli"))
                                    if f.endswith(".py") and f != "__init__.py"))
            proc = subprocess.run([sys.executable, cli, *args],
                                  capture_output=True, text=True, timeout=60, cwd="/tmp")
            if proc.returncode != 0 or len(proc.stdout.strip()) < 50:
                failures.append((slug, (proc.stderr or proc.stdout).strip()[-150:]))
        self.assertEqual(failures, [], f"CLI execution failures: {failures}")


if __name__ == "__main__":
    unittest.main()
