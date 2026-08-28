---
name: x-trend-jacker-agent
description: 'Trend velocity, angle fit, and safe trend-jacking timing'
version: 1.0.0
author: AI Agent Architect
category: 'Social: X'
---

# X Trend Jacker

> "Trend velocity, angle fit, and safe trend-jacking timing"

**Demand:** Social/video growth & automation — part of the 70-agent Social + Video Generation series (LinkedIn, Instagram, X, YouTube, TikTok, plus free-stock + Gemini/VeO).

## 🎯 Activation Triggers
- `x trend`
- `trend velocity`
- `angle fit`
- `trend jacking`

## ⚡ Execution Protocol
1. Ingest input (`--text`/`--file`/stdin) and profile it offline (platform/freebie signals + hook/CTA + keyword hits).
2. Run deterministic heuristics for **X Trend Jacker** — severity-ranked findings with evidence + fix (platform mismatch, CTA/hook, license hygiene for freebie, Gemini prompt hygiene).
3. Emit verdict **PASS / PASS_WITH_NOTES / NEEDS_REVIEW / BLOCKED** with prioritized next steps.

## 🧠 Cognitive Depth Protocols
- `ds-deep-think`: 3 non-obvious framings before closure.
- `ds-adversary`: worst-case spam/ban inputs.
- `ds-excavate`: hidden assumptions + missing evidence.

## 🔌 I/O Contract
- **CLI:** `python agents/x-trend-jacker-agent/cli/x_trend_jacker.py --help`
- **Input:** `--text` inline, `--file` path, or stdin
- **Output:** markdown report (verdict/score/metrics/findings/next_steps); `--json` for machine
- **Runtime:** fully offline, deterministic, zero API keys

## 🛡️ Framework Wiring
- Input validation + ceilings (guardrails) + spam/ToS safety
- 3-currency budgets (steps/tokens/wall-clock) via master loop
- JSONL + cost entries via observability bus
- Evidence + severity for evaluator scoring

## 🔗 See Also
- Hub: [`agents/AGENTS.md`](../AGENTS.md)
- Master: [`README.md`](../../README.md)
