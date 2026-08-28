"""
Cloud Cost Optimizer Agent Engine.
Finds idle/oversized/zombie resources, computes waste with a
pricing table, and writes a savings plan ordered by savings-per-risk.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class CostAction:
    resource: str
    kind: str          # stop | downsize | schedule | commit | right
    waste_monthly: float
    risk: str
    action: str

@dataclass
class SavingsPlan:
    inventory_n: int
    total_monthly: float
    waste_monthly: float
    actions: List[CostAction] = field(default_factory=list)
    projected_savings: float = 0.0
    guardrails: List[str] = field(default_factory=list)
    verdict: str = ""

# indicative on-demand monthly USD per instance-size (rough, documented as heuristic)
PRICE_TABLE = {
    "nano": 4, "micro": 8, "small": 17, "medium": 35, "large": 70,
    "xlarge": 140, "2xlarge": 280, "4xlarge": 560, "8xlarge": 1120,
}

class CloudCostOptimizerEngine:
    """Every idle instance is a standing invoice for nothing."""

    @classmethod
    def optimize(cls, inventory: List[dict]) -> SavingsPlan:
        if not inventory:
            return SavingsPlan(0, 0, 0, [], 0,
                               ["Empty inventory — run the collector first."], "NO_DATA")

        actions: List[CostAction] = []
        total = 0.0
        waste = 0.0

        for r in inventory:
            rid = str(r.get("id", r.get("name", "?")))
            rtype = str(r.get("type", "vm")).lower()
            size = str(r.get("size", r.get("instance_type", "medium"))).lower()
            cpu = float(r.get("cpu_util", r.get("cpu", 0)) or 0)
            hours = float(r.get("running_hours_per_day", 24) or 24)
            env = str(r.get("env", r.get("environment", "prod"))).lower()
            monthly = float(r.get("monthly_cost", 0) or 0) or PRICE_TABLE.get(
                next((k for k in PRICE_TABLE if k in size), "medium"), 35)
            total += monthly

            # skip non-vm for rightsizing but still count cost
            if rtype in ("vm", "instance", "compute", "ec2", "vm"):
                if cpu <= 2 and hours >= 22:
                    waste += monthly
                    actions.append(CostAction(rid, "stop", monthly, "low",
                        "Utilization ~0 for weeks: STOP it (not terminate) for 14 days, then delete if nobody screams."))
                elif cpu < 10 and monthly > 20:
                    saved = round(monthly * 0.5, 2)
                    waste += saved
                    actions.append(CostAction(rid, "downsize", saved, "low-medium",
                        f"CPU {cpu:.0f}% -> downsize one tier (~50% cost cut); revisit after 7 days of metrics."))
                elif cpu < 25 and monthly > 100:
                    saved = round(monthly * 0.3, 2)
                    waste += saved
                    actions.append(CostAction(rid, "downsize", saved, "medium",
                        f"CPU {cpu:.0f}% on a big box: downsize; watch p99 latency for a week."))
                if hours >= 22 and env in ("dev", "staging", "test", "qa"):
                    saved = round(monthly * (16 / 24) * (5 / 7), 2)
                    waste += saved
                    actions.append(CostAction(rid, "schedule", saved, "low",
                        "Non-prod running 24/7: schedule on 8x5 — nights/weekends are ~65% of the week."))
            if rtype in ("volume", "disk", "ebs", "storage") and float(r.get("attached", 1)) == 0:
                waste += monthly
                actions.append(CostAction(rid, "delete", monthly, "low",
                    "Unattached volume: snapshot once, then delete. Snapshots cost 5-10% of volumes."))
            if rtype in ("ip", "elastic-ip") and float(r.get("attached", 1)) == 0:
                waste += monthly
                actions.append(CostAction(rid, "release", monthly, "none",
                    "Unattached public IP: hourly metering while idle — release it."))
            if rtype in ("db", "rds", "database") and cpu < 15 and monthly > 200:
                saved = round(monthly * 0.4, 2)
                waste += saved
                actions.append(CostAction(rid, "right", saved, "medium-high",
                    "DB oversized: snapshot, downsize in a maintenance window; verify replication lag after."))

        # commit-level advice when stable spend dominates
        stable = total - waste
        if stable > 2000:
            actions.append(CostAction("(portfolio)", "commit", round(stable * 0.28, 2), "medium",
                "Stable baseline spend > 2k/mo: 1-yr commit (SRP/RI/savings plan) typically cuts ~28% of the stable portion."))

        actions.sort(key=lambda a: -a.waste_monthly)
        projected = round(sum(a.waste_monthly for a in actions), 2)

        guardrails = [
            "Never downsize the week before a launch/peak season — calendar beats dashboards.",
            "Stateful services (DBs) get a backup + tested restore BEFORE any resize.",
            "Tag everything with owner+env first: untaggable resources are unmanageable costs.",
            "Run this audit monthly; waste regrows within 2 cycles of a big hiring push.",
        ]

        verdict = (f"{len(inventory)} resources | {total:,.0f}/mo current | {projected:,.0f}/mo waste "
                   f"({(projected/max(1,total))*100:.0f}%) | {len(actions)} actions")
        return SavingsPlan(len(inventory), round(total, 2), round(waste, 2), actions[:12],
                           projected, guardrails, verdict)

    @staticmethod
    def format_plan(p: SavingsPlan) -> str:
        out = ["=" * 62, "CLOUD COST OPTIMIZER AGENT — SAVINGS PLAN", "=" * 62, p.verdict, "-" * 62,
               f"{'resource':22}{'action':10}{'saves/mo':>10}  risk"]
        for a in p.actions:
            out.append(f"{a.resource[:22]:22}{a.kind:10}{a.waste_monthly:>10,.0f}  {a.risk}")
            out.append(f"    {a.action[:92]}")
        out += ["-" * 62,
                f"Total current: {p.total_monthly:,.0f}/mo | projected savings: {p.projected_savings:,.0f}/mo "
                f"({p.projected_savings/max(1,p.total_monthly)*100:.0f}%)"]
        out += ["Guardrails:"] + [f"  * {g}" for g in p.guardrails]
        out.append("=" * 62)
        return "\n".join(out)
