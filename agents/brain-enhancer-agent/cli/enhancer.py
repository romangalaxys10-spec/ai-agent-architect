"""CLI for GVS5H Brain Enhancer Sub-Agent"""
import sys
import os
import argparse
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from core.brain_enhancer import BrainEnhancerEngine, ProblemSpec


def main():
    parser = argparse.ArgumentParser(description="GVS5H Brain Enhancer CLI")
    parser.add_argument("--task", required=True, help="The algorithmic, mathematical, or system design problem")
    parser.add_argument("--ws", default="/tmp/brain_enhancer_ws", help="Workspace directory for ledger")
    parser.add_argument("--test-input", default="", help="Optional test input string")
    parser.add_argument("--test-expected", default="", help="Optional test expected output string")

    args = parser.parse_args()
    ws = os.path.abspath(args.ws)
    state = BrainEnhancerEngine.initialize_workspace(ws, args.task)

    print("🧠 GVS5H Brain Enhancer Initialized:")
    print(f"📁 Shared Ledger Workspace: {state.workspace_path}")
    print(f"📋 Task: {state.task_desc[:100]}...")

    plan_prompt = BrainEnhancerEngine.synthesize_gvs5h_prompt("primary_plan", args.task, "", "", "")
    ideate_prompt = BrainEnhancerEngine.synthesize_gvs5h_prompt("ideation", args.task, "", "", "")

    print("
--- GVS5H COGNITIVE SCAFFOLD DEPLOYED ---")
    print("1. [Primary Plan]: Decomposition into verified work units.")
    print("2. [Ideation Worker]: Prose-only algorithmic divergence (NO premature code).")
    print("3. [Living Notes]: Compacted state ledger maintained in notes.md.")
    print("4. [Anti-Fixation Engine]: Forced paradigm switching upon test failure.")

    if args.test_input and args.test_expected:
        sample_code = "import sys\nline = sys.stdin.read().strip()\nprint(line)"
        test_cases = [{"input": args.test_input, "expected": args.test_expected}]
        result = BrainEnhancerEngine.run_sample_tests(sample_code, test_cases)
        print(f"
🧪 Empirical Verification Engine Check: {result['feedback']}")


if __name__ == "__main__":
    main()
