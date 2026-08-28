---
name: invoice-intake-agent
description: 'Parses inbound invoices, checks arithmetic, policy, duplicates, 3-way match'
version: 1.0.0
author: AI Agent Architect
category: 'Finance'
---

# Invoice Intake Agent

> "Parses inbound invoices, checks arithmetic, policy, duplicates, 3-way match."

**Demand basis:** AP automation is the highest-ROI finance agent use case (accounts-payable ops).

## 🎯 Activation Triggers
- `process invoice`
- `AP intake`
- `invoice validation`
- `3-way match`

## ⚡ Execution Protocol
1. Parse vendor, invoice number, dates, line items, subtotal/tax/total from invoice text.
2. Validate arithmetic (line sum, tax math), policy thresholds, and duplicate numbers against history.
3. Emit posting recommendation (approve / hold / reject) with exception reasons and GL coding hints.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/invoice-intake-agent/cli/invoice_intake.py --help`
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
