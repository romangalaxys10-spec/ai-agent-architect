"""CLI for the Contract Reviewer Agent — Detects and grades clauses, flags missing terms, drafts negotiation redlines"""
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
    parser = argparse.ArgumentParser(description='Contract Reviewer Agent — clause detection + risk grading + redlines')
    parser.add_argument('--contract', help='Contract text (inline)')
    parser.add_argument('--file', help='Path to a contract text file')
    parser.add_argument('--side', default='buyer', choices=['buyer', 'seller', 'neutral'], help='Which side we represent')
    args = parser.parse_args()

    from core.contract_reviewer_engine import ContractReviewerEngine
    text = _pick(args.contract, args.file)
    if not text.strip():
        raise SystemExit("Provide --contract or --file")
    review = ContractReviewerEngine.review(text, side=args.side)
    print(ContractReviewerEngine.format_review(review))


if __name__ == "__main__":
    main()
