"""CLI for the Access Review Agent — Audits access grants for least-privilege violations and dormant privilege risk"""
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
    parser = argparse.ArgumentParser(description='Access Review Agent — least-privilege audit + revocation list')
    parser.add_argument('--grants', help='JSON array of access grants (inline)')
    parser.add_argument('--file', help='Path to a JSON grants file')
    args = parser.parse_args()

    from core.access_review_engine import AccessReviewEngine
    raw = _pick(args.grants, args.file)
    if not raw.strip():
        raise SystemExit("Provide --grants or --file")
    import json as _json
    try:
        grants = _json.loads(raw)
    except _json.JSONDecodeError as e:
        raise SystemExit(f"Grants JSON parse error: {e}")
    report = AccessReviewEngine.review(grants)
    print(AccessReviewEngine.format_report(report))


if __name__ == "__main__":
    main()
