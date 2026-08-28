"""CLI for Model Bridge Router"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import argparse
import json
from agents.model_bridge_router.core.router_engine import ModelBridgeRouter


def main():
    parser = argparse.ArgumentParser(description="Model Bridge Router CLI")
    sub = parser.add_subparsers(dest="command")

    p_route = sub.add_parser("route", help="Evaluate prompt and determine optimal model routing")
    p_route.add_argument("--prompt", required=True, help="Prompt text to analyze")
    p_route.add_argument("--code", action="store_true", help="Flag if code execution is required")

    args = parser.parse_args()

    if args.command == "route":
        decision = ModelBridgeRouter.route_request(args.prompt, requires_code=args.code)
        print("🧠 Routing Decision:")
        print(json.dumps(decision.__dict__, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
