---
name: script-writer-agent
description: 'Writes video scripts: 5-second hook, beat structure, retention tactics, cutdowns'
version: 1.0.0
author: AI Agent Architect
category: 'Content & Creative'
---

# Script Writer Agent

> "Writes video scripts: 5-second hook, beat structure, retention tactics, cutdowns."

**Demand basis:** Video-script agents are the top creator-economy agent search.

## 🎯 Activation Triggers
- `write video script`
- `youtube script`
- `hook + beats`
- `shorts cutdown`

## ⚡ Execution Protocol
1. Fit structure to duration and platform: hook, promise, beats with timestamps, payoff, CTA.
2. Insert retention tactics at drop-off points (pattern breaks, open loops, visual changes).
3. Emit B-roll cues, caption notes, and platform cutdowns (YouTube/TikTok/Shorts).

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/script-writer-agent/cli/script_writer.py --help`
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
