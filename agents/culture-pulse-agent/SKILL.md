---
name: culture-pulse-agent
description: 'Analyzes engagement surveys: eNPS, distribution, comment themes, segment gaps'
version: 1.0.0
author: AI Agent Architect
category: 'HR & Recruiting'
---

# Culture Pulse Agent

> "Analyzes engagement surveys: eNPS, distribution, comment themes, segment gaps."

**Demand basis:** Engagement-survey analysis is the most-outsourced People-Ops task to agents.

## 🎯 Activation Triggers
- `survey analysis`
- `eNPS`
- `engagement pulse`
- `culture themes`

## ⚡ Execution Protocol
1. Compute eNPS, score distribution, and participation per segment.
2. Theme-mine comments with sentiment; rank drivers of promoters vs detractors.
3. Recommend 2-3 interventions mapped to the biggest detractor themes with owners.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/culture-pulse-agent/cli/culture_pulse.py --help`
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
