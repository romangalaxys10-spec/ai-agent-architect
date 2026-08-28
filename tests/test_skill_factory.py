"""Unit tests for Skill Factory & Prompt Synthesizer"""

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from factory.skill_builder import SkillBuilder, SkillManifest
from factory.prompt_synthesizer import PromptSynthesizer


class TestSkillFactory(unittest.TestCase):
    def test_skill_manifest_render(self):
        manifest = SkillManifest(
            name="test-skill",
            description="A test skill for unit verification",
            triggers=["run test", "verify skill"],
            fallback_rules=[{"condition": "error", "action": "retry", "fallback": "abort"}]
        )
        builder = SkillBuilder(manifest)
        md = builder.render_skill_md(
            core_instructions="Operate with zero errors.",
            workflow_steps=["Step A", "Step B"]
        )
        self.assertIn("name: test-skill", md)
        self.assertIn("Step A", md)
        self.assertIn("Failure Modes & Fallback Tree", md)

    def test_prompt_synthesizer(self):
        prompt = PromptSynthesizer.build_system_prompt(
            role_name="SecOps Architect",
            mission="Audit cloud infrastructure",
            core_principles=["Zero Trust", "Minimal Privileges"],
            operational_rules=["Verify IAM roles", "Inspect security groups"],
            output_format_contract="JSON output only",
            anti_patterns=["Do not disable 2FA"]
        )
        self.assertIn("<identity>", prompt)
        self.assertIn("SecOps Architect", prompt)
        self.assertIn("Zero Trust", prompt)


if __name__ == "__main__":
    unittest.main()
