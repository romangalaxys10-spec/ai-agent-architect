---
name: social-media-manager-agent
description: 'Generates post variants, hashtag sets, thread structures, response templates'
version: 1.0.0
author: AI Agent Architect
category: 'Content & Creative'
---

# Social Media Manager Agent

> "Generates post variants, hashtag sets, thread structures, response templates."

**Demand basis:** Social-posting agents are the most-used creator/marketing micro-agents.

## 🎯 Activation Triggers
- `write social post`
- `thread structure`
- `hashtag strategy`
- `engagement replies`

## ⚡ Execution Protocol
1. Adapt message to platform constraints (length, tone, link policy) and audience.
2. Generate 3 post variants + thread/carousel structure + vetted hashtag tiers.
3. Attach posting-time windows, engagement reply templates, and do-not-post guardrails.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/social-media-manager-agent/cli/social_media.py --help`
- **Input:** CLI arguments (see `--help`); text or JSON input inline or via `--file`
- **Output:** structured report with verdict/plan + ranked next actions
- **Runtime:** fully offline, deterministic, zero API keys

## 🛡️ Framework Wiring
- Input validation + length ceilings before processing (guardrails discipline)
- 3-currency budgets (steps/tokens/wall-clock) enforced by the master loop
- JSONL event + cost entries via the observability bus on every run
- Findings carry evidence + severity so the evaluation judge can score them

## 🔗 See Also
- Hub catalog: [`agents/AGENTS.md`](../AGENTS.md)
- Master architecture: [`README.md`](../../README.md)
