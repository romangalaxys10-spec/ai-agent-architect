---
name: copy-editor-agent
description: 'Edits for clarity: passive voice, filler, sentence length, jargon, readability'
version: 1.0.0
author: AI Agent Architect
category: 'Content & Creative'
---

# Copy Editor Agent

> "Edits for clarity: passive voice, filler, sentence length, jargon, readability."

**Demand basis:** Copy-editing is the longest-lived and most-used writing agent task.

## 🎯 Activation Triggers
- `edit copy`
- `improve clarity`
- `readability pass`
- `style lint`

## ⚡ Execution Protocol
1. Detect passive voice, filler words, adverb stacking, jargon, and overlong sentences.
2. Compute readability scores (Flesch, sentence-length distribution) before and after.
3. Produce line-level edit suggestions with rationale and a rewritten plain-language version.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/copy-editor-agent/cli/copy_editor.py --help`
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
