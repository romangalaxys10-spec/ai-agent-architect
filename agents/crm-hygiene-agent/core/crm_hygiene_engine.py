"""
CRM Hygiene Agent Engine.
Detects duplicates, decay, and missing-field debt in CRM records;
emits a forecast-impact-ordered cleanup plan.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class HygieneReport:
    total: int
    completeness_pct: float
    duplicates: List[dict] = field(default_factory=list)
    invalid_contacts: List[str] = field(default_factory=list)
    stale: List[str] = field(default_factory=list)
    missing_fields: List[str] = field(default_factory=list)
    cleanup_plan: List[str] = field(default_factory=list)
    forecast_impact: str = ""
    verdict: str = ""

EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.]{2,}$")
PHONE_RE = re.compile(r"^\+?[\d\s().-]{7,}$")

def _norm_name(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(s).lower())

def _jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a | b else 0.0


class CRMHygieneEngine:
    """Forecast accuracy is downstream of record hygiene — clean the well, not the water."""

    @classmethod
    def audit(cls, records: List[dict]) -> HygieneReport:
        if not records:
            return HygieneReport(0, 0.0, [], [], [], ["No records provided."], "No data — nothing to audit.", "NO_DATA")

        TRACKED = ["name", "email", "company", "stage", "value", "owner", "last_touch"]
        field_hits = {f: 0 for f in TRACKED}
        invalid, stale = [], []
        now_proxy = 200  # we can't know 'today'; use provided last_touch recency if numeric

        for r in records:
            for f in TRACKED:
                if r.get(f) not in (None, "", "unknown"):
                    field_hits[f] += 1
            email = str(r.get("email", ""))
            if email and not EMAIL_RE.match(email):
                invalid.append(f"{r.get('name', '?')}: malformed email '{email[:30]}'")
            lt = r.get("last_touch", None)
            try:
                days = float(lt) if lt is not None else None
                if days is not None and days > 90:
                    stale.append(f"{r.get('name', '?')}: last touch {days:.0f} days ago")
            except (TypeError, ValueError):
                pass
            if r.get("value") in (None, "", 0, "0"):
                field_hits["value"] -= 0  # counted as missing already

        completeness = round(100 * sum(field_hits.values()) / (len(records) * len(TRACKED)), 1)

        # duplicate detection: same normalized name OR same email OR high name+company jaccard
        dups = []
        seen_emails = {}
        for i, r in enumerate(records):
            em = str(r.get("email", "")).lower().strip()
            if em:
                if em in seen_emails:
                    dups.append({"a": seen_emails[em], "b": r.get("name", f"rec{i}"),
                                 "key": f"email:{em}", "merge_key": "email"})
                else:
                    seen_emails[em] = r.get("name", f"rec{i}")
        for i in range(len(records)):
            for j in range(i + 1, len(records)):
                ni, nj = _norm_name(records[i].get("name", "")), _norm_name(records[j].get("name", ""))
                if not ni or not nj or ni == nj:
                    continue
                sim = _jaccard(set(ni), set(nj))
                ci, cj = _norm_name(records[i].get("company", "")), _norm_name(records[j].get("company", ""))
                if sim >= 0.8 and (ci == cj or not ci or not cj):
                    dups.append({"a": records[i].get("name", f"rec{i}"), "b": records[j].get("name", f"rec{j}"),
                                 "key": f"name-similarity {sim:.2f}", "merge_key": "name"})

        missing = [f for f, hits in field_hits.items()
                   if hits < len(records) * 0.7]
        missing_pct = {f: f"{100 - round(100 * hits / len(records), 0):.0f}% missing" for f, hits in field_hits.items()
                       if hits < len(records) * 0.7}

        plan = []
        if dups:
            plan.append(f"Merge {len(dups)} duplicate pair(s) — run BEFORE any forecast; dupes double-count pipeline.")
        if "stage" in missing:
            plan.append("Backfill stage for records missing it — forecast buckets are undefined until then.")
        if "value" in missing:
            plan.append("Backfill deal value (use median of same stage if unknown) — a blank value silently zeroes.")
        if "owner" in missing:
            plan.append("Assign owners to orphaned records; unowned deals are where deals go to die.")
        if invalid:
            plan.append(f"Fix {len(invalid)} malformed email(s) — sequences bounce and pollute sender reputation.")
        if stale:
            plan.append(f"Re-engage or archive {len(stale)} stale record(s) (>90d no touch).")
        if not plan:
            plan.append("Hygiene pass clean — move to enrichment (ICP fit scores, technographics).")

        health = 100 - 8 * len(dups) - 4 * len(missing) - 2 * len(invalid) - 1 * len(stale)
        impact = (f"{len(dups)} dup pairs + {len(missing)} weak fields: "
                  f"forecast error band roughly +/-{min(35, 4 * len(dups) + 3 * len(missing))}%")
        verdict = f"HYGIENE {max(5, health)}/100 | completeness {completeness:.0f}%"
        return HygieneReport(len(records), completeness, dups, invalid, stale, missing_pct, plan, impact, verdict)

    @staticmethod
    def format_report(r: HygieneReport) -> str:
        out = ["=" * 62, "CRM HYGIENE AGENT — REPORT", "=" * 62, r.verdict,
               f"Forecast impact: {r.forecast_impact}", "-" * 62]
        if r.duplicates:
            out += ["Duplicate pairs:"]
            out += [f"  {d['a']} <-> {d['b']} ({d['key']})" for d in r.duplicates[:8]]
        if r.missing_fields:
            out += ["Field debt: " + ", ".join(f"{k} {v}" for k, v in r.missing_fields.items())]
        if r.invalid_contacts:
            out += ["Invalid contacts:"] + [f"  ! {i}" for i in r.invalid_contacts[:5]]
        if r.stale:
            out += ["Stale records:"] + [f"  ~ {s}" for s in r.stale[:5]]
        out += ["-" * 62, "Cleanup plan (forecast-impact order):"]
        out += [f"  {i}. {p}" for i, p in enumerate(r.cleanup_plan, 1)]
        out.append("=" * 62)
        return "\n".join(out)
