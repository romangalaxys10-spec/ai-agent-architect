"""
Skill Factory: Automated generation and validation of modular Agent Skills (SKILL.md).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import os
import yaml


@dataclass
class SkillManifest:
    name: str
    description: str
    version: str = "1.0.0"
    author: str = "AI Agent Architect"
    triggers: List[str] = field(default_factory=list)
    tools_required: List[str] = field(default_factory=list)
    fallback_rules: List[Dict[str, str]] = field(default_factory=list)


class SkillBuilder:
    """Builds, packages, and validates SKILL.md bundles."""

    def __init__(self, manifest: SkillManifest):
        self.manifest = manifest

    def render_skill_md(self, core_instructions: str, workflow_steps: List[str]) -> str:
        """Generates standard SKILL.md markdown with YAML frontmatter."""
        frontmatter = {
            "name": self.manifest.name,
            "description": self.manifest.description.strip(),
            "version": self.manifest.version,
            "author": self.manifest.author,
        }
        
        yaml_header = yaml.dump(frontmatter, sort_keys=False).strip()
        
        triggers_formatted = "\n".join(f"- `{t}`" for t in self.manifest.triggers)
        steps_formatted = "\n".join(f"{i+1}. **{step}**" for i, step in enumerate(workflow_steps))
        
        fallbacks_formatted = ""
        if self.manifest.fallback_rules:
            fallbacks_formatted = "## 🛡️ Failure Modes & Fallback Tree\n\n| Trigger Condition | Primary Action | Fallback Safeguard |\n|---|---|---|\n"
            for rule in self.manifest.fallback_rules:
                fallbacks_formatted += f"| {rule.get('condition', '')} | {rule.get('action', '')} | {rule.get('fallback', '')} |\n"

        content = f"""---
{yaml_header}
---

# {self.manifest.name.replace('-', ' ').title()}

> "{self.manifest.description.strip()}"

## 🎯 Activation Triggers
{triggers_formatted}

---

## ⚡ Execution Workflow (Protocol)
{steps_formatted}

---

## 🧠 Core Operational Guidelines
{core_instructions.strip()}

---

{fallbacks_formatted}
"""
        return content

    def export_skill_bundle(self, output_dir: str, core_instructions: str, workflow_steps: List[str]):
        """Exports SKILL.md and directory skeleton."""
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "scripts"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "references"), exist_ok=True)
        
        skill_path = os.path.join(output_dir, "SKILL.md")
        content = self.render_skill_md(core_instructions, workflow_steps)
        with open(skill_path, "w", encoding="utf-8") as f:
            f.write(content)
        return skill_path
