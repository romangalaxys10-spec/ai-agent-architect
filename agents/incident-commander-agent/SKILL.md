---
name: incident-commander-agent
description: 'Classifies severity, runs the response runbook, drafts comms and postmortem'
version: 1.0.0
author: AI Agent Architect
category: 'Ops, IT & Security'
---

# Incident Commander Agent

> "Classifies severity, runs the response runbook, drafts comms and postmortem."

**Demand basis:** SRE incident agents are the top on-call automation request.

## 🎯 Activation Triggers
- `incident response`
- `SEV classification`
- `on-call triage`
- `status page draft`

## ⚡ Execution Protocol
1. Parse alert signals and timeline into impact scope (users, revenue, blast radius).
2. Classify SEV 1-4 and activate the matching runbook steps with role assignments.
3. Draft status-page + stakeholder comms and the postmortem skeleton with 5-whys scaffold.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/incident-commander-agent/cli/incident_commander.py --help`
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
