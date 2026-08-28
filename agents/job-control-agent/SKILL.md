---
name: job-control-agent
description: 'Foreground/background, disown/nohup, signal routing, and exit trap cleanup'
version: 1.0.0
author: AI Agent Architect
category: 'Terminal Use'
---

# Job Control Sentinel

> "Foreground/background, disown/nohup, signal routing, and exit trap cleanup"

**Demand:** Computer/Browser/Terminal/Server control & automation — part of the 100-agent Computer Use series (OS + browser + terminal + Linux/macOS/Windows engineering).

## 🎯 Activation Triggers
- `job control`
- `foreground`
- `disown`
- `signal routing`

## ⚡ Execution Protocol
1. Ingest input (`--text`/`--file`/stdin) and profile it offline (chars/words/keyword hits + OS detection).
2. Run deterministic heuristics for **Job Control Sentinel** — severity-ranked findings with evidence + fix; OS-adaptive checks for Linux/macOS/Windows.
3. Emit verdict **PASS / PASS_WITH_NOTES / NEEDS_REVIEW / BLOCKED** with prioritized next steps.

## 🧠 Cognitive Depth Protocols
- `ds-deep-think`: 3 non-obvious framings before closure.
- `ds-adversary`: worst-case injection/fault inputs.
- `ds-excavate`: hidden assumptions + missing evidence.

## 🔌 I/O Contract
- **CLI:** `python agents/job-control-agent/cli/job_control.py --help`
- **Input:** `--text` inline, `--file` path, or stdin; optional `--os linux|macos|windows|agnostic`
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
