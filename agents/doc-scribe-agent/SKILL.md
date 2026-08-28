---
name: doc-scribe-agent
description: 'Reverse-engineers living documentation from source: API refs, examples, README blocks'
version: 1.0.0
author: AI Agent Architect
category: 'Coding & Development'
---

# Doc Scribe Agent

> "Reverse-engineers living documentation from source: API refs, examples, README blocks."

**Demand basis:** Documentation generation is a perennial top-5 developer agent ask (docs decay fastest).

## 🎯 Activation Triggers
- `document module`
- `generate API docs`
- `write README section`
- `docstring pass`

## ⚡ Execution Protocol
1. Parse module structure: public/private API surface, signatures, classes, and constants.
2. Generate markdown API reference with param/return tables and a usage example per callable.
3. Flag undocumented public symbols and stale-doc smells (docstring referencing renamed symbol).

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/doc-scribe-agent/cli/doc_scribe.py --help`
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
