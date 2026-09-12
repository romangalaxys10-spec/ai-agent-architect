"""CLI for Code Review & Refactoring Sentinel"""
import sys, os, argparse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from agents.code_review_refactor_sentinel.core.review_engine import CodeReviewEngine


def main():
    parser = argparse.ArgumentParser(description="Code Review & Refactoring Sentinel")
    parser.add_argument("file", help="Path to Python file to review")
    parser.add_argument("--patch", action="store_true", help="Print refactoring unified diff patch")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File not found {args.file}")
        sys.exit(1)

    with open(args.file, "r", encoding="utf-8") as f:
        code = f.read()

    report = CodeReviewEngine.analyze_code(code, args.file)
    print(f"🛡️ Review Report for: {report.file_path}")
    print(f"Lines: {report.total_lines} | Cyclomatic Complexity: {report.complexity_score} | Verdict: {report.verdict}")
    print("-" * 60)
    if not report.issues:
        print("✅ No security or quality issues detected. Clean codebase!")
    else:
        for iss in report.issues:
            print(f"[{iss.severity}] L{iss.line_number} ({iss.rule_id}): {iss.message}")
            print(f"    Suggested Fix: {iss.suggested_fix}")

    if args.patch and report.diff_patch:
        print("
--- RECOMMENDED REFACTOR PATCH ---")
        print(report.diff_patch)


if __name__ == "__main__":
    main()
