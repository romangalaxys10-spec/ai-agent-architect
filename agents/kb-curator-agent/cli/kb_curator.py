"""CLI for the KB Curator Agent — Audits the knowledge base for gaps, duplicates, staleness, and coverage holes"""
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
    parser = argparse.ArgumentParser(description='KB Curator Agent — knowledge base gap/duplicate/staleness audit')
    parser.add_argument('--kb', help='JSON array of articles [{id,title,body,updated}] (inline)')
    parser.add_argument('--file', help='Path to a JSON article array')
    parser.add_argument('--ticket-themes', default='', help='Comma-separated themes tickets mention')
    args = parser.parse_args()

    from core.kb_curator_engine import KBCuratorEngine
    raw = _pick(args.kb, args.file)
    if not raw.strip():
        raise SystemExit("Provide --kb or --file")
    import json as _json
    try:
        articles = _json.loads(raw)
    except _json.JSONDecodeError as e:
        raise SystemExit(f"KB JSON parse error: {e}")
    themes = [t.strip() for t in args.ticket_themes.split(",") if t.strip()]
    report = KBCuratorEngine.curate(articles, ticket_themes=themes)
    print(KBCuratorEngine.format_report(report))


if __name__ == "__main__":
    main()
