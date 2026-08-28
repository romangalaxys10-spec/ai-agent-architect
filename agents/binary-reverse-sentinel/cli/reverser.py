"""CLI for Binary Reverse Sentinel (end-to-end hardened: runs from any cwd)."""
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


_engine_mod = _load("core.binary_engine", "core/binary_engine.py")
BinaryReverseSentinel = _engine_mod.BinaryReverseSentinel

import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="Binary Reverse Sentinel CLI")
    sub = parser.add_subparsers(dest="command")

    p_scan = sub.add_parser("scan", help="Scan binary or strings dump for secrets & endpoints")
    p_scan.add_argument("--file", required=True, help="Target binary or text strings dump")

    args = parser.parse_args()

    if args.command == "scan":
        if not os.path.exists(args.file):
            print(f"File not found: {args.file}")
            return
        with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        report = BinaryReverseSentinel.audit_binary_bundle(os.path.basename(args.file), content)
        print("🛡️ Binary Reverse Security Audit:")
        print(f"• Binary: {report.binary_name} ({report.architecture})")
        print(f"• Security Score: {report.security_score}/100")
        print(f"• ATS Arbitrary Loads: {report.ats_insecure_allows}")
        print(f"• Leaked Secrets Found: {len(report.secrets_found)}")
        for s in report.secrets_found:
            print(f"  - [{s.severity}] {s.secret_type}: {s.sample}")
        print(f"• Endpoints Discovered: {len(report.endpoints_found)}")
        for ep in report.endpoints_found[:5]:
            print(f"  - {ep}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
