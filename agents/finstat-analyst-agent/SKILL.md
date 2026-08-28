---
name: finstat-analyst-agent
description: 'Analyzes financial statements: margins, burn, runway, red flags, health score'
version: 1.0.0
author: AI Agent Architect
category: 'Finance'
---

# FinStat Analyst Agent

> "Analyzes financial statements: margins, burn, runway, red flags, health score."

**Demand basis:** Financial-statement analysis agents are the top finance-analyst request.

## 🎯 Activation Triggers
- `analyze financials`
- `burn rate`
- `runway calc`
- `statement red flags`

## ⚡ Execution Protocol
1. Parse line items across periods: revenue, COGS, opex, cash, receivables.
2. Compute margins, growth, burn, runway months, and working-capital ratios per period.
3. Flag red flags (negative margin expansion, receivables outpacing revenue) and score health 0-100.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/finstat-analyst-agent/cli/finstat.py --help`
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
