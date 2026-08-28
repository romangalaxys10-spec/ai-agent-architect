"""CLI for the Deep Research Agent — Cross-examines sources: corroboration matrix, contradiction detection, confidence bands"""
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
    parser = argparse.ArgumentParser(description='Deep Research Agent — source synthesis with corroboration matrix')
    parser.add_argument('--question', required=True, help='Research question')
    parser.add_argument('--sources', help="Sources as blocks separated by lines of '---' (inline)")
    parser.add_argument('--file', help='Path to sources file (blocks separated by ---)')
    args = parser.parse_args()

    from core.deep_research_engine import DeepResearchEngine
    text = _pick(args.sources, args.file)
    blocks = [b.strip() for b in text.split("\n---\n") if b.strip()] if text.strip() else []
    synth = DeepResearchEngine.synthesize(args.question, blocks)
    print(DeepResearchEngine.format_synthesis(synth))


if __name__ == "__main__":
    main()
