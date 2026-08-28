"""
CLI Tool: `agy-architect` / `agent-architect`
Scaffold skills, run Steve Jobs reviews, and manage the Sub-Agents Hub.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
from factory.skill_builder import SkillBuilder, SkillManifest
from factory.prompt_synthesizer import PromptSynthesizer
from core.steve_jobs_lens import SteveJobsLens
from core.registry import AgentRegistry


def list_agents_cmd(args):
    print("🤖 Sub-Agents Hub Catalog:")
    agents = AgentRegistry.discover_agents()
    print("=" * 60)
    for aid, meta in agents.items():
        print(f"• [{aid}] {meta.name} (v{meta.version})")
        print(f"  Description: {meta.description}")
        print(f"  Path: {meta.path}")
        print(f"  Skill Spec: {meta.skill_file}")
        print("-" * 60)


def scaffold_skill_cmd(args):
    print(f"🛠️ Scaffolding new agent skill: {args.name}...")
    manifest = SkillManifest(
        name=args.name,
        description=args.description or f"Autonomous skill for {args.name}",
        triggers=[f"use {args.name}", f"trigger {args.name}"],
        fallback_rules=[
            {"condition": "Tool execution fails", "action": "Retry with reduced scope", "fallback": "Alert operator"}
        ]
    )
    builder = SkillBuilder(manifest)
    output_dir = os.path.join(args.output_dir or "./skills", args.name)
    skill_file = builder.export_skill_bundle(
        output_dir=output_dir,
        core_instructions="Operate with absolute precision. No hedging. Always verify outputs before responding.",
        workflow_steps=[
            "Inspect environment context",
            "Formulate minimal execution plan",
            "Execute tools deterministically",
            "Verify results against quality constraints"
        ]
    )
    print(f"✅ Skill generated successfully at: {skill_file}")


def review_product_cmd(args):
    print(f"🍏 Running Steve Jobs Product & Architecture Review for: {args.name}...")
    features = [f.strip() for f in args.features.split(",") if f.strip()]
    review = SteveJobsLens.evaluate_product(
        product_name=args.name,
        feature_list=features,
        one_sentence_pitch=args.pitch,
        user_journey_steps=args.steps,
        controls_whole_stack=not args.loose_stack,
    )
    print("\n" + SteveJobsLens.format_review_markdown(review))


def main():
    parser = argparse.ArgumentParser(description="AI Agent Architect CLI - Master Monorepo & Sub-Agents Hub.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: list-agents
    subparsers.add_parser("list-agents", help="List all registered sub-agents in the agents/ hub")

    # Command: scaffold-skill
    p_skill = subparsers.add_parser("scaffold-skill", help="Scaffold a new production-ready SKILL.md package")
    p_skill.add_argument("--name", required=True, help="Skill name")
    p_skill.add_argument("--description", default="", help="Skill description")
    p_skill.add_argument("--output-dir", default="./skills", help="Target output directory")

    # Command: review
    p_review = subparsers.add_parser("review", help="Evaluate product / agent architecture using Steve Jobs Product Lens")
    p_review.add_argument("--name", required=True, help="Product or agent name")
    p_review.add_argument("--pitch", required=True, help="One sentence pitch")
    p_review.add_argument("--features", required=True, help="Comma-separated feature list")
    p_review.add_argument("--steps", type=int, default=3, help="User journey steps count")
    p_review.add_argument("--loose-stack", action="store_true", help="Set if stack is not end-to-end controlled")

    args = parser.parse_args()
    if args.command == "list-agents":
        list_agents_cmd(args)
    elif args.command == "scaffold-skill":
        scaffold_skill_cmd(args)
    elif args.command == "review":
        review_product_cmd(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
