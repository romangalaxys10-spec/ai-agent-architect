"""CLI for the Test Forge Agent — Generates runnable pytest skeletons and closes coverage gaps with branch accounting"""
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
    parser = argparse.ArgumentParser(description='Test Forge Agent — pytest skeleton generation + coverage gap analysis')
    parser.add_argument('--file', help='Path to the Python source file to test')
    parser.add_argument('--source', help='Python source code inline')
    parser.add_argument('--target-coverage', type=int, default=80, help='Target coverage percent (default 80)')
    args = parser.parse_args()

    from core.test_forge_engine import TestForgeEngine
    source = _pick(args.source, args.file)
    if not source.strip():
        raise SystemExit("Provide --source or --file")
    plan = TestForgeEngine.forge(source, target_coverage=args.target_coverage)
    print(TestForgeEngine.format_plan(plan))


if __name__ == "__main__":
    main()
