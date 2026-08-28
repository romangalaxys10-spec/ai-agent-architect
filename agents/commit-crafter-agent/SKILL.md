---
name: commit-crafter-agent
description: 'Turns raw diffs into conventional commits, changelog entries, and semver bumps'
version: 1.0.0
author: AI Agent Architect
category: 'Coding & Development'
---

# Commit Crafter Agent

> "Turns raw diffs into conventional commits, changelog entries, and semver bumps."

**Demand basis:** Commit message + changelog generation is the most-used Copilot-class micro-agent task.

## 🎯 Activation Triggers
- `write commit message`
- `changelog entry`
- `semver bump`
- `conventional commit`

## ⚡ Execution Protocol
1. Parse the diff: touched paths, hunk intents (feature/fix/docs/refactor/test/chore), and breaking signals.
2. Craft a conventional-commit message with body bullets scoped to the change intent.
3. Derive the semver bump and a Keep-a-Changelog entry; flag breaking changes for release notes.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/commit-crafter-agent/cli/commit_crafter.py --help`
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
