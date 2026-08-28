---
name: tiktok-sound-trend-agent
description: 'Sound velocity, dance/format fit, and early-jacking timing'
version: 1.0.0
author: AI Agent Architect
category: 'Social: TikTok'
---

# TikTok Sound Trend Scout

> "Sound velocity, dance/format fit, and early-jacking timing"

**Demand:** Social/video growth & automation — part of the 70-agent Social + Video Generation series (LinkedIn, Instagram, X, YouTube, TikTok, plus free-stock + Gemini/VeO).

## 🎯 Activation Triggers
- `tiktok sound`
- `sound velocity`
- `dance format`
- `early jacking`

## ⚡ Execution Protocol
1. Ingest input (`--text`/`--file`/stdin) and profile it offline (platform/freebie signals + hook/CTA + keyword hits).
2. Run deterministic heuristics for **TikTok Sound Trend Scout** — severity-ranked findings with evidence + fix (platform mismatch, CTA/hook, license hygiene for freebie, Gemini prompt hygiene).
3. Emit verdict **PASS / PASS_WITH_NOTES / NEEDS_REVIEW / BLOCKED** with prioritized next steps.

## 🧠 Cognitive Depth Protocols
- `ds-deep-think`: 3 non-obvious framings before closure.
- `ds-adversary`: worst-case spam/ban inputs.
- `ds-excavate`: hidden assumptions + missing evidence.

## 🔌 I/O Contract
- **CLI:** `python agents/tiktok-sound-trend-agent/cli/tiktok_sound_trend.py --help`
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
