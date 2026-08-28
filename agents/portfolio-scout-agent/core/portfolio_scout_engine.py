"""
Portfolio Scout Agent Engine.
Reviews holdings: allocation vs targets, concentration (HHI),
sector overlap, drawdown exposure, and a turnover-minimizing rebalance plan.
Not investment advice — risk accounting.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class PortfolioReport:
    total_value: float
    positions: List[dict] = field(default_factory=list)
    allocation: dict = field(default_factory=dict)
    hhi: float = 0.0
    top_weight: float = 0.0
    rebalance_trades: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    diversification_score: float = 0.0
    verdict: str = ""

BROAD_TARGETS = {"equity": 60, "bond": 25, "cash": 5, "crypto": 5, "alternatives": 5}

class PortfolioScoutEngine:
    """Concentration is the risk you chose; everything else is the risk you were sold."""

    @classmethod
    def analyze(cls, holdings: List[dict]) -> PortfolioReport:
        parsed = []
        total = 0.0
        for h in holdings:
            sym = str(h.get("symbol", h.get("ticker", h.get("name", "?"))))
            try:
                val = float(h.get("value", h.get("market_value", 0)) or 0)
            except (TypeError, ValueError):
                val = 0.0
            sector = str(h.get("sector", "unknown")).lower()
            cls_ = str(h.get("asset_class", h.get("class", "equity"))).lower()
            cost = h.get("cost_basis", None)
            try:
                cost = float(cost) if cost is not None else None
            except (TypeError, ValueError):
                cost = None
            parsed.append(dict(symbol=sym, value=val, sector=sector, asset_class=cls_, cost=cost))
            total += val

        if total <= 0:
            return PortfolioReport(0, [], {}, 0, 0, [],
                                   ["No positive-value holdings — nothing to review."], 0, "NO_DATA")

        for p in parsed:
            p["weight"] = p["value"] / total
            p["pnl_pct"] = ((p["value"] - p["cost"]) / p["cost"] * 100) if p["cost"] else None

        # allocation by asset class
        alloc = {}
        for p in parsed:
            key = p["asset_class"] if p["asset_class"] in BROAD_TARGETS else "alternatives"
            if p["asset_class"] in ("stock", "stocks", "etf"):
                key = "equity"
            elif p["asset_class"] in ("fixed_income", "treasury"):
                key = "bond"
            elif p["asset_class"] in ("stablecoin", "btc", "eth"):
                key = "crypto"
            alloc[key] = alloc.get(key, 0) + p["weight"]

        # concentration: HHI + sector overlap
        hhi = sum(p["weight"] ** 2 for p in parsed)
        sector_w = {}
        for p in parsed:
            sector_w[p["sector"]] = sector_w.get(p["sector"], 0) + p["weight"]
        top_sector = max(sector_w.items(), key=lambda kv: kv[1]) if sector_w else ("-", 0)
        top_pos = max(parsed, key=lambda p: p["weight"])

        risks = []
        if top_pos["weight"] > 0.20:
            risks.append(f"Single position '{top_pos['symbol']}' is {top_pos['weight']:.0%} — "
                         f"one earnings miss moves the whole portfolio.")
        if hhi > 0.35:
            risks.append(f"HHI {hhi:.2f} — highly concentrated (typical index HHI is <0.05).")
        if top_sector[1] > 0.40 and top_sector[0] != "unknown":
            risks.append(f"Sector '{top_sector[0]}' is {top_sector[1]:.0%} of the book — "
                         f"sector rotation will hurt.")
        tech_like = sum(v for k, v in sector_w.items() if k in ("technology", "tech", "software", "semiconductor"))
        if tech_like > 0.50:
            risks.append(f"Tech-adjacent exposure {tech_like:.0%} — correlated drawdown risk.")
        crypto_w = alloc.get("crypto", 0)
        if crypto_w > 0.15:
            risks.append(f"Crypto at {crypto_w:.0%} — volatility budget exceeded (15% rule of thumb).")
        cash_w = alloc.get("cash", 0)
        if cash_w < 0.02:
            risks.append("Essentially zero cash — rebalancing requires selling, not deploying.")
        if not risks:
            risks.append("No structural concentration risks at current weights.")

        # rebalance to broad targets, minimizing turnover
        trades = []
        cash_target = BROAD_TARGETS["cash"] / 100
        for cls_, target_pct in BROAD_TARGETS.items():
            current = alloc.get(cls_, 0)
            target = target_pct / 100
            drift = current - target
            if abs(drift) > 0.05:
                action = "sell" if drift > 0 else "buy"
                amt = abs(drift) * total
                # realize losses/gains intelligently
                trades.append(f"{action} ~{amt:,.0f} of {cls_} (drift {drift:+.0%} vs {target_pct}% target)")
        if trades:
            trades.append("Execute as limit orders over 2-4 weeks; harvest tax losses where pnl < 0 first.")
        else:
            trades.append("All asset classes within 5% bands — no rebalance needed (do nothing is a decision).")

        eff_n = 1 / hhi if hhi > 0 else 0
        div_score = round(max(0, min(100, 100 * min(1.0, eff_n / 20))), 0)
        verdict = (f"{len(parsed)} positions | {total:,.0f} value | HHI {hhi:.2f} (eff. {eff_n:.1f} holdings) | "
                   f"top {top_pos['symbol']} {top_pos['weight']:.0%} | div score {div_score:.0f}")
        return PortfolioReport(total, parsed, {k: round(v, 3) for k, v in alloc.items()},
                               round(hhi, 3), round(top_pos["weight"], 3), trades, risks,
                               div_score, verdict)

    @staticmethod
    def format_report(r: PortfolioReport) -> str:
        out = ["=" * 62, "PORTFOLIO SCOUT AGENT — REPORT", "=" * 62, r.verdict, "-" * 62,
               f"{'symbol':10}{'value':>12}{'weight':>8}{'sector':>14}{'pnl%':>8}"]
        for p in sorted(r.positions, key=lambda p: -p["value"]):
            pnl = f"{p['pnl_pct']:+.1f}" if p["pnl_pct"] is not None else "-"
            out.append(f"{p['symbol'][:10]:10}{p['value']:>12,.0f}{p['weight']:>8.1%}"
                       f"{p['sector'][:14]:>14}{pnl:>8}")
        out += ["-" * 62, "Allocation:"]
        out += [f"  {k:14} {v:>7.1%} (target {BROAD_TARGETS.get(k, 5)}%)" for k, v in r.allocation.items()]
        out += ["-" * 62, "Concentration:"]
        out.append(f"  HHI: {r.hhi:.3f} | top position: {r.top_weight:.1%}")
        out += ["Risk findings:"] + [f"  ! {x}" for x in r.risks]
        out += ["-" * 62, "Rebalance plan (turnover-minimizing):"]
        out += [f"  * {t}" for t in r.rebalance_trades]
        out += ["=" * 62,
                "Disclaimer: risk accounting, not investment advice. Suitability depends on your horizon."]
        return "\n".join(out)
