---
name: expense-auditor-agent
description: 'Audits expense reports: caps, categories, duplicates, suspicious patterns'
version: 1.0.0
author: AI Agent Architect
category: 'Finance'
---

# Expense Auditor Agent

> "Audits expense reports: caps, categories, duplicates, suspicious patterns."

**Demand basis:** Expense-compliance agents cut audit cost and are standard in mid-market finance stacks.

## 🎯 Activation Triggers
- `audit expenses`
- `expense compliance`
- `receipt check`
- `policy violations`

## ⚡ Execution Protocol
1. Parse expense lines: amount, category, date, merchant, description.
2. Apply policy: category caps, weekend/round-number/just-under-cap heuristics, duplicate receipts.
3. Score report compliance and produce the exception list with required evidence per flag.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/expense-auditor-agent/cli/expense_auditor.py --help`
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
