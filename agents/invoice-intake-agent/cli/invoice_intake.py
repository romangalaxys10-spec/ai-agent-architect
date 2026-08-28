"""CLI for the Invoice Intake Agent — Parses inbound invoices, checks arithmetic, policy, duplicates, 3-way match"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _pick(inline, path):
    if path:
        return _read(path)
    return inline or ""


def main():
    parser = argparse.ArgumentParser(description='Invoice Intake Agent — inbound invoice parsing + validation + matching')
    parser.add_argument('--invoice', help='Invoice text (inline)')
    parser.add_argument('--file', help='Path to an invoice text file')
    parser.add_argument('--history', default='', help='JSON array of already-seen invoice numbers')
    args = parser.parse_args()

    from core.invoice_intake_engine import InvoiceIntakeEngine
    text = _pick(args.invoice, args.file)
    if not text.strip():
        raise SystemExit("Provide --invoice or --file")
    history = []
    if args.history.strip():
        import json as _json
        try:
            history = _json.loads(args.history)
        except _json.JSONDecodeError as e:
            raise SystemExit(f"History JSON parse error: {e}")
    result = InvoiceIntakeEngine.process(text, history=history)
    print(InvoiceIntakeEngine.format_result(result))


if __name__ == "__main__":
    main()
