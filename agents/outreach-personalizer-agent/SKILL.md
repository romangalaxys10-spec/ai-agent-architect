---
name: outreach-personalizer-agent
description: 'Writes 3-tone personalized cold emails with spam-word linting and A/B variants'
version: 1.0.0
author: AI Agent Architect
category: 'Sales & Marketing'
---

# Outreach Personalizer Agent

> "Writes 3-tone personalized cold emails with spam-word linting and A/B variants."

**Demand basis:** Email personalization at scale is the most-deployed sales agent per vendor reports.

## 🎯 Activation Triggers
- `write outreach email`
- `personalize cold email`
- `sales sequence`
- `follow-up copy`

## ⚡ Execution Protocol
1. Extract prospect hooks: role pains, tech stack, milestones, public signals.
2. Draft three tone variants (peer-expert, crisp-executive, curious-storyteller) mapped to the offer.
3. Lint spam triggers, keep under 120 words, and design a 3-touch A/B sequence.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/outreach-personalizer-agent/cli/outreach_personalizer.py --help`
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
