"""CLI for the Senior Architect Agent — architectural decomposition + anti-pattern review."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
from core.architect_engine import SeniorArchitectEngine


def main():
    parser = argparse.ArgumentParser(
        description="Senior Architect Agent — cognitive DAG decomposition & zero-trust review"
    )
    parser.add_argument("--requirement", required=True, help="System requirement to architect")
    parser.add_argument("--name", default="UnnamedSystem", help="System name")
    args = parser.parse_args()

    blueprint = SeniorArchitectEngine.decompose(args.requirement, system_name=args.name)
    print(SeniorArchitectEngine.format_blueprint(blueprint))


if __name__ == "__main__":
    main()
