"""CLI for the Voice of Customer Agent — Mines feedback corpora into quantified themes, sentiment, and prioritized pain points"""
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
    parser = argparse.ArgumentParser(description='Voice of Customer Agent — theme clustering + sentiment + fix ranking')
    parser.add_argument('--feedback', help='One feedback item per line (inline)')
    parser.add_argument('--file', help='Path to a newline-delimited feedback file')
    args = parser.parse_args()

    from core.voice_of_customer_engine import VoiceOfCustomerEngine
    text = _pick(args.feedback, args.file)
    if not text.strip():
        raise SystemExit("Provide --feedback or --file")
    items = [ln.strip() for ln in text.splitlines() if ln.strip()]
    report = VoiceOfCustomerEngine.analyze(items)
    print(VoiceOfCustomerEngine.format_report(report))


if __name__ == "__main__":
    main()
