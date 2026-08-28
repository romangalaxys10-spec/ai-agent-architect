"""
Onboarding Guide Agent Engine.
Builds 30/60/90 onboarding plans with week-1 schedule, access
checklist with owners, buddy wiring, and outcome gates.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class OnboardingPlan:
    role: str
    team: str
    week1: List[str] = field(default_factory=list)
    access_checklist: List[str] = field(default_factory=list)
    buddy_program: List[str] = field(default_factory=list)
    gates: List[dict] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    verdict: str = ""

ROLE_TOOLS = {
    "engineer": ["repo access (read+write on main repo)", "CI/CD pipeline viewer", "incident pager (shadow)",
                 "cloud console (read-only)", "design docs folder", "staging environment"],
    "designer": ["design tool seat", "component library access", "user-research archive",
                 "brand guidelines", "prototype environment", "file handoff channel"],
    "pm": ["roadmap tool", "analytics dashboard", "customer interview archive", "spec templates",
           "staging environment", "support ticket queue (read)"],
    "data": ["warehouse read access", "query editor", "dashboard tool", "data dictionary",
             "pipeline monitoring", "alerting channel"],
    "sales": ["CRM account", "email sequences tool", "call recording + playbook", "pricing approval matrix",
              "contract templates", "demo environment"],
}

class OnboardingGuideEngine:
    """Onboarding is the first product your teammate uses. Ship it like one."""

    @classmethod
    def plan(cls, role: str, team: str = "Platform Engineering", start_date: str = "Monday") -> OnboardingPlan:
        role_low = role.lower()
        tools = next((v for k, v in ROLE_TOOLS.items() if k in role_low), ROLE_TOOLS["engineer"])

        week1 = [
            f"Day 0 (before {start_date}): laptop delivered + accounts provisioned; welcome doc emailed "
            "with first-day schedule and dress-code-free honesty.",
            f"Day 1 AM: manager 1:1 (60 min) — expectations, working style, how to ask for help; "
            "NO task assignment today. Lunch with the team (paid, calendar-invited).",
            f"Day 1 PM: environment setup with the buddy; ship one trivial change end-to-end "
            "(typo fix, description update — anything that touches prod safely). First win by day 1.",
            "Day 2: read the 3 core docs (architecture, runbook, team charter) with the buddy; "
            "write 3 questions you had to ask anyway — they become doc PRs.",
            "Day 3: shadow the team's daily rituals; take notes on what confused you — freshest-eyes audit you'll ever get.",
            "Day 4: first real task — scoped to one day, with a named reviewer committed in advance.",
            "Day 5: week-1 retro with manager: what was unclear, what docs lied, what to fix for the next hire. "
            "This meeting is non-negotiable.",
        ]

        access = [f"[ ] {t} — owner: IT or {team} lead; due Day 1" for t in tools]
        access += [
            "[ ] payroll + benefits enrollment — owner: People Ops; due Day 3",
            "[ ] security training (phishing + data handling) — owner: Security; due Week 1",
            "[ ] production access (if applicable) — owner: lead + security sign-off; due Week 2-4, AFTER training",
        ]

        buddy = [
            "Assign a buddy (peer, not manager) BEFORE day 1; buddy's job: answer 'stupid' questions for 30 days.",
            "Buddy check-ins: daily week 1, twice weekly weeks 2-4, weekly through day 60.",
            "Manager 1:1s: 2x week 1, weekly after — calendar them for the first 90 days NOW.",
            "Skip-level intro in week 2 — 20 minutes, no agenda but 'how does this place actually work'.",
        ]

        gates = [
            {"day": 30, "gate": "SHIPPED", "evidence": "Merged multiple changes incl. one non-trivial; can navigate the codebase and docs unaided.",
             "owner": "manager", "risk_if_missed": "environment or mentorship failure — fix the system, not the person."},
            {"day": 60, "gate": "OWNING", "evidence": "Owns a small area end-to-end (incl. one incident shadow or customer conversation).",
             "owner": "manager", "risk_if_missed": "scope too small or feedback unclear — re-contract explicitly."},
            {"day": 90, "gate": "INDEPENDENT", "evidence": "Delivers a scoped project solo; gives help to someone newer; passes the on-call certification if applicable.",
             "owner": "manager", "risk_if_missed": "formal performance conversation with written expectations."},
        ]

        risks = [
            "Access provisioning is the #1 onboarding failure — track it as a checklist with owners, not a hope.",
            "If the buddy is 'too busy', reassign in week 1; a silent buddy costs a quarter of productivity.",
            "First task too big = day-10 spiral. Keep day-4 task to ONE day of work.",
        ]

        verdict = f"30/60/90 plan for {role} on {team} | {len(week1)} week-1 items | {len(gates)} outcome gates"
        return OnboardingPlan(role, team, week1, access, buddy, gates, risks, verdict)

    @staticmethod
    def format_plan(p: OnboardingPlan) -> str:
        out = ["=" * 62, "ONBOARDING GUIDE AGENT — PLAN", "=" * 62,
               f"{p.role} -> {p.team}", p.verdict, "-" * 62, "Week 1 schedule:"]
        out += [f"  {w}" for w in p.week1]
        out += ["-" * 62, "Access checklist (with owners):"]
        out += [f"  {a}" for a in p.access_checklist]
        out += ["-" * 62, "Buddy & manager wiring:"]
        out += [f"  * {b}" for b in p.buddy_program]
        out += ["-" * 62, "Outcome gates (outcomes, not attendance):"]
        for g in p.gates:
            out.append(f"  Day {g['day']} — {g['gate']}: {g['evidence']}")
            out.append(f"      owner: {g['owner']} | if missed: {g['risk_if_missed']}")
        out += ["-" * 62, "Known failure modes:"]
        out += [f"  ! {r}" for r in p.risks]
        out.append("=" * 62)
        return "\n".join(out)
