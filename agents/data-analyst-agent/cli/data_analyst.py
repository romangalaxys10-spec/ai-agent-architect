"""CLI for the Data Analyst Agent — Profiles CSVs end-to-end: stats, outliers, correlations, ranked insights, chart picks"""
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
    parser = argparse.ArgumentParser(description='Data Analyst Agent — CSV profiling + insights + chart recommendations')
    parser.add_argument('--data', help='CSV content (inline)')
    parser.add_argument('--file', help='Path to a CSV file')
    args = parser.parse_args()

    from core.data_analyst_engine import DataAnalystEngine
    text = _pick(args.data, args.file)
    if not text.strip():
        raise SystemExit("Provide --data or --file")
    analysis = DataAnalystEngine.analyze(text)
    print(DataAnalystEngine.format_analysis(analysis))


if __name__ == "__main__":
    main()
