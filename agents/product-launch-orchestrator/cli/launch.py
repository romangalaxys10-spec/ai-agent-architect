"""CLI for Product Launch Orchestrator (end-to-end hardened: runs from any cwd)."""
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


_engine_mod = _load("core.launch_engine", "core/launch_engine.py")
ProductLaunchOrchestrator = _engine_mod.ProductLaunchOrchestrator

import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="Product Launch Orchestrator CLI")
    sub = parser.add_subparsers(dest="command")

    p_pkg = sub.add_parser("create", help="Generate full multi-platform launch campaign package")
    p_pkg.add_argument("--name", default="SuperDesign Agent", help="Product/Repo name")
    p_pkg.add_argument("--url", default="https://github.com/romangalaxys10-spec/superdesign-agent", help="GitHub repo URL")

    args = parser.parse_args()

    if args.command == "create":
        camp = ProductLaunchOrchestrator.generate_launch_package(args.name, args.url)
        print("🚀 Multi-Platform Product Launch Package Created:")
        print(f"• Target Product: {camp.product_name}")
        print("\n--- SHOW HN POST ---")
        print(camp.show_hn_post)
        print("\n--- PRODUCT HUNT PITCH ---")
        print(json.dumps(camp.product_hunt_pitch, indent=2))
        print("\n--- 3-DAY LAUNCH TIMELINE ---")
        for step in camp.three_day_timeline:
            print(f"• [{step['day']}]: {step['action']}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
