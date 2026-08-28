"""
Deterministic Multi-Currency Invoice & Financial Telemetry Engine.
Generates vector-clean HTML/PDF invoices, logs billable timesheets, and calculates multi-currency exchange balances.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import time


@dataclass
class LineItem:
    description: str
    hours: float
    rate_hourly: float
    total: float


@dataclass
class InvoiceRecord:
    invoice_number: str
    client_name: str
    client_email: str
    issue_date: str
    due_date: str
    currency: str  # USD, EUR, SOL, USDT
    items: List[LineItem]
    subtotal: float
    tax_pct: float
    total: float


class InvoiceBillingEngine:
    """Generates deterministic invoices and manages client timesheets."""

    @classmethod
    def create_invoice(
        cls,
        invoice_num: str,
        client_name: str,
        client_email: str,
        items_data: List[Dict[str, Any]],
        currency: str = "USD",
        tax_pct: float = 0.0,
    ) -> InvoiceRecord:
        line_items = []
        subtotal = 0.0
        for item in items_data:
            hrs = float(item.get("hours", 1.0))
            rate = float(item.get("rate", 150.0))
            tot = hrs * rate
            subtotal += tot
            line_items.append(LineItem(description=item.get("desc", "Engineering Hours"), hours=hrs, rate_hourly=rate, total=tot))
        
        tax = subtotal * (tax_pct / 100)
        total = subtotal + tax

        return InvoiceRecord(
            invoice_number=invoice_num,
            client_name=client_name,
            client_email=client_email,
            issue_date=time.strftime("%Y-%m-%d"),
            due_date=time.strftime("%Y-%m-%d", time.localtime(time.time() + 14 * 86400)),
            currency=currency,
            items=line_items,
            subtotal=round(subtotal, 2),
            tax_pct=tax_pct,
            total=round(total, 2),
        )

    @classmethod
    def render_invoice_html(cls, inv: InvoiceRecord) -> str:
        """Renders an Anti-Slop Swiss minimalist vector HTML invoice ready for print or PDF conversion."""
        items_rows = ""
        for it in inv.items:
            items_rows += f"""
            <tr class="border-b border-black/10">
                <td class="py-4 font-mono">{it.description}</td>
                <td class="py-4 text-center font-mono">{it.hours} hrs</td>
                <td class="py-4 text-right font-mono">{inv.currency} {it.rate_hourly:.2f}</td>
                <td class="py-4 text-right font-mono font-bold">{inv.currency} {it.total:.2f}</td>
            </tr>"""

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Invoice {inv.invoice_number} — {inv.client_name}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Syne:wght@800&family=Chivo+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Space Grotesk', sans-serif; }}
        .font-display {{ font-family: 'Syne', sans-serif; }}
        .font-mono {{ font-family: 'Chivo Mono', monospace; }}
    </style>
</head>
<body class="bg-[#F8F7F4] text-[#111213] min-h-screen p-12 print:p-0 flex items-center justify-center">
    <div class="max-w-4xl w-full bg-white border-2 border-black p-12 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] space-y-12">
        <!-- Header -->
        <div class="flex items-start justify-between border-b-2 border-black pb-8">
            <div>
                <span class="text-xs font-mono uppercase tracking-widest bg-black text-white px-2 py-0.5 font-bold">INVOICE SPECIFICATION</span>
                <h1 class="text-4xl font-black font-display uppercase tracking-tight mt-2">{inv.invoice_number}</h1>
            </div>
            <div class="text-right font-mono text-xs space-y-1">
                <div><strong>ISSUE DATE:</strong> {inv.issue_date}</div>
                <div><strong>DUE DATE:</strong> {inv.due_date}</div>
                <div><strong>STATUS:</strong> <span class="bg-[#CCFF00] px-1 font-bold">PAYMENT DUE</span></div>
            </div>
        </div>

        <!-- Parties -->
        <div class="grid grid-cols-2 gap-8 text-sm">
            <div>
                <span class="text-xs font-mono text-neutral-400 uppercase tracking-widest">// BILLED TO</span>
                <div class="text-xl font-bold font-display mt-1">{inv.client_name}</div>
                <div class="text-neutral-600 font-mono text-xs">{inv.client_email}</div>
            </div>
            <div class="text-right">
                <span class="text-xs font-mono text-neutral-400 uppercase tracking-widest">// PAYABLE TO</span>
                <div class="text-xl font-bold font-display mt-1">Autonomous Systems Labs</div>
                <div class="text-neutral-600 font-mono text-xs">architect@domain.ai</div>
            </div>
        </div>

        <!-- Table -->
        <table class="w-full text-left text-sm border-t-2 border-black">
            <thead class="border-b-2 border-black text-xs font-mono uppercase tracking-wider">
                <tr>
                    <th class="py-3">Scope / Item</th>
                    <th class="py-3 text-center">Hours</th>
                    <th class="py-3 text-right">Rate</th>
                    <th class="py-3 text-right">Total</th>
                </tr>
            </thead>
            <tbody>
                {items_rows}
            </tbody>
        </table>

        <!-- Totals -->
        <div class="flex justify-end border-t-2 border-black pt-6">
            <div class="w-72 space-y-2 font-mono text-sm">
                <div class="flex justify-between text-neutral-600">
                    <span>SUBTOTAL:</span>
                    <span>{inv.currency} {inv.subtotal:.2f}</span>
                </div>
                <div class="flex justify-between text-neutral-600">
                    <span>TAX ({inv.tax_pct}%):</span>
                    <span>{inv.currency} {inv.total - inv.subtotal:.2f}</span>
                </div>
                <div class="flex justify-between text-2xl font-black font-display border-t-2 border-black pt-2 text-[#FF3B00]">
                    <span>TOTAL:</span>
                    <span>{inv.currency} {inv.total:.2f}</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
