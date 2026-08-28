"""CLI for the Competitor Radar Agent — Classifies competitor moves, scores threat, and updates battlecards with responses"""
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
    parser = argparse.ArgumentParser(description='Competitor Radar Agent — event classification + battlecard deltas')
    parser.add_argument('--events', help="Competitor event lines: 'date | competitor | event' (inline)")
    parser.add_argument('--file', help='Path to an events file')
    parser.add_argument('--our-position', default='developer-first platform with superior DX', help='Our differentiators')
    args = parser.parse_args()

    from core.competitor_radar_engine import CompetitorRadarEngine
    text = _pick(args.events, args.file)
    if not text.strip():
        raise SystemExit("Provide --events or --file")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    report = CompetitorRadarEngine.analyze(lines, our_position=args.our_position)
    print(CompetitorRadarEngine.format_report(report))


if __name__ == "__main__":
    main()
