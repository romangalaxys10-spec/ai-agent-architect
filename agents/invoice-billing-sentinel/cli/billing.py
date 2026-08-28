"""CLI for Invoice Billing Sentinel (end-to-end hardened: runs from any cwd)."""
import os
import sys
import importlib.util

_AGENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_REPO_ROOT = os.path.abspath(os.path.join(_AGENT_DIR, ".."))
for _p in (_REPO_ROOT, _AGENT_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def _load(name: str, relpath: str):
    """Load engine module by explicit file path (hyphenated dirs are not importable)."""
    path = os.path.join(_AGENT_DIR, relpath)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_engine_mod = _load("core.billing_engine", "core/billing_engine.py")
InvoiceBillingEngine = _engine_mod.InvoiceBillingEngine

import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="Invoice Billing Sentinel CLI")
    sub = parser.add_subparsers(dest="command")

    p_gen = sub.add_parser("create", help="Create deterministic invoice HTML")
    p_gen.add_argument("--client", default="Superteam Global", help="Client name")
    p_gen.add_argument("--email", default="finance@superteam.fun", help="Client email")
    p_gen.add_argument("--hours", type=float, default=25.0, help="Billable hours")
    p_gen.add_argument("--rate", type=float, default=160.0, help="Hourly rate")
    p_gen.add_argument("--currency", default="USD", choices=["USD", "EUR", "SOL", "USDT"], help="Currency")
    p_gen.add_argument("--out", default="./output/invoice_latest.html", help="Output file path")

    args = parser.parse_args()

    if args.command == "create":
        inv = InvoiceBillingEngine.create_invoice(
            invoice_num=f"INV-2026-{int(args.hours * 10)}",
            client_name=args.client,
            client_email=args.email,
            items_data=[
                {"desc": "Autonomous Agent Architecture & Streaming Pipeline", "hours": args.hours, "rate": args.rate}
            ],
            currency=args.currency
        )
        html = InvoiceBillingEngine.render_invoice_html(inv)
        os.makedirs(os.path.dirname(args.out), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"🧾 Invoice generated for {args.client}: Total = {args.currency} {inv.total:.2f}")
        print(f"✅ Saved to: {args.out}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
