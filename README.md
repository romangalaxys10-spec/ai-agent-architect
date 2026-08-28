# 🧠 AI Agent Architect v2.0
### *A Complete, End-to-End Production Agent Framework — From Cognitive Design to Deployed Autonomy*

[![CI](https://github.com/romangalaxys10-spec/ai-agent-architect/actions/workflows/ci.yml/badge.svg)](https://github.com/romangalaxys10-spec/ai-agent-architect/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests: 183 offline](https://img.shields.io/badge/tests-183%20offline-brightgreen.svg)]()
[![Agents Hub: 315 Sub-Agents](https://img.shields.io/badge/Agents%20Hub-315%20Complete%20Agents-brightgreen.svg)]()
[![Zero-Key Runtime](https://img.shields.io/badge/runtime-zero%20API%20keys-success.svg)]()
[![MCP](https://img.shields.io/badge/protocol-MCP%20%2B%20A2A-blueviolet.svg)]()

> **"An AI Agent is not a chatbot with a system prompt. It is an autonomous cognitive engine built with uncompromising taste, radical focus, and resilient architecture — and it must be complete: provider, loop, tools, memory, retrieval, protocols, guardrails, HITL, budgets, evals, telemetry. Anything less is a demo."**

---

## 🌟 What This Is

**AI Agent Architect** is a production-grade agent framework, cognitive engine, and monorepo sub-agent factory. Version 2.0 closes every gap identified against the definitive agent-engineering corpus:

| Reference | What it contributed to this design |
|---|---|
| Anthropic — *Building Effective Agents* | The five workflow patterns, agent-computer interface, tool poka-yoke |
| OpenAI — Agents SDK | Handoffs, guardrails with tripwires, sessions, agents-as-tools |
| Model Context Protocol (MCP) | JSON-RPC server/client, capability negotiation, tool annotations |
| Google A2A / Linux Foundation | Agent Cards, task lifecycle, skill-based discovery |
| Microsoft — *AI Agents for Beginners* + *Zero-to-Production* | Eval tiers (smoke vs full), tool-call accuracy metrics, deployment gates |
| ed-donner — *Master AI Agentic Engineering* | Middleware stack, evaluator loop, MCP-based memory, mock-LLM testing |
| bryanyzhu — *Agentic AI System Course* | Budgets (3 currencies), loop detection, compaction, trust tiers, HITL rulesets |
| GeneArnold — *AI Agent Engineering Course* | Rubric judges, mock-agent testing, JSONL logging, escalation ladders |
| MemGPT/Letta, Manus context research | Memory tiers, KV-cache-aware context assembly, note recitation |

**Everything runs offline with zero API keys** (deterministic Echo/Scripted providers) — then swaps to OpenAI/Anthropic/GLM/local models with one line.

---

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            AGENT RUNTIME (core/)                            │
│                                                                             │
│  ┌──────────────┐   ┌──────────────┐   ┌───────────────────────────────┐   │
│  │ LLM LAYER    │   │ AGENT LOOP   │   │ CONTEXT ENGINEERING           │   │
│  │ providers/   │◄──┤ agent_loop   ├──►│ compaction · notes · window   │   │
│  │ router·retry │   │ ReAct+tools  │   │ stable prefixes (KV-cache)    │   │
│  │ structured   │   │ parallel ✧   │   └───────────────────────────────┘   │
│  └──────────────┘   └──────┬───────┘   ┌───────────────────────────────┐   │
│                            │           │ RELIABILITY KIT                │   │
│  ┌─────────────────────────▼─────────┐ │ budgets(3) · loop detect      │   │
│  │ TOOL REGISTRY                     │ │ idempotency · failure policy  │   │
│  │ schema validation · hooks         │ └───────────────────────────────┘   │
│  │ dry-run · annotations             │ ┌───────────────────────────────┐   │
│  └─────────────────────────┬─────────┘ │ GUARDRAILS + HITL              │   │
│                            │           │ PII · injection · trust tiers  │   │
│  ┌─────────────────────────▼────────┐  │ approve/edit/reject/respond    │   │
│  │ PROTOCOLS                        │  │ checkpoints (resume button)    │   │
│  │ MCP server/client (JSON-RPC)     │  └───────────────────────────────┘   │
│  │ A2A: cards · tasks · discovery   │  ┌───────────────────────────────┐   │
│  │ Orchestrator: 4 topologies       │  │ EVALS + OBSERVABILITY         │   │
│  └──────────────────────────────────┘  │ rubric judge · trajectory      │   │
│  ┌──────────────────────────────────┐  │ golden sets · regression       │   │
│  │ MEMORY + AGENTIC RAG             │  │ OTel spans · JSONL · cost     │   │
│  │ working/episodic/semantic/vector │  └───────────────────────────────┘   │
│  │ curation · quarantine · persist  │                                      │
│  └──────────────────────────────────┘                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌────────────────┐        ┌────────────────┐        ┌────────────────┐
│ PLANNING       │        │ WORKFLOWS      │        │ 15 SUB-AGENTS  │
│ 4 plan shapes  │        │ 5 patterns +   │        │ agents/ hub    │
│ retry→replan→  │        │ evaluator-opt  │        │ SKILL.md+core+ │
│ human ladder   │        │ handoffs       │        │ CLI, all green │
└────────────────┘        └────────────────┘        └────────────────┘
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/romangalaxys10-spec/ai-agent-architect.git
cd ai-agent-architect
pip install -e .

# Zero keys. Zero network. The full stack just runs:
python examples/full_stack_agent.py      # agent loop + RAG + HITL + budgets + evals + OTel
python examples/multi_agent_protocols.py # workflows + handoffs + A2A + MCP

make test                                # 183 tests, offline
```

### Run a real agent loop in 12 lines

```python
from core.llm import EchoProvider                     # or OpenAICompatibleProvider()
from core.agent_loop import AgentLoop
from core.tool_registry import ToolRegistry

registry = ToolRegistry()
registry.register("add", "Add two numbers", lambda a, b: a + b,
                  parameters_schema={"type": "object",
                                     "properties": {"a": {"type": "number"},
                                                    "b": {"type": "number"}},
                                     "required": ["a", "b"]})

result = AgentLoop(provider=EchoProvider(), registry=registry).run("compute 2+3")
print(result.stop_reason, result.total_tokens, result.final_answer)
```

### Serve your tools over MCP

```python
from core.mcp import MCPServer, MCPClient

server = MCPServer(registry)          # JSON-RPC 2.0: initialize/tools/list/tools/call
client = MCPClient(server)
client.connect()
tools = client.list_tools()
result = client.call_tool("add", {"a": 2, "b": 3})
```

### Expose an agent over A2A

```python
from core.a2a_protocol import AgentCard, A2AParticipant, A2ADiscovery, AgentSkill

card = AgentCard(name="research-agent", description="Deep research",
                 url="https://agents.internal/research",
                 skills=[AgentSkill(id="r", name="research", description="web research",
                                    tags=["research"])])
discovery = A2ADiscovery()
discovery.register(A2AParticipant(card, handler=lambda task: {"sources": [...]}))
matches = discovery.find_by_skill("research")   # skill-based discovery
```

### Switch to live models

```python
from core.llm import create_provider
provider = create_provider("openai")            # reads OPENAI_API_KEY / OPENAI_BASE_URL
# or: create_provider("anthropic")
# or route cheap→flagship automatically:
from core.llm import ModelRouter, EchoProvider
router = ModelRouter(provider, small_model="gpt-4o-mini", flagship_model="gpt-4o")
```

---

## 🧠 Cognitive Depth: Powered by Depth-Skills

Traditional models suffer from **Premature Closure** and **Pattern Gravity**. This framework embeds the 19 cognitive protocols from [`depth-skills`](https://github.com/Kshitijpalsinghtomar/depth-skills) — CONDUCTOR (complexity orchestration), DEEP-THINK (tri-angle activation), ADVERSARY (self-opposition), DIVERGE (contrarian paths), EXCAVATE (assumption archaeology), TEMPORAL (Day 1 vs Year 1) — wired into the master engine lifecycle and every sub-agent.

---

## 🏭 Agents Factory: 315 Complete Sub-Agents (15 Founding + 50 Demand Suite + 150 Power Expansion + 100 Computer Use)

Every agent ships **SKILL.md + core engine + CLI + tests** (enforced by `tests/test_subagent_completeness.py`, including a run-from-any-cwd contract). **315 total = 15 founding + 50 demand suite + 150 power expansion + 100 computer/browser/terminal/server.**

| # | Agent | Domain |
|---|-------|--------|
| 1 | 🧠 `depth-conductor-agent` | Metacognition, anti-premature-closure audits |
| 2 | 🎨 `superdesign-agent` | Anti-AI-Slop design engine (sites, decks, HUDs) |
| 3 | 🍏 `steve-jobs-agent` | Focus filter, Rule of Three, binary verdicts |
| 4 | ⚡ `solana-stream-sentinel` | Yellowstone gRPC sniffer, DLMM decoder, MEV sim |
| 5 | 🛡️ `binary-reverse-sentinel` | Mach-O/iOS security scanner, credential hunter |
| 6 | 🎯 `linkedin-intent-sniper` | B2B buying-intent analysis, outreach |
| 7 | 🛰️ `discord-community-radar` | Dev-feed scanning, gig detection |
| 8 | ✍️ `anti-slop-content-engine` | Viral X threads, LinkedIn case studies |
| 9 | 🚀 `product-launch-orchestrator` | Show HN / PH / Reddit launch campaigns |
| 10 | 📬 `cold-outreach-dealflow` | Deliverability-safe email sequences, SOWs |
| 11 | 🎯 `career-hunter-orchestrator` | Job scout, ATS resumes, cover letters, CRM |
| 12 | 🧠 `model-bridge-router` | Multi-model routing, schema translation |
| 13 | 🧾 `invoice-billing-sentinel` | Multi-currency invoicing, timesheets |
| 14 | 🏛️ `senior-architect-agent` | Cognitive DAG decomposition, anti-pattern review |
| 15 | 🏭 `skill-factory-agent` | SKILL.md scaffolding, packaging, linting |

```bash
python cli/architect.py list-agents                    # browse the hub
python agents/depth-conductor-agent/cli/conductor.py --query "architect a DEX indexer"
python agents/senior-architect-agent/cli/architect.py --requirement "build an agent" --name Sys
python agents/skill-factory-agent/cli/factory.py lint --root .   # audit every SKILL.md
```

---

## 🛡️ Production Safety Stack

- **Budgets**: three non-convertible currencies (steps / tokens / wall-clock), *advertised to the model* (it paces itself) with a hard enforced ceiling as backstop.
- **Loop detection**: repetition / stagnation / cycling via canonicalized tool-call fingerprints (volatile keys stripped) with a graduated Inform → Constrain → Escalate ladder.
- **Guardrails**: input injection patterns, PII masking (email/card/SSN/phone/keys), output secret-leak blocking, tool-argument path-traversal & SSRF heuristics, untrusted-content delimiting, six trust tiers, OWASP LLM Top-10 checklist.
- **HITL**: allow/ask/deny rulesets with conditional predicates, approve/edit/reject/respond decisions, checkpoint store for resume, audit trail, fail-closed defaults.
- **Failure policies per tool**: compensate / reconcile / refuse — irreversible actions never auto-retry.
- **Idempotency ledger**: side-effecting calls replay cached results instead of double-firing.

## 📊 Evals & Observability

```python
from core.evaluation import AgentEvaluator, LLMAsJudge, GoldenDataset, RegressionGate, pass_at_k

report = AgentEvaluator.evaluate_run(agent_name="a", goal="g", final_output=..., turns=...,
                                     latency_ms=..., total_cost_usd=...)
# rubric judge + trajectory eval + deterministic checks → PRODUCTION_READY / NEEDS_REFINEMENT / FAILED
# evals/rubrics/*.json — versioned rubrics; evals/golden/ — smoke (every deploy) vs full (nightly)
```

```python
from core.observability import TelemetryTracer, JSONLLogger, CostLedger

tracer = TelemetryTracer("run")            # OTel-compatible export + PII redaction
logger = JSONLLogger("events.jsonl")        # structured events: llm_call/tool_call/hitl/guardrail
ledger = CostLedger()                      # per-model / per-agent USD accounting
```

---

## 📦 Project Layout

```
core/
├── llm/                    # providers, model router, retry+circuit breaker, structured output
├── agent_loop.py           # THE agent loop: tools, HITL, budgets, loop detection, stop conditions
├── workflows.py            # 5 Anthropic patterns (chain/route/parallel/orch/eval-opt)
├── handoffs.py             # transfer_to_X tools, input filters, audit trail
├── planning.py             # 4 plan shapes, retry→replan→human ladder, ReAct scaffold
├── reliability.py          # 3-currency budgets, loop detector, idempotency, failure policies
├── context_engineering.py  # compaction, note recitation, 4-block window
├── memory.py               # working/episodic/semantic + vector store + curation
├── rag.py                  # agentic RAG: retrieval tools, corrective grading, citations
├── guardrails.py           # PII, injection, trust tiers, delimiting, OWASP checklist
├── hitl.py                 # interrupts, approval rulesets, checkpoints
├── evaluation.py           # rubric judge, trajectory evals, golden sets, regression, pass^k
├── observability.py        # OTel spans, JSONL events, cost ledger, metrics
├── mcp.py                  # MCP JSON-RPC server + client + stdio transport
├── a2a_protocol.py         # Agent Cards, task lifecycle, discovery, message bus
├── orchestrator.py         # hierarchical / pipeline / mesh / blackboard
├── tool_registry.py        # schemas, validation pipeline, hooks, annotations
├── depth_cognitive_engine.py · steve_jobs_lens.py · engine.py · registry.py
agents/                     # 315 complete sub-agents (SKILL.md + core + cli)
factory/                    # skill builder, prompt synthesizer
evals/                      # versioned rubrics + golden datasets
examples/                   # end-to-end walkthroughs
tests/                      # 183 tests — all offline
docs/                       # compendium, patterns, product DNA, skill factory spec
```

## 🌍 Top-50 Demand-Driven Agent Suite (2026)

The 50 most-wanted, highest-searched agent capabilities — researched from global 2025–2026 demand data
(coding agents #1 search class, support automation = largest enterprise spend, sales agents $3.25B @ 44.7% CAGR,
deep research = fastest-growing term) — now shipped as first-class sub-agents:

**Coding & Dev (10)** · code-review-sentinel, test-forge-agent, bug-triage-agent, ci-surgeon-agent, refactor-pilot-agent, doc-scribe-agent, sast-sentinel-agent, dep-guardian-agent, migration-planner-agent, commit-crafter-agent

**Customer Support (5)** · ticket-router-agent, kb-curator-agent, escalation-shield-agent, voice-of-customer-agent, sla-sentinel-agent

**Sales & Marketing (7)** · lead-qualifier-agent, outreach-personalizer-agent, meeting-brief-agent, crm-hygiene-agent, competitor-radar-agent, seo-content-strategist-agent, ad-campaign-optimizer-agent

**Research & Analysis (5)** · deep-research-agent, data-analyst-agent, fact-check-agent, market-scout-agent, literature-review-agent

**Personal Productivity (5)** · email-triage-agent, calendar-architect-agent, meeting-scribe-agent, trip-compass-agent, deal-hunter-agent

**Finance (4)** · invoice-intake-agent, expense-auditor-agent, finstat-analyst-agent, portfolio-scout-agent

**HR & Recruiting (4)** · resume-screener-agent, interview-coach-agent, onboarding-guide-agent, culture-pulse-agent

**Content & Creative (4)** · content-calendar-agent, script-writer-agent, social-media-manager-agent, copy-editor-agent

**Ops, IT & Security (3)** · cloud-cost-optimizer-agent, incident-commander-agent, access-review-agent

**Education, Legal & Life (3)** · socratic-tutor-agent, language-coach-agent, contract-reviewer-agent

Every agent: offline-deterministic engine, argparse CLI (runs from any cwd), SKILL.md contract, and
functional smoke tests. Full catalog with per-agent tables: [`agents/AGENTS.md`](agents/AGENTS.md).
Test suite: `python -m pytest tests/test_top50_agents.py` (56 tests).

```bash
# try one:
python agents/sast-sentinel-agent/cli/sast_sentinel.py --code 'cursor.execute(f"SELECT * FROM t WHERE id={uid}")'
```


## 🚀 150 Power Expansion Suite (Global Demand + X / LinkedIn / SMM Research)

*Beyond the founding 15 + Top-50, this expansion adds 150 high-demand agents synthesized from worldwide 2025–2026 research: GitHub trending (awesome-ai-agents 300+ resources), X/LinkedIn hiring signals, SMM growth playbooks, and full cross-check against 6 canonical courses (Google ADK / ed-donner / Microsoft Zero-to-Production / bryanyzhu Agentic Systems / Microsoft AI Agents for Beginners / GeneArnold Agent Engineering). Every agent: offline deterministic engine, CLI from any cwd, SKILL.md contract.*

Full catalog with per-agent tables: [`agents/AGENTS.md`](agents/AGENTS.md). Every agent is discoverable via `AgentRegistry.discover_agents()` and the CLI hub.

### Coding & DevOps (20)
| Agent | What it does |
|---|---|
| `api-architect-agent` | Designs REST/GraphQL/gRPC APIs with OpenAPI specs, versioning, and contract tests |
| `perf-surgeon-agent` | Bottleneck detection, flame-graph interpretation, latency budgets, and perf regression gates |
| `log-detective-agent` | Structured log aggregation, anomaly detection, distributed trace stitching, alert synthesis |
| `infra-as-code-agent` | Terraform/Pulumi generation, drift detection, env parity checks, plan review |
| `db-migration-agent` | Schema diff, zero-downtime migration plans, rollback scripts, data backfill verification |
| `qa-oracle-agent` | Test plan matrices, edge-case enumeration, risk-based test prioritization, flaky test triage |
| `release-train-agent` | Cut branches, changelog collation, semver enforcement, rollout & feature-flag coordination |
| `feature-flag-agent` | Flag lifecycle, targeting rules, kill-switch runbooks, experiment exposure auditing |
| `chaos-lab-agent` | Fault injection plans, blast-radius scoping, steady-state hypotheses, game-day runbooks |
| `oncall-buddy-agent` | Runbook retrieval, escalation routing, post-page context assembly, handoff summaries |
| `sdk-forge-agent` | Multi-language SDK scaffolding from OpenAPI/Proto, versioned changelogs, breaking-change detection |
| `git-historian-agent` | Blame forensics, bisect automation, contributor graphs, tech-debt timeline mapping |
| `code-migration-agent` | Language/framework translation plans with semantic equivalence checks and test scaffolding |
| `env-doctor-agent` | Repro pass/fail for .env, Docker, Node/Python version mismatches, setup script generation |
| `secrets-vault-agent` | Hardcoded secret scan beyond SAST, rotation schedules, least-privilege env config mapping |
| `build-optimizer-agent` | Bundle-size audit, tree-shake analysis, cache-hit maximization, CI minute reduction |
| `api-mock-agent` | Deterministic mocks from OpenAPI, Pact contracts, stub servers, fake-data factories |
| `licensing-guardian-agent` | OSS license compatibility, copyleft risk, SBOM generation, attribution assembly |
| `prompt-ops-agent` | Prompt versioning, regression evals, few-shot curation, token-cost vs quality tradeoffs |
| `agent-eval-harness-agent` | Trajectory scoring, tool-use accuracy, golden-set curation, pass@k gating |

### Data & AI/ML (15)
| Agent | What it does |
|---|---|
| `ml-pipeline-agent` | Feature store wiring, training DAG authoring, eval gates, model registry lifecycle |
| `feature-store-agent` | Feature drift detection, leakage checks, importance ranking, store backfill plans |
| `model-risk-agent` | Bias/fairness audits, SHAP-style attribution summaries, challenger-model comparison, MRM reports |
| `vector-db-architect-agent` | Index selection (HNSW/IVF), chunking strategy, ANN recall benchmarking, hybrid search tuning |
| `etl-surgeon-agent` | Pipeline lineage mapping, idempotency checks, late-arriving data handling, cost-per-GB optimization |
| `dashboard-crafter-agent` | KPI tree design, chart selection logic, SQL generation, stakeholder-ready narrative framing |
| `anomaly-hunter-agent` | Time-series outlier detection, seasonal decomposition, root-cause ranking, alert suppression tuning |
| `forecast-oracle-agent` | Horizon selection, Prophet/ARIMA-style heuristics, confidence intervals, scenario modeling |
| `nlp-pipeline-agent` | Tokenization choices, NER/CLS routing, eval on imbalanced sets, multilingual tradeoffs |
| `label-ops-agent` | Label schema design, IAA measurement, active-learning queue prioritization, QA sampling plans |
| `synthetic-data-agent` | Privacy-preserving synthetic generation, fidelity metrics, bias preservation checks |
| `data-governance-agent` | PII discovery, retention policy mapping, lineage cataloging, access-tier enforcement |
| `experiment-tracker-agent` | Run comparison matrices, hyperparam importance, early-stopping verdicts, reproducibility checklists |
| `rag-architect-agent` | Chunking/embedding model selection, retrieval grading, citation grounding, hallucination rate measurement |
| `agent-memory-architect-agent` | Working/episodic/semantic tier design, compaction triggers, retrieval policy tuning |

### Security & Compliance (12)
| Agent | What it does |
|---|---|
| `threat-model-agent` | STRIDE mapping, attack-tree enumeration, mitigations ranked by risk-to-cost |
| `pen-test-scribe-agent` | Finding deduplication, CVSS scoring, evidence packets, remediation roadmaps |
| `soc-triage-agent` | Alert correlation, false-positive suppression, playbook dispatch, MTTR estimation |
| `privacy-shield-agent` | GDPR/CCPA gap analysis, DPA clause mapping, consent-flow audits, retention enforcement |
| `compliance-mapper-agent` | SOC2/ISO27001/HIPAA control mapping, evidence collection checklists, gap heatmaps |
| `red-team-agent` | Jailbreak prompt generation, guardrail bypass attempts, safety eval reporting |
| `forensics-timeline-agent` | Artifact correlation, chain-of-custody logging, timeline reconstruction |
| `identity-governance-agent` | SoD conflict detection, certification campaign planning, orphaned account hunting |
| `supply-chain-guard-agent` | Dependency provenance, sigstore verification, typosquat detection, SBOM diffing |
| `crypto-audit-agent` | Primitive misuse detection, key-length enforcement, rotation hygiene scoring |
| `bug-bounty-triage-agent` | Report deduplication, reproducibility checks, severity re-grading, payout band mapping |
| `incident-legal-bridge-agent` | Breach classification, notification timeline, regulator mapping, disclosure draft generation |

### Sales & Revenue Ops (12)
| Agent | What it does |
|---|---|
| `pricing-strategist-agent` | Willingness-to-pay modeling, packaging tiers, discount guardrails, expansion triggers |
| `sales-coach-agent` | MEDDICC gap analysis, talk-time metrics, objection handling plays, next-step enforcement |
| `proposal-forge-agent` | RFP shredding, win-theme mapping, compliance matrix, proposal narrative assembly |
| `revenue-ops-agent` | Funnel stage conversion, forecast hygiene, territory balancing, comp-plan alignment |
| `churn-prophet-agent` | Health scoring, leading-indicator ranking, save-play matching, expansion risk flagging |
| `partner-ecosystem-agent` | Partner-fit scoring, co-sell motion design, referral tracking, enablement gap analysis |
| `sales-enablement-agent` | Battlecard freshness, asset-to-stage mapping, rep ramp checklists, content gap closure |
| `gong-clone-agent` | Call transcript themes, competitor mention tracking, coaching moment extraction |
| `account-plan-agent` | Org chart mapping, whitespace analysis, multi-threading plan, executive briefing pack |
| `forecast-radar-agent` | Pipeline coverage math, stage-weighted forecast, risk-adjusted commit calls |
| `win-loss-analyst-agent` | Interview synthesis, loss-reason taxonomy, competitive loss attribution, fix-backlog routing |
| `event-roi-agent` | Event cost capture, lead-to-opportunity math, follow-up SLA enforcement, repeat/skip verdict |

### Marketing & Growth (13)
| Agent | What it does |
|---|---|
| `growth-loops-agent` | Loop mapping (acquisition/retention/monetization), unit economics, experiment backlog |
| `influencer-scout-agent` | Audience overlap scoring, authenticity checks, brief generation, performance attribution |
| `brand-voice-agent` | Tone taxonomy enforcement, off-brand flagging, rewrite suggestions with voice preservation |
| `lifecycle-marketer-agent` | Journey mapping, trigger logic, send-time optimization, deliverability linting |
| `community-builder-agent` | Channel health scoring, contributor ladder design, moderation playbooks, activation campaigns |
| `web-analytics-agent` | Funnel drop analysis, cohort retention curves, attribution model comparison |
| `paid-social-surgeon-agent` | Creative fatigue detection, audience saturation scoring, bid strategy tuning |
| `affiliate-ops-agent` | Payout integrity, fraud heuristics, creative freshness scoring, partner tiering |
| `pr-pitch-agent` | Angle generation, journalist-fit scoring, embargo timing, follow-up sequencing |
| `launch-telemetry-agent` | Pre/post metric deltas, sentiment shift, source attribution, repeat-launch playbook |
| `referral-architect-agent` | Incentive design, viral coefficient math, fraud controls, share-copy generation |
| `local-seo-agent` | NAP consistency audit, review velocity tracking, GMB optimization checklist |
| `video-growth-agent` | Hook scoring, retention-curve analysis, thumbnail/title A/B planning, platform cutdowns |

### Product & Research (10)
| Agent | What it does |
|---|---|
| `ux-research-agent` | Interview coding, affinity mapping, insight prioritization, JTBD extraction |
| `roadmap-architect-agent` | RICE/WSJF scoring, dependency mapping, theme balancing, stakeholder narrative |
| `spec-writer-agent` | Requirement decomposition, acceptance criteria authoring, edge-case enumeration, open-question tracking |
| `design-system-agent` | Token hygiene, component API consistency, Figma drift detection, adoption metrics |
| `user-journey-agent` | Touchpoint mapping, emotion curves, pain-point severity ranking, opportunity sizing |
| `ab-test-architect-agent` | Hypothesis framing, sample-size math, guardrail metrics, ship/hold/iterate verdicts |
| `accessibility-auditor-agent` | WCAG 2.2 checks, screen-reader flow testing, color contrast math, remediation priority |
| `localization-pilot-agent` | String externalization, pseudo-locale testing, cultural adaptation flags, TM leverage scoring |
| `feedback-miner-agent` | Support/survey/app-review clustering, theme-to-roadmap linking, fix prioritization |
| `jobs-to-be-done-agent` | Job statement extraction, switch-moment mapping, competing-solution analysis |

### Ops, Finance & Legal (12)
| Agent | What it does |
|---|---|
| `procurement-scout-agent` | Vendor comparison matrices, TCO modeling, negotiation leverage mapping, renewal risk flags |
| `contract-lifecycle-agent` | Obligation extraction, renewal/deadline tracking, clause deviation flagging |
| `tax-navigator-agent` | Jurisdiction mapping, nexus flagging, filing deadline calendar, risk-ranked action list (not advice) |
| `treasury-ops-agent` | Cash positioning, bank fee audit, FX exposure flagging, liquidity runway math |
| `audit-trail-agent` | Evidence packet assembly, control-to-artifact mapping, auditor-ready narratives |
| `vendor-risk-agent` | Risk tiering, questionnaire gap analysis, mitigation plan generation |
| `kpi-ledger-agent` | North-star decomposition, metric ownership, anomaly alerts, board-ready rollups |
| `okr-coach-agent` | Objective quality scoring, key-result measurability checks, alignment mapping, retrospective synthesis |
| `meeting-ops-agent` | Meeting load analysis, purpose/attendee pruning, async-shift recommendations |
| `policy-drafter-agent` | Policy structure generation, control mapping, exception workflow, review cadence design |
| `real-estate-scout-agent` | Location scoring, comps analysis, cap-rate math, due-diligence checklist |
| `insurance-advisor-agent` | Gap analysis, limit adequacy, exclusion flagging, renewal negotiation prep (not advice) |

### HR & Talent (8)
| Agent | What it does |
|---|---|
| `talent-sourcer-agent` | Boolean search construction, profile-fit scoring, outreach personalization, pipeline health tracking |
| `performance-review-agent` | Feedback theme synthesis, calibration support, growth-plan drafting, bias flagging |
| `compensation-benchmark-agent` | Band mapping, market percentile analysis, pay-equity flags, offer construction (not advice) |
| `learning-path-agent` | Skill-gap mapping, curriculum sequencing, adaptive checkpoint design, certification prep |
| `workforce-planner-agent` | Capacity modeling, hiring plan phasing, attrition risk flags, org design options |
| `exit-insight-agent` | Departure theme extraction, regretted vs non-regretted loss, retention lever mapping |
| `dei-auditor-agent` | Pipeline diversity metrics, language inclusivity audit, intervention effectiveness scoring |
| `manager-coach-agent` | 1:1 agenda generation, coaching prompt synthesis, team health diagnostics |

### Support & Success (7)
| Agent | What it does |
|---|---|
| `csat-surgeon-agent` | Driver analysis, recovery playbooks, closed-loop tracking, segment trending |
| `knowledge-ops-agent` | Article performance vs ticket deflection, freshness SLA, AI-assist readiness scoring |
| `support-qa-agent` | Interaction scoring against rubric, coaching themes, calibration packet assembly |
| `renewal-orchestrator-agent` | Health-triggered playbooks, commercial term tracking, risk-adjusted renewal forecast |
| `community-support-agent` | Forum post classification, crowdsourced answer scoring, escalation to KB creation |
| `nps-driver-agent` | Promoter/passive/detractor drivers, closed-loop prioritization, exec narrative |
| `self-serve-architect-agent` | Deflection opportunity scoring, flow design, containment rate tracking |

### Creator & Media (8)
| Agent | What it does |
|---|---|
| `podcast-producer-agent` | Episode arcs, show-note generation, guest research packs, distribution checklist |
| `newsletter-architect-agent` | Section planning, curation scoring, subject-A/B generation, send-time optimization |
| `ugc-curator-agent` | Submission triage, rights management, creator attribution, repurposing queue |
| `meme-ops-agent` | Trend velocity scoring, format-body fit, timing windows, brand-safety gates |
| `press-kit-agent` | Boilerplate synthesis, asset inventory, embargo packet, media Q&A prep |
| `course-builder-agent` | Learning objective mapping, module sequencing, assessment design, completion analytics |
| `event-producer-agent` | Run-of-show authoring, speaker/venue logistics, contingency branches, post-event retro |
| `creator-monetization-agent` | Revenue stream mapping, tier pricing, sponsor-fit scoring, payout optimization |

### Vertical Specialists (13)
| Agent | What it does |
|---|---|
| `healthcare-scribe-agent` | SOAP note structuring, code suggestion, compliance flagging (not medical advice) |
| `legal-ops-agent` | Matter intake, outside-counsel spend tracking, playbook compliance, ebilling audit |
| `proptech-analyst-agent` | Rent-roll parsing, valuation sensitivity, zoning flag checks, investment memo drafting |
| `edtech-coach-agent` | Curriculum alignment, Bloom-level tagging, assignment feedback scaffolding |
| `fintech-compliance-agent` | KYC/AML flow checks, transaction monitoring flag review, regulatory mapping |
| `climate-risk-agent` | Physical/transition risk scoring, disclosure mapping (TCFD/ISSB), mitigation ranking |
| `supply-chain-optimizer-agent` | Demand forecast reconciliation, inventory policy, route optimization, disruption playbooks |
| `retail-merchandiser-agent` | Assortment planning, markdown optimization, planogram compliance, sell-through analysis |
| `hospitality-ops-agent` | Occupancy pacing, upsell triggers, staffing-to-demand matching, guest recovery workflows |
| `manufacturing-qa-agent` | SPC chart interpretation, defect Pareto, CAPA tracking, traceability mapping |
| `energy-ops-agent` | Load forecasting, tariff optimization, curtailment planning, carbon accounting |
| `gov-procurement-agent` | RFP eligibility checks, compliance matrix, proposal choreography for public sector |
| `nonprofit-impact-agent` | Theory-of-change mapping, outcome metric design, grant reporting packet assembly |

### Emerging & Agent-Native (10)
| Agent | What it does |
|---|---|
| `autonomous-researcher-agent` | Hypothesis generation, experiment planning, lit-review synthesis, preprint monitoring |
| `eval-judge-agent` | Rubric authoring, LLM-as-judge calibration, inter-rater agreement scoring, golden-set expansion |
| `tool-smith-agent` | Tool schema design, validation harness, mock-server generation, version migration planning |
| `orchestration-designer-agent` | Topology selection (hierarchical/mesh/blackboard), handoff choreography, failure-mode mapping |
| `memory-ops-agent` | Memory tier health, compaction trigger tuning, recall precision measurement, curation backlog |
| `adversarial-tester-agent` | Red-team prompt banks, bypass attempt logging, safety regression tracking |
| `cost-optimizer-agent` | Token/latency Pareto frontier, model routing policy, cache-hit maximization |
| `skills-librarian-agent` | Skill discovery indexing, reuse scoring, deprecation planning, marketplace curation |
| `workflow-miner-agent` | Process mining from logs, variant analysis, automation opportunity ranking |
| `digital-twin-agent` | State-sync design, simulation scenario authoring, drift detection, what-if analysis |

### GTM & SMM Power Suite (10)
| Agent | What it does |
|---|---|
| `x-growth-hacker-agent` | Viral hook engineering, thread pacing, reply-guy strategy, algorithmic timing optimization |
| `linkedin-authority-agent` | POV extraction from commits, carousel outlining, comment-to-DM funnel, SSI scoring |
| `youtube-growth-agent` | Title/thumbnail scoring, retention editing, chapter optimization, cross-platform repurposing |
| `tiktok-virality-agent` | Hook-window optimization, trend-jacking timing, sound selection, loop-rate engineering |
| `smm-command-center-agent` | Cross-platform calendar, asset variant generation, performance rollup, crisis monitoring |
| `influencer-ops-agent` | Brief generation, deliverable tracking, usage-rights ledger, payout reconciliation |
| `social-listening-agent` | Mention clustering, sentiment velocity, crisis early-warning, competitor share-of-voice |
| `content-repurposer-agent` | Long-form -> thread/carousel/shorts atomization, platform-native rewriting, CTA tailoring |
| `community-growth-agent` | Activation funnel, referral loop design, moderation at scale, UGC flywheel |
| `paid-growth-ops-agent` | Channel mix modeling, CAC payback math, creative fatigue rotation, incrementality testing |

```bash
# try any of the 150:
python agents/api-architect-agent/cli/api_architect.py --text "Design a rate-limited REST API for billing"
python agents/x-growth-hacker-agent/cli/x_growth_hacker.py --text "Draft a viral thread about our launch"
python agents/threat-model-agent/cli/threat_model.py --text "STRIDE for a multi-tenant agent gateway"
```


## 🖥️ 100 Computer Use Series — Browser / Terminal / OS / Server Automation (Linux · macOS · Windows)

*100 deterministic control & automation agents — the missing computer-use layer. Covers desktop GUI + accessibility, headless/browser CDP, terminal/PTY/shell, and cross-platform server engineering (systemd, launchd, services.msc, k8s, containers, DB, queues, TLS, GitOps). Every agent: offline, OS-aware heuristics, CLI from any cwd.*

Full catalog: [`agents/AGENTS.md`](agents/AGENTS.md). Discoverable via `AgentRegistry.discover_agents()`.

### Computer Use (22)
| Agent | What it does |
|---|---|
| `computer-vision-agent` | GUI element detection, screenshot grounding, coordinate resolution, and vision-to-action translation |
| `desktop-automation-agent` | Cross-app desktop workflows, window management, dock/taskbar control, and macro recording |
| `screen-recorder-agent` | Session capture, action trace diffing, deterministic replay, and flake diagnosis |
| `accessibility-pilot-agent` | AX tree traversal, VoiceOver/Narrator/Orca mapping, label-role audits, and a11y-driven control |
| `keyboard-maestro-agent` | Hotkey choreography, chord sequencing, input method switching, and shortcut conflict resolution |
| `mouse-precision-agent` | DPI-aware moves, drag semantics, hover intent, and pixel-perfect assertion |
| `clipboard-ops-agent` | Multi-format clipboard (text/image/files), history vault, and cross-app paste validation |
| `file-explorer-agent` | Finder/Explorer/Nautilus navigation, batch rename, quick-look preview, and breadcrumb forensics |
| `notification-center-agent` | Banner/toast interception, permission routing, Do-Not-Disturb orchestration, and alert triage |
| `system-prefs-agent` | Settings search, plist/registry diffing, profile provisioning, and drift enforcement |
| `spotlight-search-agent` | Indexed search, intent disambiguation, quick-open ranking, and recent-items forensics |
| `window-tiling-agent` | Tiling layout synthesis, focus follows mouse, workspace assignment, and multi-monitor mapping |
| `menubar-tray-agent` | Status item orchestration, menu introspection, tray icon health checks |
| `screenshot-assert-agent` | Visual diff, perceptual hash, region masking, and golden screenshot gates |
| `drag-drop-orchestrator-agent` | Cross-app drag semantics, payload validation, drop-zone mapping, and undo safety |
| `touch-gesture-agent` | Trackpad/phone gestures, palm rejection, pressure curves, and haptic feedback mapping |
| `ocr-reader-agent` | On-screen text extraction, table de-warping, language detection, and redaction |
| `audio-router-agent` | Input/output device switching, volume ducking, mic gate, and audio capture routing |
| `camera-mic-governor-agent` | Permission gates, virtual camera/mic injection, and recording indicator enforcement |
| `power-battery-agent` | Sleep/wake orchestration, battery health, thermal throttling, and charge-limit policies |
| `display-color-agent` | Resolution/refresh switching, HDR/color profile validation, and night-shift scheduling |
| `input-device-agent` | Keyboard/mouse/gamepad pairing, driver health, DPI/remap sync, and latency checks |

### Browser Use (22)
| Agent | What it does |
|---|---|
| `browser-pilot-agent` | Tab orchestration, navigation guards, history/cookie/session control, and profile isolation |
| `cdp-bridge-agent` | Chrome DevTools Protocol — DOM, debugger, network, emulation, and trace capture |
| `playwright-orchestrator-agent` | Cross-browser (Chromium/Firefox/WebKit) test generation, auto-wait, trace viewer |
| `puppeteer-forge-agent` | Headless Chromium control, PDF/screenshot pipelines, and request interception |
| `selenium-grid-agent` | Hub/node scaling, capability matching, grid health, and flaky quarantine |
| `browser-extension-agent` | Manifest v3, content/background/service worker, storage sync, and store review prep |
| `dom-forensics-agent` | Selector resilience scoring, shadow-DOM piercing, hydration mismatch detection |
| `web-scraper-agent` | Polite crawling, robots.txt respect, anti-bot evasion planning, and dataset diffing |
| `form-autofill-agent` | Field inference, constraint validation, CAPTCHA/Turnstile routing, and submit guards |
| `cookie-consent-agent` | CMP banner classification, preference persistence, and consent-string validation |
| `storage-inspector-agent` | LocalStorage/SessionStorage/IndexedDB/cookies audit, quota sizing, and eviction forensics |
| `network-har-agent` | HAR capture, waterfall analysis, cache-hit verification, and payload PII scrubbing |
| `performance-audit-agent` | Lighthouse/Web Vitals, CLS/LCP/INP budgets, bundle waterfall, and perf regression gates |
| `accessibility-web-agent` | axe-core style audits, keyboard trap detection, color contrast, and screen-reader order |
| `visual-regression-agent` | Cross-viewport screenshot diff, layout shift masking, anti-alias tolerance |
| `auth-session-agent` | Login flows, OAuth/PKCE, MFA/TOTP, session refresh, and token theft guards |
| `download-manager-agent` | Download orchestration, virus-scan hooks, checksum verification, and resume safety |
| `pdf-renderer-agent` | HTML→PDF fidelity, print media CSS, pagination orphans, and PDF/A validation |
| `webrtc-media-agent` | Peer connection forensics, ICE candidate mapping, bandwidth/echo diagnostics |
| `service-worker-agent` | Cache strategy, offline fallback, update lifecycle, and push subscription forensics |
| `web-security-agent` | CSP/HSTS/XFO audit, mixed-content detection, and SRI/subresource integrity checks |
| `browser-profile-agent` | Profile cloning, fingerprint hygiene, proxy rotation, and container isolation |

### Terminal Use (18)
| Agent | What it does |
|---|---|
| `shell-pilot-agent` | POSIX shell orchestration (bash/zsh/fish), prompt detection, and exit-code triage |
| `pty-bridge-agent` | Pseudo-terminal allocation, raw mode, echo suppression, and resize propagation |
| `tmux-orchestrator-agent` | Session/window/pane topology, layout persistence, and copy-mode automation |
| `terminal-renderer-agent` | ANSI/VT100 parsing, 24-bit color, ligature handling, and damage-region rendering |
| `cli-scaffold-agent` | Argparse/cobra/clap scaffolding, help/usage consistency, and shell completion generation |
| `prompt-engineer-agent` | Terminal prompt theme (starship/oh-my-zsh), git status embedding, and latency budgets |
| `history-forensics-agent` | Shell history forensics, deduplication, secret scrubbing, and recall ranking |
| `autocomplete-intel-agent` | Tab completion synthesis, fuzzy ranking, man-page harvesting, and contextual suggestion |
| `env-shell-agent` | Dotfile management, profile layering (.zshrc/.bashrc), env diffing, and idempotent bootstrap |
| `ssh-remote-agent` | Jump hosts, multiplexing, keepalives, agent forwarding, and host-key pinning |
| `terminal-recorder-agent` | Asciinema-style capture, timing file synthesis, and deterministic replay gates |
| `log-tail-agent` | Follow-mode, ANSI stripping, pattern alerting, and backpressure handling |
| `job-control-agent` | Foreground/background, disown/nohup, signal routing, and exit trap cleanup |
| `keybinding-doctor-agent` | Readline/editing mode, keymap conflict resolution, and latency-to-action tracing |
| `terminal-security-agent` | Shell injection forensics, quoted-arg validation, and paste-jacking guards |
| `repl-bridge-agent` | Python/Node/Ruby REPL orchestration, cell execution guards, and output capture |
| `man-help-agent` | Man page summarization, flag inference, example harvesting, and TL;DR generation |
| `shell-benchmark-agent` | Startup time (zsh --startup), plugin cost, and prompt latency profiling |

### Server Mgmt (Linux/Mac/Win) (38)
| Agent | What it does |
|---|---|
| `linux-admin-agent` | User/group/sudo, service (systemd), cron/at, and filesystem (ext4/xfs/btrfs) operations |
| `systemd-surgeon-agent` | Unit authoring, dependency ordering, socket activation, and journald forensics |
| `package-manager-agent` | apt/dnf/pacman/apk/zypper — repo pinning, hold/unhold, and atomic rollback |
| `kernel-tuner-agent` | sysctl, cgroups v2, io-queue, hugepages, and perf/eBPF perf analysis |
| `network-ops-agent` | iptables/nftables, ip route, DNS (systemd-resolved/Unbound), and mtr forensics |
| `storage-raid-agent` | RAID/LVM/ZFS/btrfs, fstab, mount guards, and SMART failure prediction |
| `log-rotation-agent` | logrotate/journal vacuuming, retention budgets, and centralized shipper wiring |
| `backup-restore-agent` | rsync/restic/borg, push vs pull, encryption, and restore drill verification |
| `sec-hardening-agent` | CIS benchmarks, Lynis scoring, fail2ban, AppArmor/SELinux, and auditd |
| `container-ops-agent` | Docker/Podman, cgroups, overlayfs, rootless, and image provenance (cosign) |
| `k8s-pilot-agent` | kubectl, helm, Kustomize, CNI/CSI forensics, and etcd backup/restore |
| `nginx-ops-agent` | vhosts, upstreams, mTLS, rate-limit, and config test/ reload choreography |
| `macos-admin-agent` | launchd, defaults, profiles, MDM, SIP/TCC, and `systemextensionsctl` |
| `brew-ops-agent` | Formula/cask lifecycle, pin, bottle vs source, and cleanup/doctor diagnostics |
| `xcode-ops-agent` | xcodebuild, simulators, provisioning, notarization, and SPM resolution |
| `macos-security-agent` | Gatekeeper, XProtect, TCC db, keychain, and Endpoint Security framework |
| `windows-admin-agent` | Registry, services (sc.exe), Task Scheduler, and NTFS/ACL forensics |
| `powershell-forge-agent` | Module authoring, DSC, remoting (WinRM), and execution policy forensics |
| `winget-choco-agent` | Package resolution, silent install flags, and winget source pinning |
| `windows-security-agent` | Defender, AppLocker/WDAC, Credential Guard, and event log forensics |
| `ad-identity-agent` | Active Directory/GPO, Entra ID sync, LDAP, and Kerberos ticket forensics |
| `ci-cd-orchestrator-agent` | GitHub Actions/GitLab CI/CircleCI, cache-hit optimization, and runner fleet sizing |
| `observability-stack-agent` | Prometheus/Grafana/OTel/Loki, SLO burn, and cardinality explosion guards |
| `infra-provisioner-agent` | Terraform/OpenTofu, state locking, drift detection, and provider pinning |
| `ansible-pilot-agent` | Playbook linting, idempotency verification, vault, and inventory forensics |
| `tls-cert-agent` | ACME/Let's Encrypt, chain validation, OCSP, and cert-rotation without downtime |
| `db-ops-agent` | Postgres/MySQL/Redis — vacuum/replication/latency, slow-query forensics, backup PITR |
| `queue-ops-agent` | Kafka/RabbitMQ/SQS — partition lag, dead-letter triage, and exactly-once forensics |
| `cdn-edge-agent` | Cache keys, purge, stale-while-revalidate, and edge function forensics |
| `incident-ops-agent` | On-call handoff, status page, postmortem, and runbook-as-code |
| `cost-ops-agent` | Tagging hygiene, idle/oversized detection, reservation modeling, and showback |
| `compliance-ops-agent` | SOC2/HIPAA evidence, CIS drift, and continuous audit trails |
| `secrets-ops-agent` | Vault/1Password/AWS Secrets Manager rotation, lease scoping, and break-glass drills |
| `gitops-pilot-agent` | ArgoCD/Flux, drift vs desired, sync waves, and progressive delivery analysis |
| `edge-iot-agent` | Fleet OTA, MQTT, secure boot attestation, and offline-queue draining |
| `perf-lab-agent` | CPU flame graphs, heap profiles, io_uring, and p95 regression gates |
| `disaster-recovery-agent` | RTO/RPO math, pilot-light vs warm-standby, and chaos-day runbooks |
| `migration-ops-agent` | Lift-and-shift vs replatform, data gravity, cutover windows, and rollback rehearsals |

```bash
# try any of the 100:
python agents/browser-pilot-agent/cli/browser_pilot.py --text "automate checkout flow with profile isolation"
python agents/shell-pilot-agent/cli/shell_pilot.py --text "debug bash zsh prompt on linux"
python agents/linux-admin-agent/cli/linux_admin.py --text "systemd unit for ubuntu with journalctl" --os linux
python agents/windows-admin-agent/cli/windows_admin.py --text "powershell remoting with registry on windows" --os windows
```

## 🧪 Testing & CI

```bash
make test       # 183 tests: providers, loop, HITL, budgets, RAG, MCP, A2A, evals...
make coverage   # line coverage for core/ + factory/
make smoke      # 5-second offline sanity check
make docker     # image with baked-in offline smoke gate
```

CI runs on every push: syntax compile → offline import smoke → Python 3.10/3.11/3.12 matrix with coverage → sub-agent CLI end-to-end job → MCP stdio protocol conformance.

## 🔧 Configuration

Copy `.env.example` → `.env`. Defaults are offline-safe: `AGENT_LLM_PROVIDER=echo`. Add `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` only when you want live models.

---

## 📄 License & Governance

MIT License — see [`LICENSE`](./LICENSE). Contributions follow [`CONTRIBUTING.md`](./CONTRIBUTING.md); report vulnerabilities per [`SECURITY.md`](./SECURITY.md); history in [`CHANGELOG.md`](./CHANGELOG.md).

**Depth-Skills cognitive protocols** — inspired by [depth-skills](https://github.com/Kshitijpalsinghtomar/depth-skills). **Steve Jobs Product DNA** — see [`docs/STEVE_JOBS_PRODUCT_DNA.md`](./docs/STEVE_JOBS_PRODUCT_DNA.md).
