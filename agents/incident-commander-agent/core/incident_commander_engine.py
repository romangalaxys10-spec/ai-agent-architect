"""
Incident Commander Agent Engine.
Classifies severity SEV1-4 from signals, activates the response runbook
with role assignments, drafts comms, and scaffolds the postmortem.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class IncidentPlan:
    severity: str
    impact: dict = field(default_factory=dict)
    roles: List[dict] = field(default_factory=list)
    runbook: List[str] = field(default_factory=list)
    comms_templates: List[str] = field(default_factory=list)
    timeline: List[str] = field(default_factory=list)
    postmortem_skeleton: List[str] = field(default_factory=list)
    blunders: List[str] = field(default_factory=list)
    verdict: str = ""

SEV_CRITERIA = [
    ("SEV1", 100, "all customers down OR data loss OR security breach OR SLA-0 violation"),
    ("SEV2", 60, "major feature broken for many customers, no workaround"),
    ("SEV3", 25, "partial degradation with workaround; single-tenant issues"),
    ("SEV4", 5, "cosmetic/minor; internal tooling; no customer-visible impact"),
]

class IncidentCommanderEngine:
    """In an incident, the commander's job is to lower variance, not to be the smartest debugger."""

    @classmethod
    def command(cls, signals_text: str) -> IncidentPlan:
        low = signals_text.lower()
        now = "T+0"

        # impact extraction
        pct_m = re.search(r"(\d{1,3})\s?%?\s*(?:of\s+)?(?:users?|customers?|traffic|requests?)", low)
        users_pct = int(pct_m.group(1)) if pct_m else (100 if re.search(r"\ball\b|\beveryone\b|\bentire\b", low) else 0)
        data_loss = bool(re.search(r"data (?:loss|lost|corrupt|deleted)|deleted production|dropped table", low))
        security = bool(re.search(r"breach|leak|unauthorized|exfiltrat|ransom|credential", low))
        outage = bool(re.search(r"down|outage|unavailable|5xx|error rate|blackhole", low))
        latency = bool(re.search(r"latency|slow|timeout|p99|degrad", low))
        single_tenant = bool(re.search(r"single (?:customer|tenant)|one customer|specific customer", low))

        # severity
        sev = "SEV4"
        if data_loss or security:
            sev = "SEV1"
        elif outage and (users_pct >= 60 or users_pct == 0 and re.search(r"\ball\b", low)):
            sev = "SEV1" if users_pct >= 60 else "SEV2"
        elif outage:
            sev = "SEV2"
        elif latency:
            sev = "SEV3"
        if single_tenant and sev == "SEV2":
            sev = "SEV3"
        threshold = next(desc for s, _p, desc in SEV_CRITERIA if s == sev)

        impact = {
            "estimated_users_affected_pct": users_pct or ("all" if sev == "SEV1" else "unknown"),
            "data_loss_suspected": data_loss,
            "security_component": security,
            "outage": outage, "degradation": latency,
            "severity_rule": f"{sev}: {threshold}",
        }

        roles = [
            {"role": "Incident Commander", "does": "runs the call, tracks timeline, decides; does NOT touch keyboards",
             "staffing": "on-call IC rotation"},
            {"role": "Ops Lead", "does": "execs mitigations on infra; proposes, IC approves",
             "staffing": "service owner"},
        ]
        if sev in ("SEV1", "SEV2"):
            roles += [
                {"role": "Comms Lead", "does": "status page + stakeholder updates every 30 min, no exceptions",
                 "staffing": "support/PM"},
                {"role": "Scribe", "does": "timestamps every action/decision in the incident channel",
                 "staffing": "anyone not debugging"},
            ]
        if security:
            roles.insert(1, {"role": "Security Lead", "does": "evidence preservation, scope of compromise, legal liaison",
                             "staffing": "security on-call"})
            roles.append({"role": "Exec Sponsor", "does": "customer-facing decisions, regulator/legal triggers",
                          "staffing": "VP+ paged automatically for SEV1"})

        runbook = [
            f"{now}: Declare {sev}. Open the incident channel + bridge. Name the IC out loud — 'I am the IC.'",
            "T+2min: Capture symptoms verbatim from alerts; assign scribe before any mitigation.",
            "T+5min: First mitigation bias — RESTART/FAILOVER is usually safer than a novel fix mid-incident.",
            "T+10min: Blast-radius question: 'what did we change in the last 24h?' (deploys, config, DNS, quotas, certs).",
            "T+15min: If unknown cause: bisect by disabling newest features via flags, not by deploying new code.",
        ]
        if data_loss:
            runbook.insert(2, "T+3min: FREEZE writes on affected stores; snapshot everything before recovery attempts.")
        if security:
            runbook.insert(2, "T+3min: Preserve logs + memory dumps; do NOT remediate-and-destroy-evidence.")

        comms = [
            f"STATUS PAGE ({sev}): 'We are investigating elevated error rates affecting {impact['estimated_users_affected_pct']} "
            "of users. Next update in 30 minutes.' (Timestamped, no blame, no ETA you can't defend.)",
            "STAKEHOLDER (internal, 15-min cadence for SEV1): impact, current hypothesis, mitigation in flight, next update time.",
            "RESOLUTION: 'Service is restored. We will publish a full postmortem within 72 hours. Thank you for your patience.'",
        ]

        timeline = [
            "Every entry: [HH:MM] ACTION or DECISION + owner. No narrative prose in the timeline.",
            "Mitigations get their own entries: 'applied config X @ 14:22 by ops-lead' — enables later causality mapping.",
            "Customer-visible impact start/end times are recorded SEPARATELY from mitigation times.",
        ]

        pm = [
            "## Summary (2 sentences, no jargon)",
            "## Impact (duration, users, revenue-at-risk, data)",
            "## Timeline (the scribe's log, cleaned)",
            "## Root cause (the WHY behind the why — 5-whys until a process, not a person, is fixable)",
            "## What went well / What went poorly",
            "## Action items (each: owner + date + 'how do we verify it's done')",
            "## Lessons (what would have caught this earlier)",
        ]

        blunders = [
            "Debugging on the bridge: IC types = nobody commands. Swap roles explicitly.",
            "'It's fixed' before monitoring says so for 15 minutes: flapping relapse is a classic.",
            "Skipping updates because 'nothing new': silence reads as chaos. 'No change' IS the update.",
            "Root cause = 'human error': a person made an error the SYSTEM allowed; fix the system.",
        ]

        verdict = f"{sev} declared | users~{impact['estimated_users_affected_pct']}% | " \
                  f"{'data-loss ' if data_loss else ''}{'security ' if security else ''}{len(roles)} roles assigned"
        return IncidentPlan(sev, impact, roles, runbook, comms, timeline, pm, blunders, verdict)

    @staticmethod
    def format_plan(p: IncidentPlan) -> str:
        out = ["=" * 62, "INCIDENT COMMANDER AGENT — PLAN", "=" * 62, p.verdict, "-" * 62,
               f"Severity rule: {p.impact.get('severity_rule', '')}"]
        out += [f"  {k}: {v}" for k, v in p.impact.items() if k != "severity_rule"]
        out += ["-" * 62, "Roles:"]
        for r in p.roles:
            out.append(f"  {r['role']:18} {r['does']}")
            out.append(f"  {'':18} staffing: {r['staffing']}")
        out += ["-" * 62, "Runbook (time-ordered):"]
        out += [f"  {r}" for r in p.runbook]
        out += ["-" * 62, "Comms drafts:"]
        out += [f"  * {c}" for c in p.comms_templates]
        out += ["-" * 62, "Timeline discipline:"]
        out += [f"  - {t}" for t in p.timeline]
        out += ["-" * 62, "Postmortem skeleton (due within 72h):"]
        out += [f"  {s}" for s in p.postmortem_skeleton]
        out += ["-" * 62, "Classic blunders to avoid:"]
        out += [f"  ! {b}" for b in p.blunders]
        out.append("=" * 62)
        return "\n".join(out)
