---
name: linux-perf-flame-agent
description: 'perf, flame graphs, and pressure stall (PSI) diagnosis'
version: 1.0.0
author: AI Agent Architect
category: 'SysAdmin: Linux'
---

# Linux Perf Flame

> "perf, flame graphs, and pressure stall (PSI) diagnosis"

**Demand:** Sys-admin control plane — part of the 90-agent SysAdmin series (Solana/Blockchain/Linux/Server/Security/Debug/Local LLM/Web Design/Web Dev).

## 🎯 Activation Triggers
- `linux perf`
- `flame graph`
- `psi`
- `pressure stall`

## ⚡ Execution Protocol
1. Ingest input (`--text`/`--file`/stdin) and profile it offline (sys signals + keyword hits).
2. Run deterministic heuristics for **Linux Perf Flame** — severity-ranked findings with evidence + fix (secret exposure, urgency, domain-specific hygiene).
3. Emit verdict **PASS / PASS_WITH_NOTES / NEEDS_REVIEW / BLOCKED** with prioritized next steps.

## 🧠 Cognitive Depth Protocols
- `ds-deep-think`: 3 non-obvious framings before closure.
- `ds-adversary`: worst-case secret/bypass inputs.
- `ds-excavate`: hidden assumptions + missing evidence.

## 🔌 I/O Contract
- **CLI:** `python agents/linux-perf-flame-agent/cli/linux_perf_flame.py --help`
- **Input:** `--text` inline, `--file` path, or stdin
- **Output:** markdown report (verdict/score/metrics/findings/next_steps); `--json` for machine
- **Runtime:** fully offline, deterministic, zero API keys

## 🛡️ Framework Wiring
- Input validation + ceilings (guardrails) + secret scrubbing
- 3-currency budgets (steps/tokens/wall-clock) via master loop
- JSONL + cost entries via observability bus
- Evidence + severity for evaluator scoring

## 🔗 See Also
- Hub: [`agents/AGENTS.md`](../AGENTS.md)
- Master: [`README.md`](../../README.md)
