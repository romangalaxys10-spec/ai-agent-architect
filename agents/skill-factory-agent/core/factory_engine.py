"""
Skill Factory Engine.
Scaffolds, packages, and validates production-grade SKILL.md bundles with
verification fixtures, prompt synthesis, and completeness linting
(all 15 sub-agents follow the same contract this engine emits).
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import os
import re
import sys

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def _load_repo_module(name: str, relpath: str):
    import importlib.util

    path = os.path.join(_REPO_ROOT, relpath)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_builder_mod = _load_repo_module("skill_builder", "factory/skill_builder.py")
_synth_mod = _load_repo_module("prompt_synthesizer", "factory/prompt_synthesizer.py")
SkillManifest = _builder_mod.SkillManifest
SkillBuilder = _builder_mod.SkillBuilder
PromptSynthesizer = _synth_mod.PromptSynthesizer

REQUIRED_SKILL_SECTIONS = [
    "Activation Triggers",
    "Execution Workflow",
    "Core Operational Guidelines",
    "Failure Modes",
]


@dataclass
class SkillPackageReport:
    skill_name: str
    output_path: str
    sections_present: List[str]
    sections_missing: List[str]
    verification_fixture: str
    system_prompt: str
    complete: bool


class SkillFactoryEngine:
    """Automated scaffolding, packaging, and validation of SKILL.md bundles."""

    @classmethod
    def build(
        cls,
        name: str,
        description: str,
        output_dir: str,
        core_instructions: str = (
            "Operate with absolute precision. No hedging. Always verify outputs "
            "before responding. Escalate irreversible actions to human approval."
        ),
        workflow_steps: Optional[List[str]] = None,
    ) -> SkillPackageReport:
        workflow_steps = workflow_steps or [
            "Inspect environment context",
            "Formulate minimal execution plan with success predicate",
            "Execute tools deterministically within budget",
            "Verify results against quality constraints",
            "Record episodic memory of the outcome",
        ]
        manifest = SkillManifest(
            name=name,
            description=description,
            triggers=[f"use {name}", f"trigger {name}", f"activate {name}"],
            fallback_rules=[
                {"condition": "Tool execution fails", "action": "Retry with reduced scope", "fallback": "Alert operator"},
                {"condition": "Budget exhausted", "action": "Degrade gracefully and summarize", "fallback": "Checkpoint and resume later"},
                {"condition": "Ambiguous input", "action": "Ask one clarifying question", "fallback": "Proceed with conservative default"},
            ],
        )
        builder = SkillBuilder(manifest)
        skill_path = builder.export_skill_bundle(
            output_dir=output_dir, core_instructions=core_instructions, workflow_steps=workflow_steps
        )

        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()
        present = [s for s in REQUIRED_SKILL_SECTIONS if s.lower() in content.lower()]
        missing = [s for s in REQUIRED_SKILL_SECTIONS if s.lower() not in content.lower()]

        prompt = PromptSynthesizer.build_system_prompt(
            role_name=name,
            mission=description,
            core_principles=["Radical focus: do one thing completely", "Verify before you speak"],
            operational_rules=["Inspect context before acting", "Escalate irreversible actions"],
            output_format_contract="Markdown with sections: Summary, Evidence, Next Actions",
            anti_patterns=["hedging", "invented facts", "skipping verification"],
        )

        fixture = cls._verification_fixture(name)
        fixture_path = os.path.join(os.path.dirname(skill_path), "verification.py")
        with open(fixture_path, "w", encoding="utf-8") as f:
            f.write(fixture)

        return SkillPackageReport(
            skill_name=name,
            output_path=skill_path,
            sections_present=present,
            sections_missing=missing,
            verification_fixture=fixture_path,
            system_prompt=prompt,
            complete=not missing,
        )

    @staticmethod
    def _verification_fixture(skill_name: str) -> str:
        safe = re.sub(r"\W+", "_", skill_name.lower())
        return f'''"""Verification fixture for skill: {skill_name}"""
import unittest


class Test{safe.title() if safe else "Skill"}Contract(unittest.TestCase):
    def test_skill_md_exists_and_parses(self):
        import os, yaml
        path = os.path.join(os.path.dirname(__file__), "SKILL.md")
        self.assertTrue(os.path.exists(path), "SKILL.md must exist")
        content = open(path, encoding="utf-8").read()
        self.assertTrue(content.startswith("---"), "YAML frontmatter required")
        parts = content.split("---", 2)
        meta = yaml.safe_load(parts[1])
        for key in ("name", "description", "version"):
            self.assertIn(key, meta, f"frontmatter missing: {{key}}")

    def test_workflow_has_steps(self):
        path = os.path.join(os.path.dirname(__file__), "SKILL.md")
        content = open(path, encoding="utf-8").read()
        self.assertIn("Execution Workflow", content)
        self.assertIn("Failure Modes", content)


if __name__ == "__main__":
    unittest.main()
'''

    @classmethod
    def lint_skill_md(cls, path: str) -> Dict[str, Any]:
        """Completeness lint for any SKILL.md in the repo."""
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        issues = []
        if not content.startswith("---"):
            issues.append("missing YAML frontmatter")
        else:
            parts = content.split("---", 2)
            if len(parts) < 3:
                issues.append("malformed frontmatter")
            else:
                try:
                    import yaml
                    meta = yaml.safe_load(parts[1])
                    for key in ("name", "description", "version"):
                        if key not in meta:
                            issues.append(f"frontmatter missing: {key}")
                except Exception as exc:
                    issues.append(f"frontmatter unparseable: {exc}")
        for section in REQUIRED_SKILL_SECTIONS:
            if section.lower() not in content.lower():
                issues.append(f"missing section: {section}")
        return {"path": path, "issues": issues, "valid": not issues}
