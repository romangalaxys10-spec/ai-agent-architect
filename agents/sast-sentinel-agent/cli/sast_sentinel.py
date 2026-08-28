"""CLI for the SAST Sentinel Agent — OWASP Top-10 aligned static security scanner with CVSS-style severity and remediation"""
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
    parser = argparse.ArgumentParser(description='SAST Sentinel Agent — OWASP-aligned static security analysis')
    parser.add_argument('--code', help='Source code to scan (inline)')
    parser.add_argument('--file', help='Path to a source file (any language, Python rules are deepest)')
    args = parser.parse_args()

    from core.sast_sentinel_engine import SASTSentinelEngine
    code = _pick(args.code, args.file)
    if not code.strip():
        raise SystemExit("Provide --code or --file")
    report = SASTSentinelEngine.scan(code)
    print(SASTSentinelEngine.format_report(report))


if __name__ == "__main__":
    main()
