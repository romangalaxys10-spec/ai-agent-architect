---
name: onboarding-guide-agent
description: 'Builds 30/60/90 onboarding plans with week-1 schedule, access, buddy wiring'
version: 1.0.0
author: AI Agent Architect
category: 'HR & Recruiting'
---

# Onboarding Guide Agent

> "Builds 30/60/90 onboarding plans with week-1 schedule, access, buddy wiring."

**Demand basis:** Onboarding agents are the highest-satisfaction HR automation per employee surveys.

## 🎯 Activation Triggers
- `onboarding plan`
- `30 60 90`
- `new hire schedule`
- `first week plan`

## ⚡ Execution Protocol
1. Parse role, team, start date, and tooling into an onboarding surface.
2. Build week-1 hour-by-hour schedule, access checklist with owners, and buddy touchpoints.
3. Define 30/60/90 outcome gates (not activities) with checkpoints and escalation paths.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/onboarding-guide-agent/cli/onboarding_guide.py --help`
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
