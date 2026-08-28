---
name: calendar-architect-agent
description: 'Schedules tasks against real constraints: deadlines, energy, focus blocks, conflicts'
version: 1.0.0
author: AI Agent Architect
category: 'Personal Productivity'
---

# Calendar Architect Agent

> "Schedules tasks against real constraints: deadlines, energy, focus blocks, conflicts."

**Demand basis:** Calendar/scheduling agents are top-2 personal assistant requests.

## 🎯 Activation Triggers
- `plan my day`
- `schedule tasks`
- `find focus time`
- `calendar conflict`

## ⚡ Execution Protocol
1. Load working hours, existing meetings, and the task list with durations/deadlines/priorities.
2. Schedule by earliest-deadline-first with priority preemption; defend two focus blocks.
3. Flag conflicts and overrun risks; emit a realistic day plan with buffer margins.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/calendar-architect-agent/cli/calendar_architect.py --help`
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
