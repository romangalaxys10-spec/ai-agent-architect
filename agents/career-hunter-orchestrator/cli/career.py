"""CLI for Career Hunter Orchestrator"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import argparse
import json
from agents.career_hunter_orchestrator.core.career_engine import CareerHunterEngine


def main():
    parser = argparse.ArgumentParser(description="Career Hunter Orchestrator CLI")
    sub = parser.add_subparsers(dest="command")

    p_scout = sub.add_parser("scout", help="Analyze job description and compute match score")
    p_scout.add_argument("--title", default="Senior AI Systems Engineer", help="Job title")
    p_scout.add_argument("--company", default="ScaleAI Labs", help="Company name")
    p_scout.add_argument("--desc", default="Looking for a Python and Rust engineer experienced with AI agents and Solana streaming pipelines.", help="Job description")

    p_resume = sub.add_parser("resume", help="Generate ATS-compliant tailored resume")
    p_resume.add_argument("--title", default="Senior AI Architect", help="Target job title")
    p_resume.add_argument("--out", default="./output/tailored_resume.md", help="Output file")

    args = parser.parse_args()

    if args.command == "scout":
        lead = CareerHunterEngine.analyze_job_posting(args.title, args.desc, args.company)
        print(f"🎯 Job Lead Analyzed for {args.company}:")
        print(json.dumps(lead.__dict__, indent=2))
    elif args.command == "resume":
        lead = CareerHunterEngine.analyze_job_posting(args.title, "Python Solana AI Agents System Design", "Premier Corp")
        res = CareerHunterEngine.generate_ats_resume(lead)
        os.makedirs(os.path.dirname(args.out), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(res)
        print(f"✅ ATS-compliant resume generated at: {args.out}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
