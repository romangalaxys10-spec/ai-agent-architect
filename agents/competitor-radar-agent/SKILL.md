---
name: competitor-radar-agent
description: 'Classifies competitor moves, scores threat, and updates battlecards with responses'
version: 1.0.0
author: AI Agent Architect
category: 'Sales & Marketing'
---

# Competitor Radar Agent

> "Classifies competitor moves, scores threat, and updates battlecards with responses."

**Demand basis:** Competitive intelligence agents are top-requested in B2B marketing teams.

## 🎯 Activation Triggers
- `competitor analysis`
- `battlecard update`
- `competitive threat`
- `market move scan`

## ⚡ Execution Protocol
1. Classify each event: pricing, feature, partnership, funding, PR, hiring, outage.
2. Score threat level by category x proximity to your differentiators.
3. Update battlecard deltas and prescribe counter-plays per event with owner + deadline.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/competitor-radar-agent/cli/competitor_radar.py --help`
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
