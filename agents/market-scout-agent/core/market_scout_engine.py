"""
Market Scout Agent Engine.
Sizes TAM/SAM/SOM two ways (top-down, bottom-up), scores market
attractiveness, and calls the entry verdict with kill-risks.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class MarketSizing:
    market: str
    tam: dict
    sam: dict
    som: dict
    reconciliation: str
    attractiveness: List[tuple] = field(default_factory=list)
    attractiveness_score: float = 0.0
    kill_risks: List[str] = field(default_factory=list)
    needed_evidence: List[str] = field(default_factory=list)
    entry_verdict: str = ""
    verdict: str = ""

class MarketScoutEngine:
    """Sizing is arithmetic; entering is judgment — do both, label which is which."""

    @staticmethod
    def _num(inputs, keys, default=None):
        for k in keys:
            for ik, iv in inputs.items():
                if k in ik.lower():
                    try:
                        return float(re.sub(r"[^0-9.]", "", str(iv)))
                    except (ValueError, TypeError):
                        continue
        return default

    @classmethod
    def size(cls, market: str, inputs: dict) -> MarketSizing:
        population = cls._num(inputs, ["population", "accounts", "companies", "users", "firms"])
        price = cls._num(inputs, ["price", "arpu", "acv", "average"])
        share = cls._num(inputs, ["share", "penetration", "segment"])
        growth = cls._num(inputs, ["growth", "cagr"])
        competitors = cls._num(inputs, ["competitors", "rivals", "vendors"])
        budget_avail = cls._num(inputs, ["budget", "spend"])

        # top-down
        if population and price:
            tam_td = population * price
        elif budget_avail:
            tam_td = budget_avail
        else:
            tam_td = None

        # bottom-up: assume inputs may include segments; fallback heuristic uses 60% of top-down reach
        if population and price and share:
            sam_v = population * (share / 100 if share > 1 else share) * price
        elif tam_td:
            sam_v = tam_td * 0.3
        else:
            sam_v = None

        som_v = sam_v * 0.05 if sam_v else None

        def fmt(v):
            if v is None:
                return "n/a"
            if v >= 1e9:
                return f"${v/1e9:.1f}B"
            if v >= 1e6:
                return f"${v/1e6:.1f}M"
            return f"${v:,.0f}"

        if tam_td and sam_v:
            ratio = sam_v / tam_td
            reconciliation = (
                f"SAM is {ratio:.0%} of TAM — " +
                ("plausible for a single-segment wedge." if 0.05 <= ratio <= 0.6 else
                 "AGGRESSIVE: re-check segment filters; SAM should be 5-60% of TAM.") +
                " SOM assumes ~5% of SAM within 3 years — sane for a new entrant with no distribution moat.")
        else:
            reconciliation = ("Insufficient inputs for two-method sizing: provide (population x price) "
                              "AND budget benchmarks to triangulate. Single-method sizes mislead by 2-5x.")

        attrs = []
        if growth is not None:
            g = growth if growth < 1 else growth / 100
            attrs.append(("growth", min(25, 25 * g / 0.25), f"CAGR {g:.0%} " +
                          ("(expansion window open)" if g >= 0.15 else "(mature — fight for share)")))
        if competitors is not None:
            c = competitors
            attrs.append(("competition", max(5, 20 - c), f"{c:.0f} named competitors " +
                          ("(greenfield-ish)" if c <= 3 else "(contested)" if c <= 8 else "(red ocean)")))
        if price is not None and price > 0:
            attrs.append(("unit_economics", 20 if price >= 5000 else 12 if price >= 500 else 6,
                          f"ACV ${price:,.0f} " + ("(enterprise motion)" if price >= 5000 else "(SMB/self-serve)")))
        if budget_avail is not None and tam_td:
            attrs.append(("budget_reality", 15 if abs(budget_avail - tam_td) / max(tam_td, 1) < 0.5 else 7,
                          "top-down vs spend benchmark within 2x (trustworthy)" if abs(budget_avail - tam_td) / max(tam_td, 1) < 0.5
                          else "top-down diverges from spend benchmark >2x (inflated TAM)"))

        score = sum(a[1] for a in attrs) / (25 * len(attrs)) * 100 if attrs else 50.0

        kill_risks = []
        if tam_td is None:
            kill_risks.append("Cannot size the market from given inputs — this alone kills most pitch meetings.")
        if competitors is not None and competitors >= 10:
            kill_risks.append(f"{competitors:.0f}+ competitors: differentiation must be structural, not feature-level.")
        if price is not None and price < 100:
            kill_risks.append(f"ACV ${price:.0f} is below the threshold where sales-led motion pays back.")
        if growth is not None and (growth < 1 and growth < 0.05 or growth <= 3):
            kill_risks.append("Growth under 5% — every dollar of revenue must be taken from an incumbent.")
        if not kill_risks:
            kill_risks.append("No structural kill-risks detected from inputs (still validate buyer willingness-to-pay).")

        needed = ["10 customer discovery interviews with budget-holder confirmation",
                  "One win/loss analysis against the closest incumbent"]
        if som_v and price:
            needed.append(f"To hit SOM {fmt(som_v)}, you need ~{som_v/max(price,1):,.0f} customers — sanity-check that count against sales capacity.")

        if score >= 65 and tam_td and price and price >= 100:
            entry = "ENTER — build the wedge; time-box to a 90-day validation gate."
        elif score >= 45:
            entry = "NICHE — enter a narrow segment first; re-score after 10 customer conversations."
        else:
            entry = "PASS (for now) — fix the flagged gaps before spending build cycles."

        verdict = f"TAM {fmt(tam_td)} | SAM {fmt(sam_v)} | SOM {fmt(som_v)} | attractiveness {score:.0f}/100"
        return MarketSizing(market,
                            {"value": fmt(tam_td), "method": "top-down (population x price / spend benchmark)"},
                            {"value": fmt(sam_v), "method": "segment-filtered TAM"},
                            {"value": fmt(som_v), "method": "~5% of SAM, 3yr, no moat"},
                            reconciliation, attrs, round(score, 1), kill_risks, needed, entry, verdict)

    @staticmethod
    def format_sizing(s: MarketSizing) -> str:
        out = ["=" * 62, "MARKET SCOUT AGENT — SIZING", "=" * 62,
               f"Market: {s.market}", s.verdict, "-" * 62,
               f"TAM: {s.tam['value']:12} ({s.tam['method']})",
               f"SAM: {s.sam['value']:12} ({s.sam['method']})",
               f"SOM: {s.som['value']:12} ({s.som['method']})",
               "-" * 62, f"Reconciliation: {s.reconciliation}", "-" * 62, "Attractiveness factors:"]
        out += [f"  {name:16} {score:5.1f}  {note}" for name, score, note in s.attractiveness] or ["  (insufficient inputs)"]
        out += ["-" * 62, "Kill-risks:"]
        out += [f"  ! {k}" for k in s.kill_risks]
        out += ["-" * 62, "Evidence still needed:"]
        out += [f"  * {n}" for n in s.needed_evidence]
        out += ["-" * 62, f"ENTRY VERDICT: {s.entry_verdict}", "=" * 62]
        return "\n".join(out)
