---
name: sla-sentinel-agent
description: 'Projects SLA breach risk per ticket and orders the queue by preventable-breach value'
version: 1.0.0
author: AI Agent Architect
category: 'Customer Support'
---

# SLA Sentinel Agent

> "Projects SLA breach risk per ticket and orders the queue by preventable-breach value."

**Demand basis:** SLA breach prevention is the most common support-ops automation after routing.

## 🎯 Activation Triggers
- `SLA risk`
- `breach forecast`
- `queue prioritization`
- `response time risk`

## ⚡ Execution Protocol
1. Load queue: each ticket's priority, SLA hours, age, and last-response time.
2. Project time-to-breach from age velocity and compute breach probability per ticket.
3. Order interventions by preventable-breach value and propose reassignment/deflection actions.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/sla-sentinel-agent/cli/sla_sentinel.py --help`
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
