"""
Expense Auditor Agent Engine.
Audits expense reports against policy caps with fraud heuristics:
duplicate receipts, round-number stacking, just-under-cap patterns,
weekend anomalies, miscategorization signals.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class ExpenseFlag:
    idx: int
    merchant: str
    amount: float
    flags: List[str] = field(default_factory=list)
    evidence_required: str = ""

@dataclass
class AuditReport:
    total_expenses: float
    n_lines: int
    flags: List[ExpenseFlag] = field(default_factory=list)
    compliance_score: float = 0.0
    required_evidence: List[str] = field(default_factory=list)
    verdict: str = ""

CAT_KEYWORDS = {
    "meal": ["restaurant", "cafe", "coffee", "bistro", "grill", "diner", "lunch", "dinner", "doordash", "uber eats"],
    "hotel": ["hotel", "inn", "suites", "resort", "hostel", "airbnb", "lodging"],
    "travel": ["airlines", "airways", "flight", "rail", "amtrak", "uber", "lyft", "taxi", "gas", "fuel", "parking"],
    "office": ["staples", "office depot", "amazon", "supplies", "furniture"],
    "software": ["saas", "subscription", "license", "adobe", "atlassian", "github", "notion"],
    "entertainment": ["bar", "club", "theater", "cinema", "golf", "spa"],
}

WEEKENDS = {5, 6}  # Monday=0

class ExpenseAuditorEngine:
    """Trust but verify — and verify the pattern, not just the receipt."""

    @classmethod
    def audit(cls, expenses: List[dict], policy: dict = None) -> AuditReport:
        policy = policy or {}
        meal_cap = float(policy.get("meal_cap", 75))
        hotel_cap = float(policy.get("hotel_cap", 250))
        require_receipt_above = float(policy.get("require_receipt_above", 25))

        parsed = []
        for i, e in enumerate(expenses, 1):
            merchant = str(e.get("merchant", e.get("vendor", "?")))
            amount = float(e.get("amount", 0) or 0)
            cat = str(e.get("category", "")).lower()
            date = str(e.get("date", ""))
            desc = str(e.get("description", ""))
            receipt = bool(e.get("receipt", e.get("receipt_attached", True)))
            parsed.append(dict(idx=i, merchant=merchant, amount=amount, cat=cat,
                               date=date, desc=desc, receipt=receipt))

        def infer_cat(p):
            blob = (p["merchant"] + " " + p["cat"] + " " + p["desc"]).lower()
            for cat, kws in CAT_KEYWORDS.items():
                if any(k in blob for k in kws):
                    return cat
            return p["cat"] or "uncategorized"

        flags = []
        evidence = []
        totals = 0.0
        for p in parsed:
            totals += p["amount"]
            fl = []
            cat = infer_cat(p)
            # cap violations
            if cat == "meal" and p["amount"] > meal_cap:
                fl.append(f"meal {p['amount']:.2f} over cap {meal_cap:.2f}")
            if cat == "hotel" and p["amount"] > hotel_cap:
                fl.append(f"hotel {p['amount']:.2f} over nightly cap {hotel_cap:.2f}")

            # just-under-cap (within 2%)
            if cat == "meal" and meal_cap * 0.98 <= p["amount"] <= meal_cap:
                fl.append(f"suspiciously just under meal cap ({p['amount']:.2f} vs {meal_cap:.2f})")
            if cat == "hotel" and hotel_cap * 0.98 <= p["amount"] <= hotel_cap:
                fl.append(f"suspiciously just under hotel cap")

            # round-number stacking
            if p["amount"] > 0 and p["amount"] == int(p["amount"]) and p["amount"] >= 50:
                fl.append("large round-number amount (possible estimate, not actual)")

            # weekend entertainment
            dm = re.match(r"(\d{4})-(\d{2})-(\d{2})", p["date"])
            if dm:
                import datetime
                try:
                    d = datetime.date(int(dm.group(1)), int(dm.group(2)), int(dm.group(3)))
                    if d.weekday() in WEEKENDS and cat in ("meal", "entertainment"):
                        fl.append(f"weekend {cat} charge ({d.strftime('%a')}) — check business purpose")
                except ValueError:
                    fl.append(f"unparseable date '{p['date']}'")
            elif p["date"] and not re.match(r"\d{4}-\d{2}-\d{2}", p["date"]):
                fl.append(f"malformed date '{p['date']}'")

            # missing receipt
            if p["amount"] >= require_receipt_above and not p["receipt"]:
                fl.append(f"no receipt for {p['amount']:.2f} (required above {require_receipt_above:.0f})")

            # miscategorization signal
            if p["cat"] and cat != p["cat"] and p["cat"] not in ("uncategorized",):
                fl.append(f"category says '{p['cat']}' but merchant looks like '{cat}'")

            if fl:
                ev = ", ".join(fl[:3])
                flags.append(ExpenseFlag(p["idx"], p["merchant"], p["amount"], fl, ev))
                evidence.append(f"Line {p['idx']} ({p['merchant']}, {p['amount']:.2f}): provide "
                                f"receipt + business purpose; {ev}")

        # duplicate detection (same merchant + same amount)
        seen = {}
        for p in parsed:
            key = (p["merchant"].lower(), round(p["amount"], 2))
            if key in seen:
                f = ExpenseFlag(p["idx"], p["merchant"], p["amount"],
                                [f"possible duplicate of line {seen[key]} (same merchant+amount)"],
                                "confirm both charges are distinct (e.g. two nights vs double-billing)")
                flags.append(f)
                evidence.append(f"Line {p['idx']}: duplicate-pattern with line {seen[key]} — "
                                f"verify not double-billed or double-submitted.")
            else:
                seen[key] = p["idx"]

        n = max(1, len(parsed))
        clean = n - len({f.idx for f in flags})
        score = round(100 * clean / n, 1)
        verdict = (f"{len(parsed)} lines | {totals:.2f} total | {len(flags)} flagged line(s) | "
                   f"compliance {score:.0f}%")
        return AuditReport(totals, len(parsed), flags, score, evidence, verdict)

    @staticmethod
    def format_report(r: AuditReport) -> str:
        out = ["=" * 62, "EXPENSE AUDITOR AGENT — REPORT", "=" * 62, r.verdict, "-" * 62,
               f"Report total: {r.total_expenses:.2f} across {r.n_lines} lines"]
        if r.flags:
            out += ["Flagged lines:"]
            for f in r.flags[:12]:
                out.append(f"  L{f.idx:<3} {f.merchant[:24]:24} {f.amount:>9.2f}")
                out += [f"        - {x}" for x in f.flags]
        else:
            out.append("No policy violations or fraud patterns detected.")
        out += ["-" * 62, f"Compliance score: {r.compliance_score:.0f}%"]
        if r.required_evidence:
            out += ["Required evidence before reimbursement:"]
            out += [f"  * {e}" for e in r.required_evidence[:8]]
        out += ["=" * 62, "Note: heuristics point at risk; a human approves or rejects, never the pattern alone."]
        return "\n".join(out)
