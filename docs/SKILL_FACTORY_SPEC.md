# Agent Skill Factory Specification
*Universal Standard for Encapsulated Agent Capabilities (`SKILL.md`)*

---

## 1. Specification Overview
A **Skill** is a self-contained capability package that endows an AI agent with domain expertise, tools, workflows, and fallback trees.

```
skills/my-specialized-skill/
├── SKILL.md                 # Primary instruction manifest & metadata
├── scripts/                 # Deterministic helper tools & automation
├── references/              # Deep domain documentation & cheat sheets
└── tests/                   # Automated skill verification tests
```

---

## 2. Frontmatter Standard
Every `SKILL.md` MUST contain YAML frontmatter:

```yaml
---
name: my-specialized-skill
description: Precise, high-salience description of capability and activation triggers.
version: 1.0.0
author: AI Agent Architect
---
```

---

## 3. Required Sections in `SKILL.md`
1. **Activation Triggers:** Explicit user intents or keywords that invoke this skill.
2. **Execution Workflow (Protocol):** Step-by-step deterministic process for the agent to follow.
3. **Core Operational Guidelines:** Quality standards, constraints, and anti-patterns.
4. **Failure Modes & Fallback Tree:** Structured matrix of potential failure conditions and mitigation steps.
