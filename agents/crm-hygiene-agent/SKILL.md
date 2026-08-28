---
name: crm-hygiene-agent
description: 'Detects duplicates, decay, and missing-field debt in CRM records; writes the merge plan'
version: 1.0.0
author: AI Agent Architect
category: 'Sales & Marketing'
---

# CRM Hygiene Agent

> "Detects duplicates, decay, and missing-field debt in CRM records; writes the merge plan."

**Demand basis:** CRM data quality is the #1 blocker sales-ops teams name for forecasting accuracy.

## 🎯 Activation Triggers
- `clean CRM`
- `dedupe records`
- `CRM audit`
- `data hygiene pass`

## ⚡ Execution Protocol
1. Load records; compute field completeness, email/phone validity, and staleness by last-touch age.
2. Detect duplicates via normalized-name/email similarity with merge-key selection.
3. Emit a cleanup plan ordered by forecast-impact: merges, enrichment queue, archive list.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/crm-hygiene-agent/cli/crm_hygiene.py --help`
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
