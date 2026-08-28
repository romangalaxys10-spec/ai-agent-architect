---
name: portfolio-scout-agent
description: 'Reviews holdings: allocation drift, concentration, correlation proxy, rebalance plan'
version: 1.0.0
author: AI Agent Architect
category: 'Finance'
---

# Portfolio Scout Agent

> "Reviews holdings: allocation drift, concentration, correlation proxy, rebalance plan."

**Demand basis:** Portfolio-review agents are the most-searched consumer finance agent.

## 🎯 Activation Triggers
- `review portfolio`
- `concentration risk`
- `rebalance plan`
- `allocation drift`

## ⚡ Execution Protocol
1. Parse holdings: symbol, value, sector, asset class, cost basis.
2. Compute allocation vs targets, concentration (HHI), sector overlap, and drawdown exposure.
3. Produce rebalance trades sized to minimize turnover plus a risk verdict.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/portfolio-scout-agent/cli/portfolio_scout.py --help`
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
