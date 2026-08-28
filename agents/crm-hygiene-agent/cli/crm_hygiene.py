"""CLI for the CRM Hygiene Agent — Detects duplicates, decay, and missing-field debt in CRM records; writes the merge plan"""
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
    parser = argparse.ArgumentParser(description='CRM Hygiene Agent — duplicate detection + field-completeness audit')
    parser.add_argument('--records', help='JSON array of CRM records (inline)')
    parser.add_argument('--file', help='Path to a JSON records file')
    args = parser.parse_args()

    from core.crm_hygiene_engine import CRMHygieneEngine
    raw = _pick(args.records, args.file)
    if not raw.strip():
        raise SystemExit("Provide --records or --file")
    import json as _json
    try:
        records = _json.loads(raw)
    except _json.JSONDecodeError as e:
        raise SystemExit(f"Records JSON parse error: {e}")
    report = CRMHygieneEngine.audit(records)
    print(CRMHygieneEngine.format_report(report))


if __name__ == "__main__":
    main()
