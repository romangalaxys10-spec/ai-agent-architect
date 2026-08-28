"""CLI for Binary Reverse Sentinel"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import argparse
import json
from agents.binary_reverse_sentinel.core.binary_engine import BinaryReverseSentinel


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
