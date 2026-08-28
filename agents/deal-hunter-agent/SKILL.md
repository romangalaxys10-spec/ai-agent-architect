---
name: deal-hunter-agent
description: 'Evaluates deals: price history percentile, rating confidence, buy/wait verdict'
version: 1.0.0
author: AI Agent Architect
category: 'Personal Productivity'
---

# Deal Hunter Agent

> "Evaluates deals: price history percentile, rating confidence, buy/wait verdict."

**Demand basis:** Shopping/deal agents lead agentic-commerce pilots (agent-driven transactions).

## 🎯 Activation Triggers
- `is this a deal`
- `price check`
- `buy or wait`
- `deal evaluation`

## ⚡ Execution Protocol
1. Parse each candidate: current price, reference price, rating, review count, stock signals.
2. Compute value score: price percentile + rating confidence (shrunk by review count) + need coverage.
3. Call BUY / WAIT / PASS per candidate with a target price and alert threshold.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/deal-hunter-agent/cli/deal_hunter.py --help`
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
