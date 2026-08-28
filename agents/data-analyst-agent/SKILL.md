---
name: data-analyst-agent
description: 'Profiles CSVs end-to-end: stats, outliers, correlations, ranked insights, chart picks'
version: 1.0.0
author: AI Agent Architect
category: 'Research & Analysis'
---

# Data Analyst Agent

> "Profiles CSVs end-to-end: stats, outliers, correlations, ranked insights, chart picks."

**Demand basis:** Data-analyst agents are the most-searched analytics agent persona.

## 🎯 Activation Triggers
- `analyze dataset`
- `CSV insights`
- `column profile`
- `find outliers`

## ⚡ Execution Protocol
1. Profile every column: type inference, nulls, cardinality, and distribution stats.
2. Compute numeric correlations and z-score outliers; detect leaky/duplicate columns.
3. Rank auto-insights by interestingness and recommend the chart type per insight.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/data-analyst-agent/cli/data_analyst.py --help`
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
