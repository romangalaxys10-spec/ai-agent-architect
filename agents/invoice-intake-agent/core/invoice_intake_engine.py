"""
Invoice Intake Agent Engine.
Parses inbound invoice text, validates arithmetic, checks policy
thresholds and duplicate numbers, and recommends approve/hold/reject
with GL coding hints. (AP-side complement to invoice-billing-sentinel.)
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class LineItem:
    desc: str
    qty: float
    unit_price: float
    total: float

@dataclass
class IntakeResult:
    vendor: str
    invoice_no: str
    date: str
    due: str
    items: List[LineItem] = field(default_factory=list)
    subtotal: float = 0.0
    tax_pct: float = 0.0
    tax_amount: float = 0.0
    total: float = 0.0
    exceptions: List[str] = field(default_factory=list)
    posting_recommendation: str = ""
    gl_hints: List[str] = field(default_factory=list)
    verdict: str = ""

MONEY = r"(?:\$|USD\s?|€|£)\s?([\d,]+(?:\.\d{2})?)"

class InvoiceIntakeEngine:
    """Every invoice is guilty of arithmetic errors until proven innocent."""

    @staticmethod
    def _money(s: str) -> float:
        try:
            return float(s.replace(",", ""))
        except (ValueError, TypeError):
            return 0.0

    @classmethod
    def process(cls, invoice_text: str, history: List[str] = None) -> IntakeResult:
        history = history or []
        text = invoice_text.replace("\n", " | ")
        low = text.lower()

        vendor = "unknown"
        vm = re.search(r"(?:from|vendor|biller|supplier|issued by)[:\s]+([A-Za-z0-9 &.,'\-]{3,45})", text, re.I)
        if vm:
            vendor = vm.group(1).strip(" .,-|")
        else:
            fm = re.search(r"^([A-Z][A-Za-z0-9 &.'\-]{3,40})(?:\s+invoice|\s*:\s*invoice)", text, re.I)
            if fm:
                vendor = fm.group(1).strip()

        im = re.search(r"(?:invoice|inv)[\s#:.no]*(\w[\w\-]{2,20})", text, re.I)
        invoice_no = im.group(1) if im else "NOT-FOUND"
        dm = re.search(r"(?:date|issued)[:\s]+(\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4})", text, re.I)
        date = dm.group(1) if dm else "-"
        ddm = re.search(r"(?:due|pay by)[:\s]+(\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4}|net\s?\d{1,2})", text, re.I)
        due = ddm.group(1) if ddm else "-"

        items = []
        for m in re.finditer(rf"([^|]{{4,60}}?)\s+(\d+(?:\.\d+)?)\s*[x@]\s*{MONEY}(?:\s*=\s*{MONEY})?", text):
            desc = m.group(1).strip(" .-|")
            qty = float(m.group(2))
            unit = cls._money(m.group(3))
            total = cls._money(m.group(4)) if m.group(4) else qty * unit
            if desc and unit:
                items.append(LineItem(desc[:60], qty, unit, round(total, 2)))

        sub_m = re.search(rf"subtotal[:\s]+{MONEY}", text, re.I)
        tot_m = re.search(rf"(?:^|[| ])(?:total|grand total|amount due|balance due)[:\s]+{MONEY}", text, re.I)
        tax_m = re.search(rf"(?:tax|vat|gst)[\s:(]*([\d.]+)\s*%[:\s]+{MONEY}", text, re.I)
        taxp_m = re.search(rf"(?:tax|vat|gst)[\s:(]*([\d.]+)\s*%", text, re.I)

        computed_sub = round(sum(i.total for i in items), 2)
        subtotal = cls._money(sub_m.group(1)) if sub_m else computed_sub
        total = cls._money(tot_m.group(1)) if tot_m else subtotal
        tax_pct = float(taxp_m.group(1)) if taxp_m else 0.0
        tax_amount = cls._money(tax_m.group(2)) if tax_m else 0.0

        exceptions = []

        # arithmetic: line-sum vs subtotal
        if items and sub_m:
            if abs(computed_sub - subtotal) > 0.02:
                exceptions.append(f"Line items sum to {computed_sub:.2f} but subtotal says {subtotal:.2f} "
                                  f"(delta {subtotal - computed_sub:+.2f}).")
        elif not items:
            exceptions.append("No parseable line items — likely a summary invoice; request the detail PDF.")

        # arithmetic: tax
        if tax_pct and subtotal:
            expected_tax = round(subtotal * tax_pct / 100, 2)
            if tax_amount and abs(expected_tax - tax_amount) > 0.02:
                exceptions.append(f"Tax mismatch: {tax_pct}% of {subtotal:.2f} = {expected_tax:.2f}, "
                                  f"but invoice shows {tax_amount:.2f}.")
            elif not tax_amount:
                tax_amount = expected_tax

        # arithmetic: total
        if abs((subtotal + tax_amount) - total) > 0.02:
            exceptions.append(f"Total {total:.2f} != subtotal {subtotal:.2f} + tax {tax_amount:.2f} "
                              f"(= {subtotal + tax_amount:.2f}).")

        # duplicate
        if invoice_no in [str(h) for h in history]:
            exceptions.append(f"DUPLICATE: invoice #{invoice_no} already processed (history match).")

        # policy thresholds
        if total >= 5000:
            exceptions.append(f"Total {total:.2f} >= 5,000 PO threshold — 3-way match (PO + GR + invoice) required.")
        if invoice_no == "NOT-FOUND":
            exceptions.append("Invoice number not found — cannot dedupe or index; reject for resubmission.")
        if total == 0:
            exceptions.append("Zero/missing total — malformed document.")

        if not exceptions:
            posting = f"APPROVE for payment — post to AP subledger, schedule by {due}."
        elif any("DUPLICATE" in e or "malformed" in e for e in exceptions):
            posting = "REJECT — duplicate or malformed; notify vendor with the exception text."
        elif any("delta" in e or "mismatch" in e or "!=" in e for e in exceptions):
            posting = "HOLD — arithmetic exceptions require vendor clarification before approval."
        else:
            posting = "HOLD — policy exception (PO/match) must clear before payment."

        gl = []
        blob = low
        if re.search(r"software|saas|subscription|license", blob):
            gl.append("6100 Software subscriptions")
        if re.search(r"cloud|hosting|aws|azure|server", blob):
            gl.append("6110 Cloud infrastructure")
        if re.search(r"consult|service|professional|advisory", blob):
            gl.append("6200 Professional services")
        if re.search(r"hardware|equipment|laptop|device", blob):
            gl.append("1500 Capital equipment (check capitalization threshold)")
        if re.search(r"travel|flight|hotel|meal", blob):
            gl.append("6300 Travel & entertainment")
        if re.search(r"marketing|ads?|campaign", blob):
            gl.append("6400 Marketing")
        if not gl:
            gl.append("UNMAPPED — route to controller for coding")

        verdict = f"{vendor} #{invoice_no} | total {total:.2f} | {len(exceptions)} exception(s) | {posting.split(' — ')[0].split(' — ')[0]}"
        return IntakeResult(vendor, invoice_no, date, due, items, subtotal, tax_pct,
                            tax_amount, total, exceptions, posting, gl, verdict)

    @staticmethod
    def format_result(r: IntakeResult) -> str:
        out = ["=" * 62, "INVOICE INTAKE AGENT — RESULT", "=" * 62, r.verdict, "-" * 62,
               f"Vendor: {r.vendor} | Invoice #: {r.invoice_no} | Date: {r.date} | Due: {r.due}",
               "-" * 62, "Line items:"]
        if r.items:
            out += [f"  {i.desc[:44]:44} {i.qty:>5} x {i.unit_price:>9.2f} = {i.total:>9.2f}" for i in r.items]
        else:
            out.append("  (none parsed)")
        out += ["-" * 62,
                f"Subtotal: {r.subtotal:>10.2f}   Tax ({r.tax_pct:.1f}%): {r.tax_amount:>8.2f}   Total: {r.total:>10.2f}"]
        if r.exceptions:
            out += ["EXCEPTIONS:"] + [f"  ! {e}" for e in r.exceptions]
        else:
            out.append("EXCEPTIONS: none — clean arithmetic, no duplicates, within policy.")
        out += ["-" * 62, f"Posting recommendation: {r.posting_recommendation}",
                "GL coding hints:"] + [f"  * {g}" for g in r.gl_hints]
        out.append("=" * 62)
        return "\n".join(out)
