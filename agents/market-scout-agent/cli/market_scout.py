"""CLI for the Market Scout Agent — Sizes TAM/SAM/SOM two ways, scores attractiveness, and calls the entry verdict"""
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
    parser = argparse.ArgumentParser(description='Market Scout Agent — TAM/SAM/SOM sizing + entry verdict')
    parser.add_argument('--market', required=True, help='Market description')
    parser.add_argument('--inputs', help="Inputs as 'key: value' lines (population, price, share, growth, competitors)")
    parser.add_argument('--file', help="Path to inputs file ('key: value' lines)")
    args = parser.parse_args()

    from core.market_scout_engine import MarketScoutEngine
    text = _pick(args.inputs, args.file)
    inputs = {}
    for line in text.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            inputs[k.strip()] = v.strip()
    sizing = MarketScoutEngine.size(args.market, inputs)
    print(MarketScoutEngine.format_sizing(sizing))


if __name__ == "__main__":
    main()
