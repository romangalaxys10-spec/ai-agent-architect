"""CLI for Model Bridge Router (end-to-end hardened: runs from any cwd)."""
import os
import sys
import importlib.util

_AGENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_REPO_ROOT = os.path.abspath(os.path.join(_AGENT_DIR, ".."))
for _p in (_REPO_ROOT, _AGENT_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def _load(name: str, relpath: str):
    """Load engine module by explicit file path (hyphenated dirs are not importable)."""
    path = os.path.join(_AGENT_DIR, relpath)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_engine_mod = _load("core.router_engine", "core/router_engine.py")
ModelBridgeRouter = _engine_mod.ModelBridgeRouter

import argparse
import json


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
