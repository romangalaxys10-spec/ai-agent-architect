---
name: dep-guardian-agent
description: 'Audits dependency manifests for risk, staleness, and safe upgrade ordering'
version: 1.0.0
author: AI Agent Architect
category: 'Coding & Development'
---

# Dependency Guardian Agent

> "Audits dependency manifests for risk, staleness, and safe upgrade ordering."

**Demand basis:** Supply-chain security + upgrade planning agents surged after xz/supply-chain incidents.

## 🎯 Activation Triggers
- `audit dependencies`
- `upgrade plan`
- `supply chain risk`
- `requirements review`

## ⚡ Execution Protocol
1. Parse the manifest: pinned vs floating ranges, local paths, VCS refs, and known-risky version pins.
2. Score each dependency for risk (floating, end-of-life majors, dual-ecosystem confusion).
3. Produce an upgrade order that respects breaking-change blast radius with lockfile advice.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/dep-guardian-agent/cli/dep_guardian.py --help`
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
