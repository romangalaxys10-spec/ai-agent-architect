---
name: content-calendar-agent
description: 'Generates 4-week calendars with format mix, hooks, and channel adaptations'
version: 1.0.0
author: AI Agent Architect
category: 'Content & Creative'
---

# Content Calendar Agent

> "Generates 4-week calendars with format mix, hooks, and channel adaptations."

**Demand basis:** Content-calendar agents are the most-adopted marketing agent after SEO.

## 🎯 Activation Triggers
- `content calendar`
- `editorial plan`
- `posting schedule`
- `content mix`

## ⚡ Execution Protocol
1. Parse goal, audience, channels, and cadence into a content strategy skeleton.
2. Generate the calendar with format mix ratios (educate/inspire/promote/community) and hooks.
3. Adapt each pillar piece per channel and attach KPI targets + repurposing map.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/content-calendar-agent/cli/content_calendar.py --help`
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
