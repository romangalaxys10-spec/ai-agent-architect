"""
Agent Registry & Dynamic Discovery.
Scans the `agents/` directory, parses SKILL.md metadata, and registers sub-agents into the central architecture.
"""

import os
import yaml
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class SubAgentMetadata:
    id: str
    name: str
    description: str
    version: str
    author: str
    path: str
    skill_file: str
    has_cli: bool = False


class AgentRegistry:
    """Discovers and manages sub-agents within the monorepo."""

    @classmethod
    def discover_agents(cls, agents_dir: Optional[str] = None) -> Dict[str, SubAgentMetadata]:
        if not agents_dir:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            agents_dir = os.path.join(base, "agents")

        agents = {}
        if not os.path.exists(agents_dir):
            return agents

        for item in os.listdir(agents_dir):
            sub_path = os.path.join(agents_dir, item)
            if os.path.isdir(sub_path):
                skill_file = os.path.join(sub_path, "SKILL.md")
                has_cli = os.path.exists(os.path.join(sub_path, "cli"))
                name = item
                description = f"Autonomous sub-agent: {item}"
                version = "1.0.0"
                author = "AI Agent Architect"

                if os.path.exists(skill_file):
                    try:
                        with open(skill_file, "r", encoding="utf-8") as f:
                            content = f.read()
                        if content.startswith("---"):
                            parts = content.split("---", 2)
                            if len(parts) >= 3:
                                meta = yaml.safe_load(parts[1])
                                if isinstance(meta, dict):
                                    name = meta.get("name", name)
                                    description = meta.get("description", description).strip()
                                    version = meta.get("version", version)
                                    author = meta.get("author", author)
                    except Exception:
                        pass

                agents[item] = SubAgentMetadata(
                    id=item,
                    name=name,
                    description=description,
                    version=version,
                    author=author,
                    path=sub_path,
                    skill_file=skill_file,
                    has_cli=has_cli,
                )

        return agents
