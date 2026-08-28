---
name: davinci-resolve-agent
description: 'Resolve Cut/Edit/Color/Fairlight pipelines with node grading and delivery'
version: 1.0.0
author: AI Agent Architect
category: 'Creative: Video/3D/Music/YouTube'
---

# DaVinci Resolve Pilot

> "Resolve Cut/Edit/Color/Fairlight pipelines with node grading and delivery"

**Demand:** Studio-grade creative — part of the 20-agent Video Editing, 3D Creation (3D Studio), 3D Design/Modeling, Music Editing/Creation, and YouTube Curation/Editing/Remixing/Publishing series.

## 🎯 Activation Triggers
- `davinci resolve`
- `node grading`
- `fairlight`
- `delivery`

## ⚡ Execution Protocol
1. Ingest input (`--text`/`--file`/stdin) and profile it offline (creative signals + keyword hits).
2. Run deterministic heuristics for **DaVinci Resolve Pilot** — severity-ranked findings with evidence + fix (render/license, publish CTA).
3. Emit verdict **PASS / PASS_WITH_NOTES / NEEDS_REVIEW / BLOCKED** with prioritized next steps.

## 🧠 Cognitive Depth Protocols
- `ds-deep-think`: 3 non-obvious framings before closure.
- `ds-adversary`: worst-case copyright/render inputs.
- `ds-excavate`: hidden assumptions + missing evidence.

## 🔌 I/O Contract
- **CLI:** `python agents/davinci-resolve-agent/cli/davinci_resolve.py --help`
- **Input:** `--text` inline, `--file` path, or stdin
- **Output:** markdown report (verdict/score/metrics/findings/next_steps); `--json` for machine
- **Runtime:** fully offline, deterministic, zero API keys

## 🛡️ Framework Wiring
- Input validation + ceilings (guardrails)
- 3-currency budgets (steps/tokens/wall-clock) via master loop
- JSONL + cost entries via observability bus
- Evidence + severity for evaluator scoring

## 🔗 See Also
- Hub: [`agents/AGENTS.md`](../AGENTS.md)
- Master: [`README.md`](../../README.md)
