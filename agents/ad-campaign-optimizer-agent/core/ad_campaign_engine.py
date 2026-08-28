"""
Ad Campaign Optimizer Agent Engine.
Computes CTR/CPC/CPA/ROAS per campaign, classifies performance,
reallocates budget, and designs one experiment per loser.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class CampaignRow:
    name: str
    spend: float
    impressions: int
    clicks: int
    conversions: float
    revenue: float
    ctr: float
    cpc: float
    cpa: float
    roas: float
    verdict: str
    wasted_spend: float

@dataclass
class OptimizationPlan:
    rows: List[CampaignRow] = field(default_factory=list)
    totals: dict = field(default_factory=dict)
    reallocation: List[str] = field(default_factory=list)
    experiments: List[str] = field(default_factory=list)
    projected_lift: float = 0.0
    verdict: str = ""

class AdCampaignOptimizerEngine:
    """Spend follows marginal ROAS, not last month's habit."""

    @classmethod
    def optimize(cls, campaigns: List[dict], breakeven_roas: float = 2.0) -> OptimizationPlan:
        rows: List[CampaignRow] = []
        tot_spend = tot_rev = tot_conv = tot_clicks = 0.0
        for c in campaigns:
            name = str(c.get("name", c.get("campaign", "unnamed")))
            spend = float(c.get("spend", 0) or 0)
            imps = int(c.get("impressions", 0) or 0)
            clicks = float(c.get("clicks", 0) or 0)
            conv = float(c.get("conversions", 0) or 0)
            rev = float(c.get("revenue", 0) or 0)

            ctr = round(100 * clicks / imps, 2) if imps else 0.0
            cpc = round(spend / clicks, 2) if clicks else 0.0
            cpa = round(spend / conv, 2) if conv else float("inf")
            roas = round(rev / spend, 2) if spend else 0.0

            if spend == 0:
                verdict = "NO_DATA"
            elif roas >= breakeven_roas * 1.5:
                verdict = "SCALE"
            elif roas >= breakeven_roas:
                verdict = "HOLD"
            elif roas >= breakeven_roas * 0.6:
                verdict = "FIX"
            else:
                verdict = "PAUSE"

            wasted = round(spend * max(0.0, 1 - roas / breakeven_roas), 2) if spend else 0.0
            rows.append(CampaignRow(name, spend, imps, clicks, conv, rev, ctr, cpc,
                                    cpa if cpa != float("inf") else -1, roas, verdict, wasted))
            tot_spend += spend; tot_rev += rev; tot_conv += conv; tot_clicks += clicks

        rows.sort(key=lambda r: -r.roas)
        winners = [r for r in rows if r.verdict in ("SCALE",)]
        losers = [r for r in rows if r.verdict in ("FIX", "PAUSE")]
        total_wasted = round(sum(r.wasted_spend for r in rows), 2)

        realloc = []
        if winners and losers:
            pool = sum(r.spend for r in losers) * 0.5
            top = winners[0]
            realloc.append(f"Move ~{pool:.0f} (half of loser budgets) into '{top.name}' (ROAS {top.roas}), "
                           f"staged +20%/48h to avoid resetting learning phase.")
            if len(winners) > 1:
                realloc.append(f"Cap '{winners[0].name}' if CPA rises >25% after scaling; overflow to '{winners[1].name}'.")
        elif not winners and rows:
            realloc.append("No campaign clears breakeven — freeze budget; fix offers/landing pages first.")
        for r in rows:
            if r.verdict == "PAUSE":
                realloc.append(f"PAUSE '{r.name}' now: ROAS {r.roas} vs breakeven {breakeven_roas} (wasting {r.wasted_spend:.0f}).")
        if not realloc:
            realloc.append("All campaigns between HOLD and SCALE — no reallocation needed this cycle.")

        experiments = []
        exp_bank = {
            "FIX": "Test 3 new headlines against the current one (same audience, 7 days, >=1,000 impressions/arm).",
            "PAUSE": "Before killing: one last test with a narrowed audience (top-converting geo/age only).",
            "HOLD": "Test raising CPM-bid floor 10% to filter junk placements; watch CPA for 5 days.",
            "SCALE": "Test a lookalike audience seeded from converters with >2 conversions.",
        }
        for r in losers[:3] + winners[:1]:
            experiments.append(f"{r.name}: {exp_bank[r.verdict]}")

        blended_roas = round(tot_rev / tot_spend, 2) if tot_spend else 0.0
        lift = round(100 * (0.3 * total_wasted / tot_spend), 1) if tot_spend else 0.0
        verdict = f"BLENDED ROAS {blended_roas} | waste {total_wasted} | {len(winners)} scalable, {len(losers)} fix/pause"
        return OptimizationPlan(rows, {
            "spend": round(tot_spend, 2), "revenue": round(tot_rev, 2),
            "conversions": tot_conv, "clicks": tot_clicks,
            "blended_roas": blended_roas, "total_wasted": total_wasted,
        }, realloc, experiments, lift, verdict)

    @staticmethod
    def format_plan(p: OptimizationPlan) -> str:
        out = ["=" * 62, "AD CAMPAIGN OPTIMIZER AGENT — PLAN", "=" * 62, p.verdict, "-" * 62,
               f"{'campaign':20}{'spend':>8}{'CTR%':>7}{'CPC':>7}{'CPA':>8}{'ROAS':>7}  verdict"]
        for r in p.rows:
            cpa = f"{r.cpa}" if r.cpa >= 0 else "n/a"
            out.append(f"{r.name[:20]:20}{r.spend:>8.0f}{r.ctr:>7.2f}{r.cpc:>7.2f}{cpa:>8}{r.roas:>7.2f}  {r.verdict}")
        out += ["-" * 62, f"Totals: spend {p.totals.get('spend',0)} | revenue {p.totals.get('revenue',0)} | "
                          f"wasted {p.totals.get('total_wasted',0)}",
                "-" * 62, "Budget reallocation:"]
        out += [f"  {i}. {r}" for i, r in enumerate(p.reallocation, 1)]
        out += ["-" * 62, "Experiments (one per campaign, clean reads):"]
        out += [f"  * {e}" for e in p.experiments]
        out += [f"-" * 62, f"Projected blended-ROAS lift if plan executed: ~{p.projected_lift}%", "=" * 62]
        return "\n".join(out)
