---
name: email-triage-agent
description: 'Sorts an inbox into urgency quadrants, extracts asks/deadlines, drafts replies'
version: 1.0.0
author: AI Agent Architect
category: 'Personal Productivity'
---

# Email Triage Agent

> "Sorts an inbox into urgency quadrants, extracts asks/deadlines, drafts replies."

**Demand basis:** Email triage is the #1 most-searched personal AI agent use case.

## 🎯 Activation Triggers
- `triage inbox`
- `prioritize email`
- `email overload`
- `draft replies`

## ⚡ Execution Protocol
1. Parse each email: sender seniority, ask verbs, deadlines, and length.
2. Place each in the Eisenhower quadrant and assign action type (reply/forward/delegate/read/archive).
3. Draft reply skeletons for the top quadrant items and batch the rest into time blocks.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/email-triage-agent/cli/email_triage.py --help`
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
