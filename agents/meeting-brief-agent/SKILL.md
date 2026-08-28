---
name: meeting-brief-agent
description: 'Builds pre-meeting briefs: attendee map, agenda, talk tracks, objection plays'
version: 1.0.0
author: AI Agent Architect
category: 'Sales & Marketing'
---

# Meeting Brief Agent

> "Builds pre-meeting briefs: attendee map, agenda, talk tracks, objection plays."

**Demand basis:** Meeting prep agents rank in the top tier of personal-productivity agent searches.

## 🎯 Activation Triggers
- `prep meeting`
- `meeting brief`
- `account research summary`
- `pre-call planning`

## ⚡ Execution Protocol
1. Parse meeting context: attendees + roles, topic, account history notes.
2. Build the brief: agenda with timeboxes, attendee stakes, top-3 goals, win/exit criteria.
3. Arm objection-response pairs and pre-read assignments; flag missing critical context.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/meeting-brief-agent/cli/meeting_brief.py --help`
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
