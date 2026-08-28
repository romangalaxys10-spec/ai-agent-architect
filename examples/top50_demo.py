"""Top-50 Demand-Driven Agent Suite — end-to-end demo.

Runs one representative agent from each of the 10 categories on realistic inputs,
fully offline (zero API keys, deterministic outputs).

Usage:
    python examples/top50_demo.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
AGENTS = os.path.join(REPO, "agents")

DEMOS = [
    ("Coding & Dev", "sast-sentinel-agent/cli/sast_sentinel.py",
     ["--code", 'import pickle\ndef load(b):\n    return pickle.loads(b)  # RCE risk\n']),
    ("Customer Support", "ticket-router-agent/cli/ticket_router.py",
     ["--ticket", "URGENT: we were overcharged $199 on order #A-9231, cancel my account now"]),
    ("Sales & Marketing", "lead-qualifier-agent/cli/lead_qualifier.py",
     ["--lead", "Jane is VP Engineering at ScaleCo, raised Series B, needs incident response fix "
                "this quarter, budget $50k approved"]),
    ("Research & Analysis", "fact-check-agent/cli/fact_check.py",
     ["--claim", "The company has 500 employees and grew revenue 40%",
      "--evidence", "According to the annual report, revenue grew 40%.\n---\n"
                    "The 10-K confirms 500 employees on staff."]),
    ("Personal Productivity", "meeting-scribe-agent/cli/meeting_scribe.py",
     ["--notes", "We decided to ship v2 on Friday. Sarah will write release notes by Thursday. "
                 "Tom should schedule the infra sync. Open question: rollback plan?"]),
    ("Finance", "invoice-intake-agent/cli/invoice_intake.py",
     ["--invoice", "From: Acme Corp | Invoice #INV-1001 | Due: net 30 | "
                   "Consulting 3 x $500.00 = $1500.00 | Subtotal: $1500.00 | "
                   "Tax 10%: $150.00 | Total: $1650.00"]),
    ("HR & Recruiting", "resume-screener-agent/cli/resume_screener.py",
     ["--resume", "Senior engineer, 8 years. Python, Django, Kubernetes, AWS. Led team of 5.",
      "--job", "Requires Python, Kubernetes, AWS, system design. 5+ years. Nice to have: Rust."]),
    ("Content & Creative", "copy-editor-agent/cli/copy_editor.py",
     ["--text", "The report was written by the team. It was very basically decided that the "
                "synergies of the new paradigm would be leveraged in order to move the needle."]),
    ("Ops, IT & Security", "incident-commander-agent/cli/incident_commander.py",
     ["--signals", "Alert: checkout API down, 100% of users affected, 5xx error rate. "
                   "Possible data loss on orders table."]),
    ("Education/Legal/Life", "contract-reviewer-agent/cli/contract_reviewer.py",
     ["--contract", "Provider owns all work product. Customer shall indemnify provider for any "
                    "and all claims. This agreement renews automatically.", "--side", "buyer"]),
]


def main():
    print("=" * 70)
    print("TOP-50 DEMAND-DRIVEN AGENT SUITE — LIVE DEMO (1 per category, 10 of 50)")
    print("=" * 70)
    failures = []
    for i, (cat, rel, args) in enumerate(DEMOS, 1):
        cli = os.path.join(AGENTS, rel)
        print(f"\n[{i}/10] {cat}: {rel.split('/')[0]}")
        print("-" * 70)
        proc = subprocess.run([sys.executable, cli, *args],
                              capture_output=True, text=True, timeout=60, cwd="/tmp")
        if proc.returncode != 0:
            failures.append((cat, proc.stderr[-200:]))
            print(f"  FAILED: {proc.stderr[-300:]}")
            continue
        # print first ~14 lines of output
        for line in proc.stdout.splitlines()[:14]:
            print("  " + line)
    print("\n" + "=" * 70)
    if failures:
        print(f"RESULT: {len(failures)} demo(s) FAILED")
        for cat, err in failures:
            print(f"  - {cat}: {err[:120]}")
        sys.exit(1)
    print("RESULT: all 10 category demos passed. Remaining 40 agents: see agents/AGENTS.md")
    print("Run the full suite: python -m pytest tests/test_top50_agents.py")


if __name__ == "__main__":
    main()
