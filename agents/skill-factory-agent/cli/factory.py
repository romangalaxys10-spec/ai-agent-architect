"""CLI for the Skill Factory Agent — scaffold, package, and lint SKILL.md bundles."""
import os
import sys
import glob

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
_AGENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for _p in (_REPO_ROOT, _AGENT_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import argparse
from core.factory_engine import SkillFactoryEngine


def main():
    parser = argparse.ArgumentParser(
        description="Skill Factory Agent — scaffold, package, and validate SKILL.md bundles"
    )
    sub = parser.add_subparsers(dest="command")

    p_build = sub.add_parser("build", help="Scaffold a new skill bundle with verification fixture")
    p_build.add_argument("--name", required=True, help="Skill name (kebab-case)")
    p_build.add_argument("--description", required=True, help="One-line skill description")
    p_build.add_argument("--output-dir", default="./skills", help="Output directory")

    p_lint = sub.add_parser("lint", help="Lint all SKILL.md files for completeness")
    p_lint.add_argument("--root", default=".", help="Directory tree to scan")

    args = parser.parse_args()

    if args.command == "build":
        report = SkillFactoryEngine.build(args.name, args.description, os.path.join(args.output_dir, args.name))
        print("Skill package generated:")
        print(f"  SKILL.md: {report.output_path}")
        print(f"  Verification fixture: {report.verification_fixture}")
        print(f"  Sections present: {report.sections_present}")
        print(f"  Complete: {report.complete}")
    elif args.command == "lint":
        root = os.path.abspath(args.root)
        found = 0
        for path in sorted(glob.glob(os.path.join(root, "**", "SKILL.md"), recursive=True)):
            result = SkillFactoryEngine.lint_skill_md(path)
            status = "VALID" if result["valid"] else "INVALID"
            print(f"[{status}] {os.path.relpath(path, root)}")
            for issue in result["issues"]:
                print(f"    - {issue}")
            found += 1
        print(f"\nLinted {found} SKILL.md files.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
