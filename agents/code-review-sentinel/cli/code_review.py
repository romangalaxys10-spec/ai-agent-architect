"""CLI for the Code Review Sentinel — Zero-trust PR review: severity-ranked findings, CWE mapping, verdict gate"""
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
    parser = argparse.ArgumentParser(description='Code Review Sentinel — severity-ranked static review of Python source')
    parser.add_argument('--code', help='Python source code to review (inline)')
    parser.add_argument('--file', help='Path to a Python source file')
    parser.add_argument('--strict', action='store_true', help='Promote major findings to blockers')
    args = parser.parse_args()

    from core.code_review_engine import CodeReviewSentinelEngine
    code = _pick(args.code, args.file)
    if not code.strip():
        raise SystemExit("Provide --code or --file")
    report = CodeReviewSentinelEngine.review(code, strict=args.strict)
    print(CodeReviewSentinelEngine.format_report(report))


if __name__ == "__main__":
    main()
