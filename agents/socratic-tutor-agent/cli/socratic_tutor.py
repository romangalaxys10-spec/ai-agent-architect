"""CLI for the Socratic Tutor Agent — Builds question ladders from easy to hard with misconception probes and hints"""
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
    parser = argparse.ArgumentParser(description='Socratic Tutor Agent — question ladders + misconception probes')
    parser.add_argument('--topic', required=True, help='Topic to tutor')
    parser.add_argument('--level', default='beginner', choices=['beginner', 'intermediate', 'advanced'], help='Student level')
    parser.add_argument('--goal', default='solid understanding of core concepts', help='Learning goal')
    args = parser.parse_args()

    from core.socratic_tutor_engine import SocraticTutorEngine
    session = SocraticTutorEngine.tutor(args.topic, args.level, args.goal)
    print(SocraticTutorEngine.format_session(session))


if __name__ == "__main__":
    main()
