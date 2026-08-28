"""
Data Analyst Agent Engine.
Profiles CSV data end-to-end: per-column stats, nulls, outliers (z-score),
correlations, duplicate columns, ranked insights, chart recommendations.
Pure stdlib — no pandas dependency.
"""

import csv
import io
import math
import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class ColumnProfile:
    name: str
    dtype: str
    nulls: int
    cardinality: int
    stats: dict = field(default_factory=dict)
    top_values: List[tuple] = field(default_factory=list)
    outliers: List[str] = field(default_factory=list)

@dataclass
class Insight:
    rank: int
    text: str
    chart: str

@dataclass
class DataAnalysis:
    n_rows: int
    n_cols: int
    columns: List[ColumnProfile] = field(default_factory=list)
    correlations: List[tuple] = field(default_factory=list)
    duplicate_columns: List[str] = field(default_factory=list)
    data_quality: List[str] = field(default_factory=list)
    insights: List[Insight] = field(default_factory=list)
    verdict: str = ""

class DataAnalystEngine:
    """Look at the data before looking for insights — profile first, conclude second."""

    @staticmethod
    def _try_float(s: str):
        try:
            v = float(str(s).replace(",", "").replace("$", "").rstrip("%"))
            return v
        except (ValueError, TypeError):
            return None

    @classmethod
    def analyze(cls, csv_text: str) -> DataAnalysis:
        rows = list(csv.reader(io.StringIO(csv_text.strip())))
        if len(rows) < 2:
            return DataAnalysis(0, 0, [], [], [], ["Not enough rows to analyze."], [],
                                "NO_DATA")
        header = [h.strip() for h in rows[0]]
        data = [r for r in rows[1:] if any(c.strip() for c in r)]
        n, m = len(data), len(header)

        cols: List[ColumnProfile] = []
        for j in range(m):
            name = header[j] if j < len(header) else f"col_{j}"
            vals = [r[j] if j < len(r) else "" for r in data]
            nulls = sum(1 for v in vals if v is None or str(v).strip() in ("", "NA", "N/A", "null", "None", "-"))
            floats = [f for f in (cls._try_float(v) for v in vals) if f is not None]
            nonnull = [str(v) for v in vals if str(v).strip() not in ("", "NA", "N/A", "null", "None", "-")]
            cardinality = len(set(nonnull))

            is_numeric = len(floats) >= max(1, int(0.8 * (n - nulls))) and floats
            stats, top_values, outliers = {}, [], []
            if is_numeric and floats:
                mean = sum(floats) / len(floats)
                var = sum((x - mean) ** 2 for x in floats) / len(floats)
                std = math.sqrt(var)
                srt = sorted(floats)
                med = srt[len(srt)//2] if len(srt) % 2 else (srt[len(srt)//2 - 1] + srt[len(srt)//2]) / 2
                stats = {"mean": round(mean, 3), "std": round(std, 3),
                         "min": srt[0], "max": srt[-1], "median": med,
                         "range": round(srt[-1] - srt[0], 3)}
                if std > 0 and len(floats) >= 8:
                    z = lambda x: abs(x - mean) / std
                    outliers = [f"row where {name}={x:g} (z={z(x):.1f})" for x in floats if z(x) > 2.5][:4]
                counts = {}
                for v in floats:
                    counts[v] = counts.get(v, 0) + 1
                top_values = [(str(k), v) for k, v in sorted(counts.items(), key=lambda kv: -kv[1])[:3]]
            else:
                counts = {}
                for v in nonnull:
                    counts[v] = counts.get(v, 0) + 1
                top_values = sorted(counts.items(), key=lambda kv: -kv[1])[:5]
            dtype = "numeric" if is_numeric else ("categorical" if cardinality <= max(12, n // 3) else "text/id")
            cols.append(ColumnProfile(name, dtype, nulls, cardinality, stats, top_values, outliers))

        # correlations between numeric columns
        num_idx = [j for j, c in enumerate(cols) if c.dtype == "numeric" and c.stats]
        correlations = []
        for a in range(len(num_idx)):
            for b in range(a + 1, len(num_idx)):
                ja, jb = num_idx[a], num_idx[b]
                xs = [cls._try_float(r[ja]) if ja < len(r) else None for r in data]
                ys = [cls._try_float(r[jb]) if jb < len(r) else None for r in data]
                pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
                if len(pairs) < 5:
                    continue
                mx = sum(p[0] for p in pairs) / len(pairs)
                my = sum(p[1] for p in pairs) / len(pairs)
                cov = sum((p[0]-mx)*(p[1]-my) for p in pairs)
                sx = math.sqrt(sum((p[0]-mx)**2 for p in pairs))
                sy = math.sqrt(sum((p[1]-my)**2 for p in pairs))
                if sx > 0 and sy > 0:
                    r = cov / (sx * sy)
                    if abs(r) >= 0.55:
                        correlations.append((cols[ja].name, cols[jb].name, round(r, 3)))

        # duplicate column detection
        dup_cols = []
        for a in range(len(cols)):
            for b in range(a + 1, len(cols)):
                va = [r[a] if a < len(r) else "" for r in data]
                vb = [r[b] if b < len(r) else "" for r in data]
                if va == vb:
                    dup_cols.append(f"'{cols[a].name}' == '{cols[b].name}' (identical values)")

        quality = []
        for c in cols:
            if c.nulls:
                pct = round(100 * c.nulls / n, 1)
                quality.append(f"'{c.name}': {c.nulls} nulls ({pct}%)"
                               + (" — impute or drop; >40% nulls means drop" if pct > 40 else ""))
            if c.dtype == "numeric" and c.stats and c.stats["std"] == 0:
                quality.append(f"'{c.name}': constant column (zero variance) — remove")
        if n < 30:
            quality.append(f"Only {n} rows — insights are directional, not statistical.")

        insights = []
        for x, y, r in correlations:
            direction = "positive" if r > 0 else "negative"
            strength = "strong" if abs(r) >= 0.8 else "moderate"
            insights.append((abs(r), f"'{x}' and '{y}' move together ({strength} {direction}, r={r:+.2f}) — "
                                      f"investigate causality before acting.",
                             "scatter plot with trend line"))
        for c in cols:
            if c.dtype == "numeric" and c.outliers:
                insights.append((0.7, f"'{c.name}' has {len(c.outliers)} outlier(s) beyond 2.5 sigma — "
                                      f"verify they are real, not data-entry errors.",
                                 "histogram or box plot"))
            if c.top_values and c.dtype == "categorical":
                tv, tc = c.top_values[0]
                share = 100 * tc / max(1, n - c.nulls)
                if share >= 50:
                    insights.append((0.6, f"'{c.name}' is dominated by '{tv}' ({share:.0f}%) — "
                                          f"check for a default-value artifact.",
                                     "bar chart of category counts"))
            if c.stats and "range" in c.stats:
                rg = c.stats["range"]
                if rg == 0:
                    continue
        for d in dup_cols:
            insights.append((0.9, f"Duplicate columns detected: {d} — drop one before modeling.", "-"))
        insights.sort(key=lambda t: -t[0])
        ranked = [Insight(i + 1, t, ch) for i, (score, t, ch) in enumerate(insights[:6])]

        verdict = (f"{n} rows x {m} cols | {len([c for c in cols if c.dtype=='numeric'])} numeric | "
                   f"{len(correlations)} notable correlations | {len(quality)} quality issues")
        return DataAnalysis(n, m, cols, correlations, dup_cols, quality, ranked, verdict)

    @staticmethod
    def format_analysis(a: DataAnalysis) -> str:
        out = ["=" * 62, "DATA ANALYST AGENT — ANALYSIS", "=" * 62, a.verdict, "-" * 62,
               f"{'column':20}{'type':12}{'nulls':>6}{'card':>6}  notes"]
        for c in a.columns:
            note = ""
            if c.dtype == "numeric" and c.stats:
                note = f"mean={c.stats['mean']} std={c.stats['std']} range=[{c.stats['min']},{c.stats['max']}]"
            elif c.top_values:
                note = "top: " + ", ".join(f"{v}({t})" for v, t in c.top_values[:3])
            out.append(f"{c.name[:20]:20}{c.dtype:12}{c.nulls:>6}{c.cardinality:>6}  {note[:70]}")
        if a.correlations:
            out += ["-" * 62, "Correlations (|r| >= 0.55):"]
            out += [f"  {x} <-> {y}: r={r:+.3f}" for x, y, r in a.correlations]
        if a.duplicate_columns:
            out += ["Duplicate columns: " + "; ".join(a.duplicate_columns)]
        if a.data_quality:
            out += ["-" * 62, "Data quality:"]
            out += [f"  ! {q}" for q in a.data_quality]
        out += ["-" * 62, "Ranked insights:"]
        if a.insights:
            for i in a.insights:
                out.append(f"  {i.rank}. {i.text}")
                if i.chart != "-":
                    out.append(f"      visualize: {i.chart}")
        else:
            out.append("  no strong patterns in this dataset")
        out.append("=" * 62)
        return "\n".join(out)
