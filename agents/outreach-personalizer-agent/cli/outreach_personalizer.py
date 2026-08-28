"""CLI for the Outreach Personalizer Agent — Writes 3-tone personalized cold emails with spam-word linting and A/B variants"""
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
    parser = argparse.ArgumentParser(description='Outreach Personalizer Agent — 3-tone personalized email variants')
    parser.add_argument('--prospect', help='Prospect facts text (inline)')
    parser.add_argument('--file', help='Path to prospect facts file')
    parser.add_argument('--offer', default='a 15-minute architecture review call', help='What you are offering')
    args = parser.parse_args()

    from core.outreach_personalizer_engine import OutreachPersonalizerEngine
    text = _pick(args.prospect, args.file)
    if not text.strip():
        raise SystemExit("Provide --prospect or --file")
    pack = OutreachPersonalizerEngine.personalize(text, offer=args.offer)
    print(OutreachPersonalizerEngine.format_pack(pack))


if __name__ == "__main__":
    main()
