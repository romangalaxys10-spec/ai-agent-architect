"""CLI for the Email Triage Agent — Sorts an inbox into urgency quadrants, extracts asks/deadlines, drafts replies"""
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
    parser = argparse.ArgumentParser(description='Email Triage Agent — urgency quadrants + action extraction + reply drafts')
    parser.add_argument('--emails', help='JSON array of emails {from, subject, body} (inline)')
    parser.add_argument('--file', help='Path to a JSON emails file')
    args = parser.parse_args()

    from core.email_triage_engine import EmailTriageEngine
    raw = _pick(args.emails, args.file)
    if not raw.strip():
        raise SystemExit("Provide --emails or --file")
    import json as _json
    try:
        emails = _json.loads(raw)
    except _json.JSONDecodeError as e:
        raise SystemExit(f"Emails JSON parse error: {e}")
    plan = EmailTriageEngine.triage(emails)
    print(EmailTriageEngine.format_plan(plan))


if __name__ == "__main__":
    main()
