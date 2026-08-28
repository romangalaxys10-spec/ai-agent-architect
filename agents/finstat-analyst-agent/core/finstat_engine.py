"""
FinStat Analyst Agent Engine.
Analyzes financial statements: margins, growth, burn, runway months,
working-capital ratios, red flags, and a 0-100 health score.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class FinAnalysis:
    periods: List[str] = field(default_factory=list)
    ratios: List[dict] = field(default_factory=list)
    growth: dict = field(default_factory=dict)
    runway_months: float = 0.0
    red_flags: List[str] = field(default_factory=list)
    green_flags: List[str] = field(default_factory=list)
    health_score: float = 0.0
    verdict: str = ""

class FinStatAnalystEngine:
    """Numbers tell the story; ratios tell whether it's a tragedy."""

    @classmethod
    def analyze(cls, data: dict) -> FinAnalysis:
        periods = [str(p) for p in data.get("periods", [])]
        items = data.get("items", {})
        n = len(periods)

        def series(name):
            vals = items.get(name, [])
            out = []
            for v in vals[:n]:
                try:
                    out.append(float(v))
                except (TypeError, ValueError):
                    out.append(None)
            return out

        rev = series("revenue")
        cogs = series("cogs")
        opex = series("opex")
        cash = series("cash")
        ar = series("receivables")
        ap = series("payables")

        if n == 0 or not any(v is not None for v in rev):
            return FinAnalysis(red_flags=["No revenue series provided — cannot analyze."],
                               verdict="NO_DATA")

        rows = []
        for i in range(n):
            r = rev[i] if i < len(rev) else None
            c = cogs[i] if i < len(cogs) else None
            o = opex[i] if i < len(opex) else None
            ch = cash[i] if i < len(cash) else None
            a = ar[i] if i < len(ar) else None
            row = {"period": periods[i]}
            if r:
                row["revenue"] = r
                if c is not None:
                    row["gross_margin"] = round((r - c) / r * 100, 1)
                if o is not None:
                    row["opex_ratio"] = round(o / r * 100, 1)
                    row["op_margin"] = round((r - (c or 0) - o) / r * 100, 1)
                if a is not None and r > 0:
                    # rough DSO: AR / revenue * days in period (assume quarter=91d if 4 periods/yr else 365/12)
                    days = 91 if n > 2 else 30
                    row["dso_days"] = round(a / r * days, 0)
            if ch is not None:
                row["cash"] = ch
            rows.append(row)

        growth = {}
        if n >= 2 and rev[0] and rev[-1]:
            total_growth = (rev[-1] / rev[0] - 1) * 100 if rev[0] != 0 else 0
            growth["total_growth_pct"] = round(total_growth, 1)
            if n >= 3:
                import math
                years = max(0.5, (n - 1) * (1.0 if n <= 5 else 0.25))
                cagr = ((rev[-1] / rev[0]) ** (1 / years) - 1) * 100 if rev[0] > 0 else 0
                growth["cagr_pct"] = round(cagr, 1)
            latest = [v for v in rev if v][-1]
            prior = [v for v in rev if v][-2]
            growth["latest_qoq_pct"] = round((latest / prior - 1) * 100, 1) if prior else None

        # burn & runway
        runway = 0.0
        if cash and cash[-1] is not None and rev and rev[-1]:
            net_burn = ((rev[-1] or 0) - (cogs[-1] or 0) - (opex[-1] or 0))
            period_len = 12 / max(1, n) if n <= 12 else 1
            monthly_burn = -net_burn / period_len if net_burn < 0 else 0
            if monthly_burn > 0:
                runway = round(cash[-1] / monthly_burn, 1)
            else:
                runway = float("inf")

        red, green = [], []
        last = rows[-1]
        if "gross_margin" in last and last["gross_margin"] < 20:
            red.append(f"Gross margin {last['gross_margin']}% — thin; pricing or COGS problem.")
        elif "gross_margin" in last and last["gross_margin"] >= 60:
            green.append(f"Software-grade gross margin ({last['gross_margin']}%).")
        if "op_margin" in last and last["op_margin"] < -25:
            red.append(f"Operating margin {last['op_margin']}% — burning over a quarter of revenue.")
        elif "op_margin" in last and last["op_margin"] > 10:
            green.append(f"Profitable at the operating line ({last['op_margin']}%).")
        if n >= 2:
            prev = rows[-2]
            if "gross_margin" in last and "gross_margin" in prev and last["gross_margin"] < prev["gross_margin"] - 5:
                red.append(f"Gross margin eroding: {prev['gross_margin']}% -> {last['gross_margin']}%.")
            if rev[-1] and rev[-2] and rev[-1] < rev[-2]:
                red.append(f"Revenue declined {periods[-2]} -> {periods[-1]}.")
        if ar and rev and n >= 2:
            if ar[-1] and rev[-1] and ar[-2] and rev[-2]:
                ar_growth = ar[-1] / max(ar[-2], 1)
                rev_growth = rev[-1] / max(rev[-2], 1)
                if ar_growth > rev_growth * 1.2 and ar_growth > 1.1:
                    red.append("Receivables growing faster than revenue — collections problem or channel stuffing.")
                elif ar[-1] / max(rev[-1], 1) > 0.4:
                    red.append(f"AR is {ar[-1]/max(rev[-1],1):.0%} of revenue — cash conversion is slow.")
            if "dso_days" in last and last["dso_days"] > 75:
                red.append(f"DSO {last['dso_days']:.0f} days — money is stuck outside the company.")
        if cash and cash[-1] is not None:
            if runway == float("inf"):
                green.append("Cash-flow positive — no runway constraint.")
            elif runway < 12:
                red.append(f"RUNWAY {runway} months — below the 12-month safety line; raise or cut NOW.")
            elif runway < 18:
                red.append(f"Runway {runway} months — start the next raise within 2 quarters.")
            else:
                green.append(f"Runway {runway} months — comfortable buffer.")
        if growth.get("cagr_pct") is not None and growth["cagr_pct"] >= 40:
            green.append(f"Revenue compounding at {growth['cagr_pct']}%/yr.")

        score = 50.0
        score += 8 * len(green)
        score -= 10 * len(red)
        score = max(3.0, min(97.0, score))

        verdict = (f"{' | '.join(periods[:4])} | health {score:.0f}/100 | "
                   f"{'runway ' + str(runway) + 'mo' if runway != float('inf') else 'cash-flow positive'} | "
                   f"{len(red)} red flag(s)")
        return FinAnalysis(periods, rows, growth, runway, red, green, score, verdict)

    @staticmethod
    def format_analysis(a: FinAnalysis) -> str:
        out = ["=" * 62, "FINSTAT ANALYST AGENT — ANALYSIS", "=" * 62, a.verdict, "-" * 62,
               "Ratio table:"]
        keys = ["revenue", "gross_margin", "opex_ratio", "op_margin", "dso_days", "cash"]
        hdr = f"  {'period':10}" + "".join(f"{k[:11]:>12}" for k in keys)
        out.append(hdr)
        for row in a.ratios:
            line = f"  {row['period'][:10]:10}"
            for k in keys:
                v = row.get(k)
                line += f"{(f'{v:,.1f}' if isinstance(v, float) else (f'{v:,.0f}' if v is not None else '-')):>12}"
            out.append(line)
        if a.growth:
            out += ["-" * 62, "Growth:"]
            out += [f"  {k}: {v}" for k, v in a.growth.items() if v is not None]
        if a.red_flags:
            out += ["-" * 62, "RED FLAGS:"] + [f"  ! {r}" for r in a.red_flags]
        if a.green_flags:
            out += ["-" * 62, "Green flags:"] + [f"  + {g}" for g in a.green_flags]
        out += ["-" * 62, f"HEALTH SCORE: {a.health_score:.0f}/100",
                "Basis: margins, growth, collections (DSO/AR), and runway — not vibes.",
                "=" * 62]
        return "\n".join(out)
