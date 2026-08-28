# Changelog

## [2.2.0] - 2026-08-28 — 100 Computer Use Series (315 Total)

### Added — 100 computer/browser/terminal/server control agents
- **Computer Use (22):** computer-vision, desktop-automation, screen-recorder, accessibility-pilot, keyboard-maestro, mouse-precision, clipboard-ops, file-explorer, notification-center, system-prefs, spotlight-search, window-tiling, menubar-tray, screenshot-assert, drag-drop-orchestrator, touch-gesture, ocr-reader, audio-router, camera-mic-governor, power-battery, display-color, input-device
- **Browser Use (22):** browser-pilot, cdp-bridge, playwright-orchestrator, puppeteer-forge, selenium-grid, browser-extension, dom-forensics, web-scraper, form-autofill, cookie-consent, storage-inspector, network-har, performance-audit, accessibility-web, visual-regression, auth-session, download-manager, pdf-renderer, webrtc-media, service-worker, web-security, browser-profile
- **Terminal Use (18):** shell-pilot, pty-bridge, tmux-orchestrator, terminal-renderer, cli-scaffold, prompt-engineer, history-forensics, autocomplete-intel, env-shell, ssh-remote, terminal-recorder, log-tail, job-control, keybinding-doctor, terminal-security, repl-bridge, man-help, shell-benchmark
- **Server Mgmt Linux/macOS/Windows (38):** linux-admin, systemd-surgeon, package-manager, kernel-tuner, network-ops, storage-raid, log-rotation, backup-restore, sec-hardening, container-ops, k8s-pilot, nginx-ops, macos-admin, brew-ops, xcode-ops, macos-security, windows-admin, powershell-forge, winget-choco, windows-security, ad-identity, ci-cd-orchestrator, observability-stack, infra-provisioner, ansible-pilot, tls-cert, db-ops, queue-ops, cdn-edge, incident-ops, cost-ops, compliance-ops, secrets-ops, gitops-pilot, edge-iot, perf-lab, disaster-recovery, migration-ops
- Each: SKILL.md + OS-aware core engine (Linux/macOS/Windows detection, heuristics per domain) + CLI (`--text/--file/--os/--json`, any cwd), `AgentRegistry.discover_agents()` auto-discovers all 315
- Tests: `tests/test_computer100_agents.py` (6 tests), EXPECTED_AGENTS 215→315
- Example: `examples/computer_use_demo.py`

### Changed
- README: badge 215→315, factory 215→315, added “100 Computer Use Series” grouped tables + try-commands, layout 215→315
- agents/AGENTS.md: header 215→315, added 100 series tables
- pyproject description 215→315

### Quality Gates
- All 315 CLIs pass `--help` from neutral cwd; all 315 engines pass `analyze`+`format_report` smoke

---

## [2.1.0] — 2026-08-28

### Added — Top-50 Demand-Driven Agent Suite
- 50 new end-to-end sub-agents covering the most-searched agent categories worldwide:
  Coding & Dev (10), Customer Support (5), Sales & Marketing (7), Research & Analysis (5),
  Personal Productivity (5), Finance (4), HR & Recruiting (4), Content & Creative (4),
  Ops/IT/Security (3), Education/Legal/Life (3).
- Demand basis: 2025–2026 global search & market research (research artifacts in repo history).
- Each agent ships: SKILL.md contract, offline-deterministic core engine, argparse CLI
  (runs from any cwd), and functional smoke tests.
- New test file `tests/test_top50_agents.py` (55 tests: structure, frontmatter, registry
  auto-discovery, CLI execution, per-engine functional assertions).
- `tests/test_subagent_completeness.py` extended from 15 → 65 agents.
- `agents/AGENTS.md` hub catalog extended with the full Top-50 directory.

### Fixed
- SAST Sentinel: SQL-injection rule backreference bug (f-string prefix capture).
- Fact Check / Deep Research: NUM_RE group-extraction crash; corroboration switched to
  overlap coefficient; numeric contradiction detection normalized.
- Resume Screener: capturing-group bug that nulled required-skills extraction.
- Commit Crafter: unterminated subpattern in the breaking-change detector.
- Incident Commander: severity-rule lookup crash on 3-tuples.
- Competitor Radar: plural-form misses on pricing verbs.
- ~15 dataclass field-ordering fixes across new engines (non-default after default).

### Tests
- Suite: 183 → 239 tests, all offline (zero API keys).


All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2.2.0] - 2026-08-28 — 100 Computer Use Series (315 Total)

### Added — 100 computer/browser/terminal/server control agents
- **Computer Use (22):** computer-vision, desktop-automation, screen-recorder, accessibility-pilot, keyboard-maestro, mouse-precision, clipboard-ops, file-explorer, notification-center, system-prefs, spotlight-search, window-tiling, menubar-tray, screenshot-assert, drag-drop-orchestrator, touch-gesture, ocr-reader, audio-router, camera-mic-governor, power-battery, display-color, input-device
- **Browser Use (22):** browser-pilot, cdp-bridge, playwright-orchestrator, puppeteer-forge, selenium-grid, browser-extension, dom-forensics, web-scraper, form-autofill, cookie-consent, storage-inspector, network-har, performance-audit, accessibility-web, visual-regression, auth-session, download-manager, pdf-renderer, webrtc-media, service-worker, web-security, browser-profile
- **Terminal Use (18):** shell-pilot, pty-bridge, tmux-orchestrator, terminal-renderer, cli-scaffold, prompt-engineer, history-forensics, autocomplete-intel, env-shell, ssh-remote, terminal-recorder, log-tail, job-control, keybinding-doctor, terminal-security, repl-bridge, man-help, shell-benchmark
- **Server Mgmt Linux/macOS/Windows (38):** linux-admin, systemd-surgeon, package-manager, kernel-tuner, network-ops, storage-raid, log-rotation, backup-restore, sec-hardening, container-ops, k8s-pilot, nginx-ops, macos-admin, brew-ops, xcode-ops, macos-security, windows-admin, powershell-forge, winget-choco, windows-security, ad-identity, ci-cd-orchestrator, observability-stack, infra-provisioner, ansible-pilot, tls-cert, db-ops, queue-ops, cdn-edge, incident-ops, cost-ops, compliance-ops, secrets-ops, gitops-pilot, edge-iot, perf-lab, disaster-recovery, migration-ops
- Each: SKILL.md + OS-aware core engine (Linux/macOS/Windows detection, heuristics per domain) + CLI (`--text/--file/--os/--json`, any cwd), `AgentRegistry.discover_agents()` auto-discovers all 315
- Tests: `tests/test_computer100_agents.py` (6 tests), EXPECTED_AGENTS 215→315
- Example: `examples/computer_use_demo.py`

### Changed
- README: badge 215→315, factory 215→315, added “100 Computer Use Series” grouped tables + try-commands, layout 215→315
- agents/AGENTS.md: header 215→315, added 100 series tables
- pyproject description 215→315

### Quality Gates
- All 315 CLIs pass `--help` from neutral cwd; all 315 engines pass `analyze`+`format_report` smoke

---

## [2.1.0] - 2026-08-28 — 150 Power Expansion (215 Total)

### Added — 150 new deterministic sub-agents
- **Coding & DevOps (20):** api-architect, perf-surgeon, log-detective, infra-as-code, db-migration, qa-oracle, release-train, feature-flag, chaos-lab, oncall-buddy, sdk-forge, git-historian, code-migration, env-doctor, secrets-vault, build-optimizer, api-mock, licensing-guardian, prompt-ops, agent-eval-harness
- **Data & AI/ML (15):** ml-pipeline, feature-store, model-risk, vector-db-architect, etl-surgeon, dashboard-crafter, anomaly-hunter, forecast-oracle, nlp-pipeline, label-ops, synthetic-data, data-governance, experiment-tracker, rag-architect, agent-memory-architect
- **Security & Compliance (12):** threat-model, pen-test-scribe, soc-triage, privacy-shield, compliance-mapper, red-team, forensics-timeline, identity-governance, supply-chain-guard, crypto-audit, bug-bounty-triage, incident-legal-bridge
- **Sales & Revenue Ops (12):** pricing-strategist, sales-coach, proposal-forge, revenue-ops, churn-prophet, partner-ecosystem, sales-enablement, gong-clone, account-plan, forecast-radar, win-loss-analyst, event-roi
- **Marketing & Growth (13):** growth-loops, influencer-scout, brand-voice, lifecycle-marketer, community-builder, web-analytics, paid-social-surgeon, affiliate-ops, pr-pitch, launch-telemetry, referral-architect, local-seo, video-growth
- **Product & Research (10):** ux-research, roadmap-architect, spec-writer, design-system, user-journey, ab-test-architect, accessibility-auditor, localization-pilot, feedback-miner, jobs-to-be-done
- **Ops/Finance/Legal (12):** procurement-scout, contract-lifecycle, tax-navigator, treasury-ops, audit-trail, vendor-risk, kpi-ledger, okr-coach, meeting-ops, policy-drafter, real-estate-scout, insurance-advisor
- **HR & Talent (8):** talent-sourcer, performance-review, compensation-benchmark, learning-path, workforce-planner, exit-insight, dei-auditor, manager-coach
- **Support & Success (7):** csat-surgeon, knowledge-ops, support-qa, renewal-orchestrator, community-support, nps-driver, self-serve-architect
- **Creator & Media (8):** podcast-producer, newsletter-architect, ugc-curator, meme-ops, press-kit, course-builder, event-producer, creator-monetization
- **Vertical Specialists (13):** healthcare-scribe, legal-ops, proptech-analyst, edtech-coach, fintech-compliance, climate-risk, supply-chain-optimizer, retail-merchandiser, hospitality-ops, manufacturing-qa, energy-ops, gov-procurement, nonprofit-impact
- **Emerging & Agent-Native (10):** autonomous-researcher, eval-judge, tool-smith, orchestration-designer, memory-ops, adversarial-tester, cost-optimizer, skills-librarian, workflow-miner, digital-twin
- **GTM & SMM Power Suite (10):** x-growth-hacker, linkedin-authority, youtube-growth, tiktok-virality, smm-command-center, influencer-ops, social-listening, content-repurposer, community-growth, paid-growth-ops
- Demand basis: synthesis of GitHub trending (awesome-ai-agents 300+), X/LinkedIn/SMM hiring signals, and full course cross-check (proflead/how-to-build-ai-agent, ed-donner/agents, microsoft/Zero-To-Production, bryanyzhu/agentic-ai-system-course, microsoft/ai-agents-for-beginners, GeneArnold/AI-Agent-Engineering-Course)
- Every new agent: **SKILL.md + core engine + CLI + tests** on the same contract (offline, deterministic, stdlib-only), `AgentRegistry.discover_agents()` auto-discovers all 215.

### Changed
- README: Agents Hub badge 15 → 215; new section “150 Power Expansion Suite” with grouped tables and try-commands; project layout count updated; docs cross-linked.
- agents/AGENTS.md: catalog header 65 → 215; added full 150 power suite grouped tables.
- tests/test_subagent_completeness.py: EXPECTED_AGENTS 65 → 215.
- tests/test_power150_agents.py: new contract + functional test suite (6 tests) for the 150.

### Quality Gates
- All 215 CLIs pass `python agents/<slug>/cli/<module>.py --help` from neutral cwd (`/tmp`).
- All 215 engines pass `Engine.analyze(text)` + `format_report` smoke test.
- All SKILL.md frontmatter (name/description/version) parse as valid YAML.

---

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
