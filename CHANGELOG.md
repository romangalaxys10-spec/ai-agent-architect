# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2.0.0] — 2026-08-28 — "End-to-End Completion"

The framework previously *described* an agent architecture; it now *is* one. This
release closes every gap identified against the six-course master checklist
(proflead, ed-donner, microsoft/Building-AI-Agents-From-Zero-To-Production,
bryanyzhu/agentic-ai-system-course, GeneArnold/AI-Agent-Engineering-Course,
microsoft/ai-agents-for-beginners) plus 2024–2025 SOTA synthesis.

### Added — Core runtime (the framework was missing a real agent loop)
- `core/llm/` — provider abstraction: OpenAI-compatible, Anthropic, offline Echo & Scripted providers; usage/cost metering; model profiles & difficulty-routing cascade; retries with exponential backoff + jitter; circuit breaker; structured output with schema validation + repair loop.
- `core/agent_loop.py` — real ReAct-style loop: native tool calling, parallel tool fan-out, stop conditions (model stop / success predicate / budgets / loop detection / guard trip), transcript + per-turn telemetry.
- `core/reliability.py` — three-currency budgets (steps/tokens/wall-clock, advertised < enforced), loop detector (repetition / stagnation / cycling with canonicalized fingerprints + graduated response ladder), idempotency ledger, per-tool failure policies (compensate / reconcile / refuse), externally-checkable termination criteria.
- `core/context_engineering.py` — compaction (asymmetric reduction, boundary markers, tool-result clipping), structured note-taking with todo recitation, four-block sliding-window assembly with stable prefixes.
- `core/workflows.py` — the five Anthropic workflow patterns as first-class blocks: prompt chaining with gates, routing, parallelization (sectioning + voting), orchestrator-workers, evaluator-optimizer; plus a pattern-selection guide.
- `core/handoffs.py` — OpenAI-SDK-style handoffs: `transfer_to_<agent>` tools, typed inputs, input filters, on_handoff callbacks, audit trail.
- `core/planning.py` — four plan shapes (no-plan / checklist / plan-execute-replan / dependency graph), executor with retry → replan → human escalation ladder, ReAct scaffold for tool-less providers.
- `core/hitl.py` — interrupts with approve/edit/reject/respond decisions, allow/ask/deny approval ruleset with conditional predicates, checkpoint store (the resume button), audit trail, subagent policy inheritance.
- `core/rag.py` — agentic RAG: chunking, vector retrieval as agent tools, Corrective-RAG relevance grading, query rewriting, citation enforcement, agentic write-back.
- `core/mcp.py` — real MCP: JSON-RPC 2.0 server (initialize handshake, capability negotiation, paginated tools/list, tools/call with isError) + client + subprocess stdio transport.

### Added — Protocols, memory, safety, evals, telemetry
- `core/a2a_protocol.py` v2 — Agent Cards (/.well-known/agent-card.json), 7-state task lifecycle with task store, typed Parts/Artifacts, skill-based discovery registry (legacy message bus retained).
- `core/memory.py` v2 — vector store with deterministic offline embeddings, persistence save/load, curation lifecycle (supersede/merge/drop conflict resolution, quarantine for memory-poisoning, rollback, decay pruning), namespaces.
- `core/guardrails.py` v2 — PII detection/masking (email/card/SSN/phone/API keys), output guardrails (secret-leak), tool-argument rails (path traversal, SSRF), untrusted-content delimiting/spotlighting, six trust tiers, OWASP LLM Top-10 checklist.
- `core/evaluation.py` v2 — versioned JSON rubrics, pluggable LLM-as-judge (judge ≠ agent model) incl. comparison mode, trajectory evaluator (tool-call accuracy, redundancy, looping), golden datasets (smoke vs full tiers), regression gating, pass^k consistency; legacy API preserved.
- `core/observability.py` v2 — OTel-compatible span export with correlation IDs and redaction at the trace boundary, JSONL event logger, per-model/per-agent cost ledger, Prometheus-style metrics registry with exposition.

### Fixed — the 12 broken sub-agent CLIs (end-to-end completeness)
- Every agent CLI now runs from **any cwd** (sys.path depth was wrong; import names referenced non-existent underscore packages).
- Syntax errors repaired: `anti-slop-content-engine` (literal newlines in strings), `cold-outreach-dealflow`, `product-launch-orchestrator` (unterminated f-strings).
- Completed the 3 structurally incomplete agents: `senior-architect-agent`, `skill-factory-agent`, `steve-jobs-agent` (core engines + CLIs + importlib-based repo-module loading).

### Added — DevOps & governance
- CI upgraded: syntax compile gate, offline import smoke, Python 3.10–3.12 matrix with coverage, sub-agent CLI end-to-end job, MCP stdio protocol conformance job.
- `Dockerfile` (non-root, offline smoke gate baked in), `Makefile`, `.env.example`.
- `CONTRIBUTING.md`, `SECURITY.md`, this `CHANGELOG.md`.
- `evals/rubrics/` versioned rubric files + golden datasets; `examples/` end-to-end walkthroughs for every new subsystem.

### Tests
- 30 → 183 tests. New coverage: providers/router/retry/breaker, structured output, agent loop (tool calling, HITL approve/edit/reject, budgets, loop detection, success predicates), reliability, context engineering, all 5 workflow patterns, handoffs, planning (retry/replan/escalation), memory (persistence, curation, poisoning), RAG (citations, corrective rewrite), guardrails (PII/SSRF/traversal/delimiting), HITL (rulesets, checkpoints, fail-closed), evals (rubric/trajectory/regression/pass^k), observability (OTel/JSONL/cost/metrics), MCP (handshake/list/call/errors/stdio), A2A (cards/lifecycle/discovery), orchestrator (mesh/blackboard/failure isolation), and the sub-agent completeness contract.

## [1.0.0] — Initial release
- 15 sub-agents hub, depth-skills cognitive engine, Steve Jobs lens, hierarchical memory, tool registry, guardrails, message-bus A2A, orchestrator (2 of 4 topologies), skill factory, 30 tests.
