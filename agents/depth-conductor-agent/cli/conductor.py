"""CLI for Depth Conductor Agent"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import argparse
from core.depth_cognitive_engine import DepthCognitiveEngine


def main():
    parser = argparse.ArgumentParser(description="Depth Conductor Agent CLI - Cognitive Depth Reasoning")
    parser.add_argument("--query", required=True, help="Problem or architecture query to audit")
    
    args = parser.parse_args()
    profile = DepthCognitiveEngine.analyze_cognitive_depth(args.query)
    print(DepthCognitiveEngine.format_depth_report(profile))


if __name__ == "__main__":
    main()
