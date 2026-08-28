---
name: cloud-cost-optimizer-agent
description: 'Finds idle and oversized resources, computes waste, and writes the savings plan'
version: 1.0.0
author: AI Agent Architect
category: 'Ops, IT & Security'
---

# Cloud Cost Optimizer Agent

> "Finds idle and oversized resources, computes waste, and writes the savings plan."

**Demand basis:** Cloud-cost agents deliver the fastest measurable FinOps ROI (30% average waste).

## 🎯 Activation Triggers
- `cut cloud spend`
- `rightsizing`
- `idle resources`
- `FinOps review`

## ⚡ Execution Protocol
1. Parse inventory: resource type, size, utilization, monthly cost, hours running.
2. Classify waste: idle (util ~ 0), oversized (util < threshold), zombie (off-hours full price).
3. Produce actions (stop/downsize/schedule/commit) ordered by savings per risk with a rollback note.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/cloud-cost-optimizer-agent/cli/cloud_cost.py --help`
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
