---
name: ticket-router-agent
description: 'Classifies support tickets, extracts entities, and routes to queue with SLA clock'
version: 1.0.0
author: AI Agent Architect
category: 'Customer Support'
---

# Ticket Router Agent

> "Classifies support tickets, extracts entities, and routes to queue with SLA clock."

**Demand basis:** Support automation is the largest enterprise agent spend category (Zendesk, Fin, Sierra).

## 🎯 Activation Triggers
- `route ticket`
- `classify support request`
- `triage inbox`
- `queue assignment`

## ⚡ Execution Protocol
1. Classify ticket intent (billing/bug/how-to/feature/security/abuse) with confidence.
2. Extract entities: order IDs, emails, product names, versions, and emotional intensity words.
3. Route to queue with priority + SLA timer and suggest the top matching macro/KB article.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/ticket-router-agent/cli/ticket_router.py --help`
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
