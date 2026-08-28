"""CLI for the Literature Review Agent — Clusters papers by method and finding, maps contradictions, and finds research gaps"""
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
    parser = argparse.ArgumentParser(description='Literature Review Agent — paper clustering + gap identification')
    parser.add_argument('--abstracts', help="Paper blocks separated by lines of '---' (inline)")
    parser.add_argument('--file', help='Path to abstracts file (blocks separated by ---)')
    args = parser.parse_args()

    from core.literature_review_engine import LiteratureReviewEngine
    text = _pick(args.abstracts, args.file)
    if not text.strip():
        raise SystemExit("Provide --abstracts or --file")
    blocks = [b.strip() for b in text.split("\n---\n") if b.strip()]
    review = LiteratureReviewEngine.review(blocks)
    print(LiteratureReviewEngine.format_review(review))


if __name__ == "__main__":
    main()
