---
name: trip-compass-agent
description: 'Builds day-by-day itineraries with pacing, budget split, packing, contingencies'
version: 1.0.0
author: AI Agent Architect
category: 'Personal Productivity'
---

# Trip Compass Agent

> "Builds day-by-day itineraries with pacing, budget split, packing, contingencies."

**Demand basis:** Travel-planning agents are among the top-5 most-searched consumer agents.

## 🎯 Activation Triggers
- `plan trip`
- `build itinerary`
- `travel plan`
- `vacation schedule`

## ⚡ Execution Protocol
1. Parse destination, dates, pace, interests, and budget envelope.
2. Balance the itinerary: anchor activity + recovery per day, cluster by geography, no 3-museum days.
3. Allocate budget per category, generate packing list from climate/activities, add contingency plans.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/trip-compass-agent/cli/trip_compass.py --help`
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
