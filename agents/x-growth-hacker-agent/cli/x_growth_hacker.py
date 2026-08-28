"""CLI for X/Twitter Growth Hacker — Viral hook engineering, thread pacing, reply-guy strategy, algorithmic timing optimization"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def main():
    parser = argparse.ArgumentParser(description='X/Twitter Growth Hacker — Viral hook engineering, thread pacing, reply-guy strategy, algorithmic timing optimization')
    parser.add_argument('--text', help='Input text to analyze (inline)')
    parser.add_argument('--file', help='Path to input file')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()

    text = ""
    if args.file:
        text = _read(args.file)
    elif args.text:
        text = args.text
    else:
        # also accept stdin pipe style via --text fallback to reading prompt
        import sys as _sys
        if not _sys.stdin.isatty():
            text = _sys.stdin.read()
        if not text or not text.strip():
            parser.error("Provide --text or --file (or pipe via stdin)")

    from core.x_growth_hacker_engine import XGrowthHackerEngine
    analysis = XGrowthHackerEngine.analyze(text)
    if args.json:
        import json as _json, dataclasses as _dc
        print(_json.dumps({_dc.asdict.__name__: _dc.asdict(analysis)}, indent=2, default=str))
        # fallback simple json
        print(_json.dumps({"verdict": analysis.verdict, "score": analysis.score, "metrics": analysis.metrics, "findings": [{"severity": f.severity, "title": f.title, "detail": f.detail, "fix": f.fix} for f in analysis.findings], "next_steps": analysis.next_steps}, indent=2))
    else:
        print(XGrowthHackerEngine.format_report(analysis))


if __name__ == "__main__":
    main()
