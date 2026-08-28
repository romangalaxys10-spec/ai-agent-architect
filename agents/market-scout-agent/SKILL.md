---
name: market-scout-agent
description: 'Sizes TAM/SAM/SOM two ways, scores attractiveness, and calls the entry verdict'
version: 1.0.0
author: AI Agent Architect
category: 'Research & Analysis'
---

# Market Scout Agent

> "Sizes TAM/SAM/SOM two ways, scores attractiveness, and calls the entry verdict."

**Demand basis:** Market-sizing agents are core to strategy and VC workflows.

## 🎯 Activation Triggers
- `size market`
- `TAM SAM SOM`
- `market attractiveness`
- `entry assessment`

## ⚡ Execution Protocol
1. Run top-down and bottom-up sizing from supplied inputs; reconcile and error-band them.
2. Score attractiveness: growth, competition density, buyer budget, regulation drag.
3. Call the entry verdict (enter / niche / pass) with the kill-risk list and needed evidence.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/market-scout-agent/cli/market_scout.py --help`
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
