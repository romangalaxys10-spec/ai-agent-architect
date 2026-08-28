---
name: meeting-scribe-agent
description: 'Converts raw meeting notes/transcripts into decisions, owners, deadlines, questions'
version: 1.0.0
author: AI Agent Architect
category: 'Personal Productivity'
---

# Meeting Scribe Agent

> "Converts raw meeting notes/transcripts into decisions, owners, deadlines, questions."

**Demand basis:** Meeting-notes agents are the most-adopted team productivity agent.

## 🎯 Activation Triggers
- `meeting notes`
- `extract action items`
- `summarize meeting`
- `who owns what`

## ⚡ Execution Protocol
1. Detect decision sentences (agreed/decided/will go with) vs action sentences (assignee + verb + date).
2. Extract action items as owner-task-deadline triples; catch dateless tasks and force follow-up.
3. Produce digest: summary, decisions, actions table, open questions, and risk mentions.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/meeting-scribe-agent/cli/meeting_scribe.py --help`
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
