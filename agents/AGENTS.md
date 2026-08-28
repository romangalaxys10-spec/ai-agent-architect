# 🤖 Sub-Agents Hub
### *Specialized Autonomous Sub-Agents Organized Under AI Agent Architect*

All specialized sub-agents are organized in this dedicated `agents/` directory. Each sub-agent is modular, self-contained, and dynamically discoverable by the master orchestrator.

---

## 🌟 Complete Sub-Agent Catalog (435 Specialized Sub-Agents)

### 🧠 Cognitive Architecture & Metacognition (Depth-Skills Powered)
| Sub-Agent | Category | Description | Primary CLI | Location |
|---|---|---|---|---|
| 🧠 **`depth-conductor-agent`** | Cognitive Depth | Powered by `depth-skills`. Prevents premature closure, excavates hidden assumptions, generates contrarian paths, and stress-tests architectures. | `python cli/conductor.py` | [`agents/depth-conductor-agent/`](./depth-conductor-agent) |
| 🏛️ **`senior-architect-agent`** | Systems Architecture | Cognitive DAG state-machine design, modular decomposition, and zero-trust verification. | `agent-architect` | [`agents/senior-architect-agent/`](./senior-architect-agent) |
| 🍏 **`steve-jobs-agent`** | Product Taste | Enforces *Focus (Saying NO to 1,000 things)*, *The Whole Widget*, and binary quality verdicts (`INSANELY_GREAT` vs `TOTAL_BULLSHIT`). | `agent-architect review` | [`agents/steve-jobs-agent/`](./steve-jobs-agent) |
| 🏭 **`skill-factory-agent`** | Skill Scaffolding | Automated builder for universal `SKILL.md` packages with verification fixtures. | `agent-architect scaffold-skill` | [`agents/skill-factory-agent/`](./skill-factory-agent) |

### 🎨 Design & Product UI
| Sub-Agent | Category | Description | Primary CLI | Location |
|---|---|---|---|---|
| 🎨 **`superdesign-agent`** | Design & UI/UX | 100% Credit-Free Anti-AI-Slop design engine for responsive websites, 16:9 keynote decks, and Teenage Engineering telemetry HUDs. | `superdesign` | [`agents/superdesign-agent/`](./superdesign-agent) |

### ⚡ Web3 & Security Operations
| Sub-Agent | Category | Description | Primary CLI | Location |
|---|---|---|---|---|
| ⚡ **`solana-stream-sentinel`** | Web3 & On-Chain | Yellowstone Geyser gRPC real-time sniffer, Meteora DLMM / Raydium pool decoder, and MEV preflight simulator. | `python cli/sentinel.py` | [`agents/solana-stream-sentinel/`](./solana-stream-sentinel) |
| 🛡️ **`binary-reverse-sentinel`** | Security & Reversing | Mach-O & iOS IPA security scanner, cloud credential leak hunter, and private API endpoint extractor. | `python cli/reverser.py` | [`agents/binary-reverse-sentinel/`](./binary-reverse-sentinel) |

### 📈 Marketing, Discord & Lead Generation
| Sub-Agent | Category | Description | Primary CLI | Location |
|---|---|---|---|---|
| 🎯 **`linkedin-intent-sniper`** | LinkedIn Growth | B2B buying-intent analyzer, profile signal scraper, and hyper-personalized value-first LinkedIn outreach. | `python cli/sniper.py` | [`agents/linkedin-intent-sniper/`](./linkedin-intent-sniper) |
| 🛰️ **`discord-community-radar`** | Community Telemetry | Real-time Discord developer feed scanner, paid gig/bounty detector, and technical authority reply generator. | `python cli/radar.py` | [`agents/discord-community-radar/`](./discord-community-radar) |
| ✍️ **`anti-slop-content-engine`** | Thought Leadership | Converts raw Git commits and benchmark graphs into high-CTR viral X threads and LinkedIn case studies. | `python cli/content.py` | [`agents/anti-slop-content-engine/`](./anti-slop-content-engine) |
| 🚀 **`product-launch-orchestrator`** | Launch Campaigns | Multi-platform product launch campaigns for GitHub repos, Show HN posts, Product Hunt, and Reddit developer subs. | `python cli/launch.py` | [`agents/product-launch-orchestrator/`](./product-launch-orchestrator) |
| 📬 **`cold-outreach-dealflow`** | B2B Sales & Contracts | High-deliverability technical email sequences, spam-word linter, and Statement of Work (SOW) contract generator. | `python cli/dealflow.py` | [`agents/cold-outreach-dealflow/`](./cold-outreach-dealflow) |

### 🛠️ Core Operations & Infrastructure
| Sub-Agent | Category | Description | Primary CLI | Location |
|---|---|---|---|---|
| 🎯 **`career-hunter-orchestrator`** | Career & Leads | Headless job scout, ATS-optimized resume generator, bespoke cover letter engine, and lead CRM. | `python cli/career.py` | [`agents/career-hunter-orchestrator/`](./career-hunter-orchestrator) |
| 🧠 **`model-bridge-router`** | LLM Gateway | Adaptive multi-model router (GLM-4.7/5.3, Claude 3.7, Local) with unified tool schema translation and cost optimizer. | `python cli/bridge.py` | [`agents/model-bridge-router/`](./model-bridge-router) |
| 🧾 **`invoice-billing-sentinel`** | Finance & Ops | Deterministic multi-currency invoice generator, timesheet tracker, and vector financial reports. | `python cli/billing.py` | [`agents/invoice-billing-sentinel/`](./invoice-billing-sentinel) |

---



---

## 🌍 Top-50 Demand-Driven Agent Suite (2026)

*The 50 most-wanted, highest-searched agent capabilities — built end-to-end on the v2.0 framework. Demand basis: 2025–2026 global search & market research (coding agents #1; support automation = largest enterprise spend; sales agents $3.25B @ 44.7% CAGR; deep research = fastest-growing search term). Every agent: offline-deterministic engine + argparse CLI + SKILL.md contract + smoke-tested (`tests/test_top50_agents.py`).*

### 💻 Coding & Development
| Sub-Agent | What it does | CLI |
|---|---|---|
| 🔍 **`code-review-sentinel`** | Severity-ranked static review with CWE mapping and PASS/NEEDS_CHANGES gate | `python cli/code_review.py` |
| 🧪 **`test-forge-agent`** | pytest skeleton generation + branch-accounted coverage gap analysis | `python cli/test_forge.py` |
| 🐛 **`bug-triage-agent`** | Defect classification, repro checklists, ranked RCA hypotheses | `python cli/bug_triage.py` |
| 🩺 **`ci-surgeon-agent`** | CI failure diagnosis with fix playbooks and flake verdicts | `python cli/ci_surgeon.py` |
| ✈️ **`refactor-pilot-agent`** | Code-smell detection + risk-gated, behavior-preserving flight plan | `python cli/refactor_pilot.py` |
| 📜 **`doc-scribe-agent`** | API reference + usage examples generated from source | `python cli/doc_scribe.py` |
| 🛡️ **`sast-sentinel-agent`** | OWASP Top-10 static security scan with CVSS-style severities | `python cli/sast_sentinel.py` |
| 📦 **`dep-guardian-agent`** | Dependency risk audit, EOL knowledge, safe upgrade ordering | `python cli/dep_guardian.py` |
| 🗺️ **`migration-planner-agent`** | Phased strangler-fig migration campaigns with HITL gates | `python cli/migration_planner.py` |
| ✍️ **`commit-crafter-agent`** | Conventional commits + changelog entries + semver bumps from diffs | `python cli/commit_crafter.py` |

### 🎧 Customer Support
| Sub-Agent | What it does | CLI |
|---|---|---|
| 🎫 **`ticket-router-agent`** | Intent classification, entity extraction, queue routing + SLA clock | `python cli/ticket_router.py` |
| 📚 **`kb-curator-agent`** | KB gap/duplicate/staleness audit mapped to ticket themes | `python cli/kb_curator.py` |
| 🛟 **`escalation-shield-agent`** | Churn-risk scoring with evidence and save-play prescriptions | `python cli/escalation_shield.py` |
| 🗣️ **`voice-of-customer-agent`** | Theme clustering + sentiment + prioritized fix ranking | `python cli/voice_of_customer.py` |
| ⏱️ **`sla-sentinel-agent`** | Breach projection per ticket + intervention ordering | `python cli/sla_sentinel.py` |

### 📈 Sales & Marketing
| Sub-Agent | What it does | CLI |
|---|---|---|
| 🎯 **`lead-qualifier-agent`** | BANT evidence scoring, MQL/SQL tiering, honest disqualifiers | `python cli/lead_qualifier.py` |
| ✉️ **`outreach-personalizer-agent`** | 3-tone personalized emails + spam lint + A/B sequence | `python cli/outreach_personalizer.py` |
| 📋 **`meeting-brief-agent`** | Attendee map, timed agenda, objection plays, pre-reads | `python cli/meeting_brief.py` |
| 🧹 **`crm-hygiene-agent`** | Duplicate detection, field debt, forecast-impact cleanup plan | `python cli/crm_hygiene.py` |
| 📡 **`competitor-radar-agent`** | Move classification, threat scoring, battlecard deltas | `python cli/competitor_radar.py` |
| 🔎 **`seo-content-strategist-agent`** | Topic clusters, outlines, link graphs, E-E-A-T checklists | `python cli/seo_content.py` |
| 💰 **`ad-campaign-optimizer-agent`** | CTR/CPC/CPA/ROAS audit + budget reallocation + experiments | `python cli/ad_campaign.py` |

### 🔬 Research & Analysis
| Sub-Agent | What it does | CLI |
|---|---|---|
| 🧠 **`deep-research-agent`** | Source cross-examination: corroboration + contradiction matrices | `python cli/deep_research.py` |
| 📊 **`data-analyst-agent`** | CSV profiling: stats, outliers, correlations, chart picks (pure stdlib) | `python cli/data_analyst.py` |
| ✅ **`fact-check-agent`** | Atomic claim decomposition + evidence-trail verdicts | `python cli/fact_check.py` |
| 🌐 **`market-scout-agent`** | TAM/SAM/SOM two-method sizing + entry verdict | `python cli/market_scout.py` |
| 📚 **`literature-review-agent`** | Paper clustering, evolution, contradictions, research gaps | `python cli/literature_review.py` |

### ⚡ Personal Productivity
| Sub-Agent | What it does | CLI |
|---|---|---|
| 📥 **`email-triage-agent`** | Eisenhower quadrants + ask/deadline extraction + reply drafts | `python cli/email_triage.py` |
| 📅 **`calendar-architect-agent`** | EDF scheduling with focus blocks and conflict flags | `python cli/calendar_architect.py` |
| 📝 **`meeting-scribe-agent`** | Notes → decisions + owner/deadline action items + questions | `python cli/meeting_scribe.py` |
| 🧭 **`trip-compass-agent`** | Pacing-aware itineraries + budget split + contingencies | `python cli/trip_compass.py` |
| 🛍️ **`deal-hunter-agent`** | Bayesian rating confidence + need coverage → BUY/WAIT/PASS | `python cli/deal_hunter.py` |

### 💵 Finance
| Sub-Agent | What it does | CLI |
|---|---|---|
| 🧾 **`invoice-intake-agent`** | AP invoice parsing, arithmetic validation, duplicates, 3-way match | `python cli/invoice_intake.py` |
| 🔍 **`expense-auditor-agent`** | Policy caps + fraud heuristics + compliance scoring | `python cli/expense_auditor.py` |
| 📈 **`finstat-analyst-agent`** | Margins, burn, runway, DSO, red flags, health score | `python cli/finstat.py` |
| 💼 **`portfolio-scout-agent`** | Allocation drift, HHI concentration, rebalance plan (not advice) | `python cli/portfolio_scout.py` |

### 👥 HR & Recruiting
| Sub-Agent | What it does | CLI |
|---|---|---|
| 📄 **`resume-screener-agent`** | Evidence-based skill matching + bias-safe language audit | `python cli/resume_screener.py` |
| 🎤 **`interview-coach-agent`** | Structured question bank + anchored rubrics + legal guardrails | `python cli/interview_coach.py` |
| 🚀 **`onboarding-guide-agent`** | 30/60/90 outcome gates + week-1 schedule + access checklist | `python cli/onboarding_guide.py` |
| 💓 **`culture-pulse-agent`** | eNPS, segment gaps, comment themes, interventions | `python cli/culture_pulse.py` |

### 🎨 Content & Creative
| Sub-Agent | What it does | CLI |
|---|---|---|
|🗓️ **`content-calendar-agent`** | Editorial calendars with format mix + repurposing map | `python cli/content_calendar.py` |
| 🎬 **`script-writer-agent`** | Video scripts with retention beats + platform cutdowns | `python cli/script_writer.py` |
| 📱 **`social-media-manager-agent`** | Post variants, tiered hashtags, reply kit, posting windows | `python cli/social_media.py` |
| ✂️ **`copy-editor-agent`** | Passive/filler/jargon detection + Flesch + rewrite | `python cli/copy_editor.py` |

### 🖥️ Ops, IT & Security
| Sub-Agent | What it does | CLI |
|---|---|---|
| ☁️ **`cloud-cost-optimizer-agent`** | Idle/oversized/zombie detection + savings plan with guardrails | `python cli/cloud_cost.py` |
| 🚨 **`incident-commander-agent`** | SEV classification, runbook, comms drafts, postmortem scaffold | `python cli/incident_commander.py` |
| 🔐 **`access-review-agent`** | Least-privilege audit + evidence-backed revocation list | `python cli/access_review.py` |

### 🎓 Education, Legal & Life
| Sub-Agent | What it does | CLI |
|---|---|---|
| 🏛️ **`socratic-tutor-agent`** | Question ladders + misconception probes + hint ladders | `python cli/socratic_tutor.py` |
| 🗣️ **`language-coach-agent`** | CEFR estimation, error taxonomy, drills, SRS queue | `python cli/language_coach.py` |
| ⚖️ **`contract-reviewer-agent`** | Clause detection, risk grading, redlines with fallbacks | `python cli/contract_reviewer.py` |

---

---

## 🚀 150 Power Expansion Suite (Global Research: GitHub + X + LinkedIn + SMM)

*150 additional agents built on the same offline-deterministic contract (SKILL.md + core engine + CLI + smoke tests). Demand basis: GitHub trending (awesome-ai-agents, 300+ resources), X/LinkedIn hiring velocity, SMM growth ops, plus coverage of all 6 canonical courses end-to-end.*

### Coding & DevOps (20)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `api-architect-agent` | Designs REST/GraphQL/gRPC APIs with OpenAPI specs, versioning, and contract tests | `python cli/api_architect.py` |
| `perf-surgeon-agent` | Bottleneck detection, flame-graph interpretation, latency budgets, and perf regression gates | `python cli/perf_surgeon.py` |
| `log-detective-agent` | Structured log aggregation, anomaly detection, distributed trace stitching, alert synthesis | `python cli/log_detective.py` |
| `infra-as-code-agent` | Terraform/Pulumi generation, drift detection, env parity checks, plan review | `python cli/infra_as_code.py` |
| `db-migration-agent` | Schema diff, zero-downtime migration plans, rollback scripts, data backfill verification | `python cli/db_migration.py` |
| `qa-oracle-agent` | Test plan matrices, edge-case enumeration, risk-based test prioritization, flaky test triage | `python cli/qa_oracle.py` |
| `release-train-agent` | Cut branches, changelog collation, semver enforcement, rollout & feature-flag coordination | `python cli/release_train.py` |
| `feature-flag-agent` | Flag lifecycle, targeting rules, kill-switch runbooks, experiment exposure auditing | `python cli/feature_flag.py` |
| `chaos-lab-agent` | Fault injection plans, blast-radius scoping, steady-state hypotheses, game-day runbooks | `python cli/chaos_lab.py` |
| `oncall-buddy-agent` | Runbook retrieval, escalation routing, post-page context assembly, handoff summaries | `python cli/oncall_buddy.py` |
| `sdk-forge-agent` | Multi-language SDK scaffolding from OpenAPI/Proto, versioned changelogs, breaking-change detection | `python cli/sdk_forge.py` |
| `git-historian-agent` | Blame forensics, bisect automation, contributor graphs, tech-debt timeline mapping | `python cli/git_historian.py` |
| `code-migration-agent` | Language/framework translation plans with semantic equivalence checks and test scaffolding | `python cli/code_migration.py` |
| `env-doctor-agent` | Repro pass/fail for .env, Docker, Node/Python version mismatches, setup script generation | `python cli/env_doctor.py` |
| `secrets-vault-agent` | Hardcoded secret scan beyond SAST, rotation schedules, least-privilege env config mapping | `python cli/secrets_vault.py` |
| `build-optimizer-agent` | Bundle-size audit, tree-shake analysis, cache-hit maximization, CI minute reduction | `python cli/build_optimizer.py` |
| `api-mock-agent` | Deterministic mocks from OpenAPI, Pact contracts, stub servers, fake-data factories | `python cli/api_mock.py` |
| `licensing-guardian-agent` | OSS license compatibility, copyleft risk, SBOM generation, attribution assembly | `python cli/licensing_guardian.py` |
| `prompt-ops-agent` | Prompt versioning, regression evals, few-shot curation, token-cost vs quality tradeoffs | `python cli/prompt_ops.py` |
| `agent-eval-harness-agent` | Trajectory scoring, tool-use accuracy, golden-set curation, pass@k gating | `python cli/agent_eval_harness.py` |

### Data & AI/ML (15)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `ml-pipeline-agent` | Feature store wiring, training DAG authoring, eval gates, model registry lifecycle | `python cli/ml_pipeline.py` |
| `feature-store-agent` | Feature drift detection, leakage checks, importance ranking, store backfill plans | `python cli/feature_store.py` |
| `model-risk-agent` | Bias/fairness audits, SHAP-style attribution summaries, challenger-model comparison, MRM reports | `python cli/model_risk.py` |
| `vector-db-architect-agent` | Index selection (HNSW/IVF), chunking strategy, ANN recall benchmarking, hybrid search tuning | `python cli/vector_db_architect.py` |
| `etl-surgeon-agent` | Pipeline lineage mapping, idempotency checks, late-arriving data handling, cost-per-GB optimization | `python cli/etl_surgeon.py` |
| `dashboard-crafter-agent` | KPI tree design, chart selection logic, SQL generation, stakeholder-ready narrative framing | `python cli/dashboard_crafter.py` |
| `anomaly-hunter-agent` | Time-series outlier detection, seasonal decomposition, root-cause ranking, alert suppression tuning | `python cli/anomaly_hunter.py` |
| `forecast-oracle-agent` | Horizon selection, Prophet/ARIMA-style heuristics, confidence intervals, scenario modeling | `python cli/forecast_oracle.py` |
| `nlp-pipeline-agent` | Tokenization choices, NER/CLS routing, eval on imbalanced sets, multilingual tradeoffs | `python cli/nlp_pipeline.py` |
| `label-ops-agent` | Label schema design, IAA measurement, active-learning queue prioritization, QA sampling plans | `python cli/label_ops.py` |
| `synthetic-data-agent` | Privacy-preserving synthetic generation, fidelity metrics, bias preservation checks | `python cli/synthetic_data.py` |
| `data-governance-agent` | PII discovery, retention policy mapping, lineage cataloging, access-tier enforcement | `python cli/data_governance.py` |
| `experiment-tracker-agent` | Run comparison matrices, hyperparam importance, early-stopping verdicts, reproducibility checklists | `python cli/experiment_tracker.py` |
| `rag-architect-agent` | Chunking/embedding model selection, retrieval grading, citation grounding, hallucination rate measurement | `python cli/rag_architect.py` |
| `agent-memory-architect-agent` | Working/episodic/semantic tier design, compaction triggers, retrieval policy tuning | `python cli/agent_memory_architect.py` |

### Security & Compliance (12)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `threat-model-agent` | STRIDE mapping, attack-tree enumeration, mitigations ranked by risk-to-cost | `python cli/threat_model.py` |
| `pen-test-scribe-agent` | Finding deduplication, CVSS scoring, evidence packets, remediation roadmaps | `python cli/pen_test_scribe.py` |
| `soc-triage-agent` | Alert correlation, false-positive suppression, playbook dispatch, MTTR estimation | `python cli/soc_triage.py` |
| `privacy-shield-agent` | GDPR/CCPA gap analysis, DPA clause mapping, consent-flow audits, retention enforcement | `python cli/privacy_shield.py` |
| `compliance-mapper-agent` | SOC2/ISO27001/HIPAA control mapping, evidence collection checklists, gap heatmaps | `python cli/compliance_mapper.py` |
| `red-team-agent` | Jailbreak prompt generation, guardrail bypass attempts, safety eval reporting | `python cli/red_team.py` |
| `forensics-timeline-agent` | Artifact correlation, chain-of-custody logging, timeline reconstruction | `python cli/forensics_timeline.py` |
| `identity-governance-agent` | SoD conflict detection, certification campaign planning, orphaned account hunting | `python cli/identity_governance.py` |
| `supply-chain-guard-agent` | Dependency provenance, sigstore verification, typosquat detection, SBOM diffing | `python cli/supply_chain_guard.py` |
| `crypto-audit-agent` | Primitive misuse detection, key-length enforcement, rotation hygiene scoring | `python cli/crypto_audit.py` |
| `bug-bounty-triage-agent` | Report deduplication, reproducibility checks, severity re-grading, payout band mapping | `python cli/bug_bounty_triage.py` |
| `incident-legal-bridge-agent` | Breach classification, notification timeline, regulator mapping, disclosure draft generation | `python cli/incident_legal_bridge.py` |

### Sales & Revenue Ops (12)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `pricing-strategist-agent` | Willingness-to-pay modeling, packaging tiers, discount guardrails, expansion triggers | `python cli/pricing_strategist.py` |
| `sales-coach-agent` | MEDDICC gap analysis, talk-time metrics, objection handling plays, next-step enforcement | `python cli/sales_coach.py` |
| `proposal-forge-agent` | RFP shredding, win-theme mapping, compliance matrix, proposal narrative assembly | `python cli/proposal_forge.py` |
| `revenue-ops-agent` | Funnel stage conversion, forecast hygiene, territory balancing, comp-plan alignment | `python cli/revenue_ops.py` |
| `churn-prophet-agent` | Health scoring, leading-indicator ranking, save-play matching, expansion risk flagging | `python cli/churn_prophet.py` |
| `partner-ecosystem-agent` | Partner-fit scoring, co-sell motion design, referral tracking, enablement gap analysis | `python cli/partner_ecosystem.py` |
| `sales-enablement-agent` | Battlecard freshness, asset-to-stage mapping, rep ramp checklists, content gap closure | `python cli/sales_enablement.py` |
| `gong-clone-agent` | Call transcript themes, competitor mention tracking, coaching moment extraction | `python cli/gong_clone.py` |
| `account-plan-agent` | Org chart mapping, whitespace analysis, multi-threading plan, executive briefing pack | `python cli/account_plan.py` |
| `forecast-radar-agent` | Pipeline coverage math, stage-weighted forecast, risk-adjusted commit calls | `python cli/forecast_radar.py` |
| `win-loss-analyst-agent` | Interview synthesis, loss-reason taxonomy, competitive loss attribution, fix-backlog routing | `python cli/win_loss_analyst.py` |
| `event-roi-agent` | Event cost capture, lead-to-opportunity math, follow-up SLA enforcement, repeat/skip verdict | `python cli/event_roi.py` |

### Marketing & Growth (13)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `growth-loops-agent` | Loop mapping (acquisition/retention/monetization), unit economics, experiment backlog | `python cli/growth_loops.py` |
| `influencer-scout-agent` | Audience overlap scoring, authenticity checks, brief generation, performance attribution | `python cli/influencer_scout.py` |
| `brand-voice-agent` | Tone taxonomy enforcement, off-brand flagging, rewrite suggestions with voice preservation | `python cli/brand_voice.py` |
| `lifecycle-marketer-agent` | Journey mapping, trigger logic, send-time optimization, deliverability linting | `python cli/lifecycle_marketer.py` |
| `community-builder-agent` | Channel health scoring, contributor ladder design, moderation playbooks, activation campaigns | `python cli/community_builder.py` |
| `web-analytics-agent` | Funnel drop analysis, cohort retention curves, attribution model comparison | `python cli/web_analytics.py` |
| `paid-social-surgeon-agent` | Creative fatigue detection, audience saturation scoring, bid strategy tuning | `python cli/paid_social_surgeon.py` |
| `affiliate-ops-agent` | Payout integrity, fraud heuristics, creative freshness scoring, partner tiering | `python cli/affiliate_ops.py` |
| `pr-pitch-agent` | Angle generation, journalist-fit scoring, embargo timing, follow-up sequencing | `python cli/pr_pitch.py` |
| `launch-telemetry-agent` | Pre/post metric deltas, sentiment shift, source attribution, repeat-launch playbook | `python cli/launch_telemetry.py` |
| `referral-architect-agent` | Incentive design, viral coefficient math, fraud controls, share-copy generation | `python cli/referral_architect.py` |
| `local-seo-agent` | NAP consistency audit, review velocity tracking, GMB optimization checklist | `python cli/local_seo.py` |
| `video-growth-agent` | Hook scoring, retention-curve analysis, thumbnail/title A/B planning, platform cutdowns | `python cli/video_growth.py` |

### Product & Research (10)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `ux-research-agent` | Interview coding, affinity mapping, insight prioritization, JTBD extraction | `python cli/ux_research.py` |
| `roadmap-architect-agent` | RICE/WSJF scoring, dependency mapping, theme balancing, stakeholder narrative | `python cli/roadmap_architect.py` |
| `spec-writer-agent` | Requirement decomposition, acceptance criteria authoring, edge-case enumeration, open-question tracking | `python cli/spec_writer.py` |
| `design-system-agent` | Token hygiene, component API consistency, Figma drift detection, adoption metrics | `python cli/design_system.py` |
| `user-journey-agent` | Touchpoint mapping, emotion curves, pain-point severity ranking, opportunity sizing | `python cli/user_journey.py` |
| `ab-test-architect-agent` | Hypothesis framing, sample-size math, guardrail metrics, ship/hold/iterate verdicts | `python cli/ab_test_architect.py` |
| `accessibility-auditor-agent` | WCAG 2.2 checks, screen-reader flow testing, color contrast math, remediation priority | `python cli/accessibility_auditor.py` |
| `localization-pilot-agent` | String externalization, pseudo-locale testing, cultural adaptation flags, TM leverage scoring | `python cli/localization_pilot.py` |
| `feedback-miner-agent` | Support/survey/app-review clustering, theme-to-roadmap linking, fix prioritization | `python cli/feedback_miner.py` |
| `jobs-to-be-done-agent` | Job statement extraction, switch-moment mapping, competing-solution analysis | `python cli/jobs_to_be_done.py` |

### Ops, Finance & Legal (12)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `procurement-scout-agent` | Vendor comparison matrices, TCO modeling, negotiation leverage mapping, renewal risk flags | `python cli/procurement_scout.py` |
| `contract-lifecycle-agent` | Obligation extraction, renewal/deadline tracking, clause deviation flagging | `python cli/contract_lifecycle.py` |
| `tax-navigator-agent` | Jurisdiction mapping, nexus flagging, filing deadline calendar, risk-ranked action list (not advice) | `python cli/tax_navigator.py` |
| `treasury-ops-agent` | Cash positioning, bank fee audit, FX exposure flagging, liquidity runway math | `python cli/treasury_ops.py` |
| `audit-trail-agent` | Evidence packet assembly, control-to-artifact mapping, auditor-ready narratives | `python cli/audit_trail.py` |
| `vendor-risk-agent` | Risk tiering, questionnaire gap analysis, mitigation plan generation | `python cli/vendor_risk.py` |
| `kpi-ledger-agent` | North-star decomposition, metric ownership, anomaly alerts, board-ready rollups | `python cli/kpi_ledger.py` |
| `okr-coach-agent` | Objective quality scoring, key-result measurability checks, alignment mapping, retrospective synthesis | `python cli/okr_coach.py` |
| `meeting-ops-agent` | Meeting load analysis, purpose/attendee pruning, async-shift recommendations | `python cli/meeting_ops.py` |
| `policy-drafter-agent` | Policy structure generation, control mapping, exception workflow, review cadence design | `python cli/policy_drafter.py` |
| `real-estate-scout-agent` | Location scoring, comps analysis, cap-rate math, due-diligence checklist | `python cli/real_estate_scout.py` |
| `insurance-advisor-agent` | Gap analysis, limit adequacy, exclusion flagging, renewal negotiation prep (not advice) | `python cli/insurance_advisor.py` |

### HR & Talent (8)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `talent-sourcer-agent` | Boolean search construction, profile-fit scoring, outreach personalization, pipeline health tracking | `python cli/talent_sourcer.py` |
| `performance-review-agent` | Feedback theme synthesis, calibration support, growth-plan drafting, bias flagging | `python cli/performance_review.py` |
| `compensation-benchmark-agent` | Band mapping, market percentile analysis, pay-equity flags, offer construction (not advice) | `python cli/compensation_benchmark.py` |
| `learning-path-agent` | Skill-gap mapping, curriculum sequencing, adaptive checkpoint design, certification prep | `python cli/learning_path.py` |
| `workforce-planner-agent` | Capacity modeling, hiring plan phasing, attrition risk flags, org design options | `python cli/workforce_planner.py` |
| `exit-insight-agent` | Departure theme extraction, regretted vs non-regretted loss, retention lever mapping | `python cli/exit_insight.py` |
| `dei-auditor-agent` | Pipeline diversity metrics, language inclusivity audit, intervention effectiveness scoring | `python cli/dei_auditor.py` |
| `manager-coach-agent` | 1:1 agenda generation, coaching prompt synthesis, team health diagnostics | `python cli/manager_coach.py` |

### Support & Success (7)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `csat-surgeon-agent` | Driver analysis, recovery playbooks, closed-loop tracking, segment trending | `python cli/csat_surgeon.py` |
| `knowledge-ops-agent` | Article performance vs ticket deflection, freshness SLA, AI-assist readiness scoring | `python cli/knowledge_ops.py` |
| `support-qa-agent` | Interaction scoring against rubric, coaching themes, calibration packet assembly | `python cli/support_qa.py` |
| `renewal-orchestrator-agent` | Health-triggered playbooks, commercial term tracking, risk-adjusted renewal forecast | `python cli/renewal_orchestrator.py` |
| `community-support-agent` | Forum post classification, crowdsourced answer scoring, escalation to KB creation | `python cli/community_support.py` |
| `nps-driver-agent` | Promoter/passive/detractor drivers, closed-loop prioritization, exec narrative | `python cli/nps_driver.py` |
| `self-serve-architect-agent` | Deflection opportunity scoring, flow design, containment rate tracking | `python cli/self_serve_architect.py` |

### Creator & Media (8)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `podcast-producer-agent` | Episode arcs, show-note generation, guest research packs, distribution checklist | `python cli/podcast_producer.py` |
| `newsletter-architect-agent` | Section planning, curation scoring, subject-A/B generation, send-time optimization | `python cli/newsletter_architect.py` |
| `ugc-curator-agent` | Submission triage, rights management, creator attribution, repurposing queue | `python cli/ugc_curator.py` |
| `meme-ops-agent` | Trend velocity scoring, format-body fit, timing windows, brand-safety gates | `python cli/meme_ops.py` |
| `press-kit-agent` | Boilerplate synthesis, asset inventory, embargo packet, media Q&A prep | `python cli/press_kit.py` |
| `course-builder-agent` | Learning objective mapping, module sequencing, assessment design, completion analytics | `python cli/course_builder.py` |
| `event-producer-agent` | Run-of-show authoring, speaker/venue logistics, contingency branches, post-event retro | `python cli/event_producer.py` |
| `creator-monetization-agent` | Revenue stream mapping, tier pricing, sponsor-fit scoring, payout optimization | `python cli/creator_monetization.py` |

### Vertical Specialists (13)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `healthcare-scribe-agent` | SOAP note structuring, code suggestion, compliance flagging (not medical advice) | `python cli/healthcare_scribe.py` |
| `legal-ops-agent` | Matter intake, outside-counsel spend tracking, playbook compliance, ebilling audit | `python cli/legal_ops.py` |
| `proptech-analyst-agent` | Rent-roll parsing, valuation sensitivity, zoning flag checks, investment memo drafting | `python cli/proptech_analyst.py` |
| `edtech-coach-agent` | Curriculum alignment, Bloom-level tagging, assignment feedback scaffolding | `python cli/edtech_coach.py` |
| `fintech-compliance-agent` | KYC/AML flow checks, transaction monitoring flag review, regulatory mapping | `python cli/fintech_compliance.py` |
| `climate-risk-agent` | Physical/transition risk scoring, disclosure mapping (TCFD/ISSB), mitigation ranking | `python cli/climate_risk.py` |
| `supply-chain-optimizer-agent` | Demand forecast reconciliation, inventory policy, route optimization, disruption playbooks | `python cli/supply_chain_optimizer.py` |
| `retail-merchandiser-agent` | Assortment planning, markdown optimization, planogram compliance, sell-through analysis | `python cli/retail_merchandiser.py` |
| `hospitality-ops-agent` | Occupancy pacing, upsell triggers, staffing-to-demand matching, guest recovery workflows | `python cli/hospitality_ops.py` |
| `manufacturing-qa-agent` | SPC chart interpretation, defect Pareto, CAPA tracking, traceability mapping | `python cli/manufacturing_qa.py` |
| `energy-ops-agent` | Load forecasting, tariff optimization, curtailment planning, carbon accounting | `python cli/energy_ops.py` |
| `gov-procurement-agent` | RFP eligibility checks, compliance matrix, proposal choreography for public sector | `python cli/gov_procurement.py` |
| `nonprofit-impact-agent` | Theory-of-change mapping, outcome metric design, grant reporting packet assembly | `python cli/nonprofit_impact.py` |

### Emerging & Agent-Native (10)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `autonomous-researcher-agent` | Hypothesis generation, experiment planning, lit-review synthesis, preprint monitoring | `python cli/autonomous_researcher.py` |
| `eval-judge-agent` | Rubric authoring, LLM-as-judge calibration, inter-rater agreement scoring, golden-set expansion | `python cli/eval_judge.py` |
| `tool-smith-agent` | Tool schema design, validation harness, mock-server generation, version migration planning | `python cli/tool_smith.py` |
| `orchestration-designer-agent` | Topology selection (hierarchical/mesh/blackboard), handoff choreography, failure-mode mapping | `python cli/orchestration_designer.py` |
| `memory-ops-agent` | Memory tier health, compaction trigger tuning, recall precision measurement, curation backlog | `python cli/memory_ops.py` |
| `adversarial-tester-agent` | Red-team prompt banks, bypass attempt logging, safety regression tracking | `python cli/adversarial_tester.py` |
| `cost-optimizer-agent` | Token/latency Pareto frontier, model routing policy, cache-hit maximization | `python cli/cost_optimizer.py` |
| `skills-librarian-agent` | Skill discovery indexing, reuse scoring, deprecation planning, marketplace curation | `python cli/skills_librarian.py` |
| `workflow-miner-agent` | Process mining from logs, variant analysis, automation opportunity ranking | `python cli/workflow_miner.py` |
| `digital-twin-agent` | State-sync design, simulation scenario authoring, drift detection, what-if analysis | `python cli/digital_twin.py` |

### GTM & SMM Power Suite (10)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `x-growth-hacker-agent` | Viral hook engineering, thread pacing, reply-guy strategy, algorithmic timing optimization | `python cli/x_growth_hacker.py` |
| `linkedin-authority-agent` | POV extraction from commits, carousel outlining, comment-to-DM funnel, SSI scoring | `python cli/linkedin_authority.py` |
| `youtube-growth-agent` | Title/thumbnail scoring, retention editing, chapter optimization, cross-platform repurposing | `python cli/youtube_growth.py` |
| `tiktok-virality-agent` | Hook-window optimization, trend-jacking timing, sound selection, loop-rate engineering | `python cli/tiktok_virality.py` |
| `smm-command-center-agent` | Cross-platform calendar, asset variant generation, performance rollup, crisis monitoring | `python cli/smm_command_center.py` |
| `influencer-ops-agent` | Brief generation, deliverable tracking, usage-rights ledger, payout reconciliation | `python cli/influencer_ops.py` |
| `social-listening-agent` | Mention clustering, sentiment velocity, crisis early-warning, competitor share-of-voice | `python cli/social_listening.py` |
| `content-repurposer-agent` | Long-form -> thread/carousel/shorts atomization, platform-native rewriting, CTA tailoring | `python cli/content_repurposer.py` |
| `community-growth-agent` | Activation funnel, referral loop design, moderation at scale, UGC flywheel | `python cli/community_growth.py` |
| `paid-growth-ops-agent` | Channel mix modeling, CAC payback math, creative fatigue rotation, incrementality testing | `python cli/paid_growth_ops.py` |

All 150: `python agents/<slug>/cli/<module>.py --help` from any cwd — same contract as the Top-50 (`tests/test_top50_agents.py` pattern), plus `tests/test_power150_agents.py` for this suite.


---

## 🖥️ 100 Computer Use Series — Browser / Terminal / OS / Server (Linux · macOS · Windows)

*100 control & automation agents — OS-aware, deterministic, offline. Same contract: SKILL.md + core engine + CLI + smoke tests.*

### Computer Use (22)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `computer-vision-agent` | GUI element detection, screenshot grounding, coordinate resolution, and vision-to-action translation | `python cli/computer_vision.py` |
| `desktop-automation-agent` | Cross-app desktop workflows, window management, dock/taskbar control, and macro recording | `python cli/desktop_automation.py` |
| `screen-recorder-agent` | Session capture, action trace diffing, deterministic replay, and flake diagnosis | `python cli/screen_recorder.py` |
| `accessibility-pilot-agent` | AX tree traversal, VoiceOver/Narrator/Orca mapping, label-role audits, and a11y-driven control | `python cli/accessibility_pilot.py` |
| `keyboard-maestro-agent` | Hotkey choreography, chord sequencing, input method switching, and shortcut conflict resolution | `python cli/keyboard_maestro.py` |
| `mouse-precision-agent` | DPI-aware moves, drag semantics, hover intent, and pixel-perfect assertion | `python cli/mouse_precision.py` |
| `clipboard-ops-agent` | Multi-format clipboard (text/image/files), history vault, and cross-app paste validation | `python cli/clipboard_ops.py` |
| `file-explorer-agent` | Finder/Explorer/Nautilus navigation, batch rename, quick-look preview, and breadcrumb forensics | `python cli/file_explorer.py` |
| `notification-center-agent` | Banner/toast interception, permission routing, Do-Not-Disturb orchestration, and alert triage | `python cli/notification_center.py` |
| `system-prefs-agent` | Settings search, plist/registry diffing, profile provisioning, and drift enforcement | `python cli/system_prefs.py` |
| `spotlight-search-agent` | Indexed search, intent disambiguation, quick-open ranking, and recent-items forensics | `python cli/spotlight_search.py` |
| `window-tiling-agent` | Tiling layout synthesis, focus follows mouse, workspace assignment, and multi-monitor mapping | `python cli/window_tiling.py` |
| `menubar-tray-agent` | Status item orchestration, menu introspection, tray icon health checks | `python cli/menubar_tray.py` |
| `screenshot-assert-agent` | Visual diff, perceptual hash, region masking, and golden screenshot gates | `python cli/screenshot_assert.py` |
| `drag-drop-orchestrator-agent` | Cross-app drag semantics, payload validation, drop-zone mapping, and undo safety | `python cli/drag_drop_orchestrator.py` |
| `touch-gesture-agent` | Trackpad/phone gestures, palm rejection, pressure curves, and haptic feedback mapping | `python cli/touch_gesture.py` |
| `ocr-reader-agent` | On-screen text extraction, table de-warping, language detection, and redaction | `python cli/ocr_reader.py` |
| `audio-router-agent` | Input/output device switching, volume ducking, mic gate, and audio capture routing | `python cli/audio_router.py` |
| `camera-mic-governor-agent` | Permission gates, virtual camera/mic injection, and recording indicator enforcement | `python cli/camera_mic_governor.py` |
| `power-battery-agent` | Sleep/wake orchestration, battery health, thermal throttling, and charge-limit policies | `python cli/power_battery.py` |
| `display-color-agent` | Resolution/refresh switching, HDR/color profile validation, and night-shift scheduling | `python cli/display_color.py` |
| `input-device-agent` | Keyboard/mouse/gamepad pairing, driver health, DPI/remap sync, and latency checks | `python cli/input_device.py` |

### Browser Use (22)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `browser-pilot-agent` | Tab orchestration, navigation guards, history/cookie/session control, and profile isolation | `python cli/browser_pilot.py` |
| `cdp-bridge-agent` | Chrome DevTools Protocol — DOM, debugger, network, emulation, and trace capture | `python cli/cdp_bridge.py` |
| `playwright-orchestrator-agent` | Cross-browser (Chromium/Firefox/WebKit) test generation, auto-wait, trace viewer | `python cli/playwright_orchestrator.py` |
| `puppeteer-forge-agent` | Headless Chromium control, PDF/screenshot pipelines, and request interception | `python cli/puppeteer_forge.py` |
| `selenium-grid-agent` | Hub/node scaling, capability matching, grid health, and flaky quarantine | `python cli/selenium_grid.py` |
| `browser-extension-agent` | Manifest v3, content/background/service worker, storage sync, and store review prep | `python cli/browser_extension.py` |
| `dom-forensics-agent` | Selector resilience scoring, shadow-DOM piercing, hydration mismatch detection | `python cli/dom_forensics.py` |
| `web-scraper-agent` | Polite crawling, robots.txt respect, anti-bot evasion planning, and dataset diffing | `python cli/web_scraper.py` |
| `form-autofill-agent` | Field inference, constraint validation, CAPTCHA/Turnstile routing, and submit guards | `python cli/form_autofill.py` |
| `cookie-consent-agent` | CMP banner classification, preference persistence, and consent-string validation | `python cli/cookie_consent.py` |
| `storage-inspector-agent` | LocalStorage/SessionStorage/IndexedDB/cookies audit, quota sizing, and eviction forensics | `python cli/storage_inspector.py` |
| `network-har-agent` | HAR capture, waterfall analysis, cache-hit verification, and payload PII scrubbing | `python cli/network_har.py` |
| `performance-audit-agent` | Lighthouse/Web Vitals, CLS/LCP/INP budgets, bundle waterfall, and perf regression gates | `python cli/performance_audit.py` |
| `accessibility-web-agent` | axe-core style audits, keyboard trap detection, color contrast, and screen-reader order | `python cli/accessibility_web.py` |
| `visual-regression-agent` | Cross-viewport screenshot diff, layout shift masking, anti-alias tolerance | `python cli/visual_regression.py` |
| `auth-session-agent` | Login flows, OAuth/PKCE, MFA/TOTP, session refresh, and token theft guards | `python cli/auth_session.py` |
| `download-manager-agent` | Download orchestration, virus-scan hooks, checksum verification, and resume safety | `python cli/download_manager.py` |
| `pdf-renderer-agent` | HTML→PDF fidelity, print media CSS, pagination orphans, and PDF/A validation | `python cli/pdf_renderer.py` |
| `webrtc-media-agent` | Peer connection forensics, ICE candidate mapping, bandwidth/echo diagnostics | `python cli/webrtc_media.py` |
| `service-worker-agent` | Cache strategy, offline fallback, update lifecycle, and push subscription forensics | `python cli/service_worker.py` |
| `web-security-agent` | CSP/HSTS/XFO audit, mixed-content detection, and SRI/subresource integrity checks | `python cli/web_security.py` |
| `browser-profile-agent` | Profile cloning, fingerprint hygiene, proxy rotation, and container isolation | `python cli/browser_profile.py` |

### Terminal Use (18)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `shell-pilot-agent` | POSIX shell orchestration (bash/zsh/fish), prompt detection, and exit-code triage | `python cli/shell_pilot.py` |
| `pty-bridge-agent` | Pseudo-terminal allocation, raw mode, echo suppression, and resize propagation | `python cli/pty_bridge.py` |
| `tmux-orchestrator-agent` | Session/window/pane topology, layout persistence, and copy-mode automation | `python cli/tmux_orchestrator.py` |
| `terminal-renderer-agent` | ANSI/VT100 parsing, 24-bit color, ligature handling, and damage-region rendering | `python cli/terminal_renderer.py` |
| `cli-scaffold-agent` | Argparse/cobra/clap scaffolding, help/usage consistency, and shell completion generation | `python cli/cli_scaffold.py` |
| `prompt-engineer-agent` | Terminal prompt theme (starship/oh-my-zsh), git status embedding, and latency budgets | `python cli/prompt_engineer.py` |
| `history-forensics-agent` | Shell history forensics, deduplication, secret scrubbing, and recall ranking | `python cli/history_forensics.py` |
| `autocomplete-intel-agent` | Tab completion synthesis, fuzzy ranking, man-page harvesting, and contextual suggestion | `python cli/autocomplete_intel.py` |
| `env-shell-agent` | Dotfile management, profile layering (.zshrc/.bashrc), env diffing, and idempotent bootstrap | `python cli/env_shell.py` |
| `ssh-remote-agent` | Jump hosts, multiplexing, keepalives, agent forwarding, and host-key pinning | `python cli/ssh_remote.py` |
| `terminal-recorder-agent` | Asciinema-style capture, timing file synthesis, and deterministic replay gates | `python cli/terminal_recorder.py` |
| `log-tail-agent` | Follow-mode, ANSI stripping, pattern alerting, and backpressure handling | `python cli/log_tail.py` |
| `job-control-agent` | Foreground/background, disown/nohup, signal routing, and exit trap cleanup | `python cli/job_control.py` |
| `keybinding-doctor-agent` | Readline/editing mode, keymap conflict resolution, and latency-to-action tracing | `python cli/keybinding_doctor.py` |
| `terminal-security-agent` | Shell injection forensics, quoted-arg validation, and paste-jacking guards | `python cli/terminal_security.py` |
| `repl-bridge-agent` | Python/Node/Ruby REPL orchestration, cell execution guards, and output capture | `python cli/repl_bridge.py` |
| `man-help-agent` | Man page summarization, flag inference, example harvesting, and TL;DR generation | `python cli/man_help.py` |
| `shell-benchmark-agent` | Startup time (zsh --startup), plugin cost, and prompt latency profiling | `python cli/shell_benchmark.py` |

### Server Mgmt (Linux/Mac/Win) (38)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `linux-admin-agent` | User/group/sudo, service (systemd), cron/at, and filesystem (ext4/xfs/btrfs) operations | `python cli/linux_admin.py` |
| `systemd-surgeon-agent` | Unit authoring, dependency ordering, socket activation, and journald forensics | `python cli/systemd_surgeon.py` |
| `package-manager-agent` | apt/dnf/pacman/apk/zypper — repo pinning, hold/unhold, and atomic rollback | `python cli/package_manager.py` |
| `kernel-tuner-agent` | sysctl, cgroups v2, io-queue, hugepages, and perf/eBPF perf analysis | `python cli/kernel_tuner.py` |
| `network-ops-agent` | iptables/nftables, ip route, DNS (systemd-resolved/Unbound), and mtr forensics | `python cli/network_ops.py` |
| `storage-raid-agent` | RAID/LVM/ZFS/btrfs, fstab, mount guards, and SMART failure prediction | `python cli/storage_raid.py` |
| `log-rotation-agent` | logrotate/journal vacuuming, retention budgets, and centralized shipper wiring | `python cli/log_rotation.py` |
| `backup-restore-agent` | rsync/restic/borg, push vs pull, encryption, and restore drill verification | `python cli/backup_restore.py` |
| `sec-hardening-agent` | CIS benchmarks, Lynis scoring, fail2ban, AppArmor/SELinux, and auditd | `python cli/sec_hardening.py` |
| `container-ops-agent` | Docker/Podman, cgroups, overlayfs, rootless, and image provenance (cosign) | `python cli/container_ops.py` |
| `k8s-pilot-agent` | kubectl, helm, Kustomize, CNI/CSI forensics, and etcd backup/restore | `python cli/k8s_pilot.py` |
| `nginx-ops-agent` | vhosts, upstreams, mTLS, rate-limit, and config test/ reload choreography | `python cli/nginx_ops.py` |
| `macos-admin-agent` | launchd, defaults, profiles, MDM, SIP/TCC, and `systemextensionsctl` | `python cli/macos_admin.py` |
| `brew-ops-agent` | Formula/cask lifecycle, pin, bottle vs source, and cleanup/doctor diagnostics | `python cli/brew_ops.py` |
| `xcode-ops-agent` | xcodebuild, simulators, provisioning, notarization, and SPM resolution | `python cli/xcode_ops.py` |
| `macos-security-agent` | Gatekeeper, XProtect, TCC db, keychain, and Endpoint Security framework | `python cli/macos_security.py` |
| `windows-admin-agent` | Registry, services (sc.exe), Task Scheduler, and NTFS/ACL forensics | `python cli/windows_admin.py` |
| `powershell-forge-agent` | Module authoring, DSC, remoting (WinRM), and execution policy forensics | `python cli/powershell_forge.py` |
| `winget-choco-agent` | Package resolution, silent install flags, and winget source pinning | `python cli/winget_choco.py` |
| `windows-security-agent` | Defender, AppLocker/WDAC, Credential Guard, and event log forensics | `python cli/windows_security.py` |
| `ad-identity-agent` | Active Directory/GPO, Entra ID sync, LDAP, and Kerberos ticket forensics | `python cli/ad_identity.py` |
| `ci-cd-orchestrator-agent` | GitHub Actions/GitLab CI/CircleCI, cache-hit optimization, and runner fleet sizing | `python cli/ci_cd_orchestrator.py` |
| `observability-stack-agent` | Prometheus/Grafana/OTel/Loki, SLO burn, and cardinality explosion guards | `python cli/observability_stack.py` |
| `infra-provisioner-agent` | Terraform/OpenTofu, state locking, drift detection, and provider pinning | `python cli/infra_provisioner.py` |
| `ansible-pilot-agent` | Playbook linting, idempotency verification, vault, and inventory forensics | `python cli/ansible_pilot.py` |
| `tls-cert-agent` | ACME/Let's Encrypt, chain validation, OCSP, and cert-rotation without downtime | `python cli/tls_cert.py` |
| `db-ops-agent` | Postgres/MySQL/Redis — vacuum/replication/latency, slow-query forensics, backup PITR | `python cli/db_ops.py` |
| `queue-ops-agent` | Kafka/RabbitMQ/SQS — partition lag, dead-letter triage, and exactly-once forensics | `python cli/queue_ops.py` |
| `cdn-edge-agent` | Cache keys, purge, stale-while-revalidate, and edge function forensics | `python cli/cdn_edge.py` |
| `incident-ops-agent` | On-call handoff, status page, postmortem, and runbook-as-code | `python cli/incident_ops.py` |
| `cost-ops-agent` | Tagging hygiene, idle/oversized detection, reservation modeling, and showback | `python cli/cost_ops.py` |
| `compliance-ops-agent` | SOC2/HIPAA evidence, CIS drift, and continuous audit trails | `python cli/compliance_ops.py` |
| `secrets-ops-agent` | Vault/1Password/AWS Secrets Manager rotation, lease scoping, and break-glass drills | `python cli/secrets_ops.py` |
| `gitops-pilot-agent` | ArgoCD/Flux, drift vs desired, sync waves, and progressive delivery analysis | `python cli/gitops_pilot.py` |
| `edge-iot-agent` | Fleet OTA, MQTT, secure boot attestation, and offline-queue draining | `python cli/edge_iot.py` |
| `perf-lab-agent` | CPU flame graphs, heap profiles, io_uring, and p95 regression gates | `python cli/perf_lab.py` |
| `disaster-recovery-agent` | RTO/RPO math, pilot-light vs warm-standby, and chaos-day runbooks | `python cli/disaster_recovery.py` |
| `migration-ops-agent` | Lift-and-shift vs replatform, data gravity, cutover windows, and rollback rehearsals | `python cli/migration_ops.py` |

All 100: `python agents/<slug>/cli/<module>.py --help` from any cwd; engines expose `analyze(text, os_hint)` + `format_report`; `tests/test_computer100_agents.py` (6 tests).


---

## 🧑‍💼 50 HR / HRBP / L&D Deep Series — Highest Wanted & Searched

*50 HR-grade agents — top global demand: HRBP, skills-based org, TNA, instructional/blended/cohort, Kirkpatrick/ROI, 9-box/succession, people analytics, DEI/wellbeing. Same contract: SKILL.md + core engine + CLI + smoke tests, with PII/bias guardrails.*

### HRBP & Strategic Partnering (12)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `hrbp-strategic-partner-agent` | End-to-end HRBP business partnering: stakeholder alignment, diagnostic, and value-tracked action plans | `python cli/hrbp_strategic_partner.py` |
| `org-effectiveness-agent` | Org health & effectiveness audit with spans/layers, decision rights, and friction heatmaps | `python cli/org_effectiveness.py` |
| `change-champion-agent` | ADKAR-based change readiness, adoption curves, sponsor mapping, and comms cadence | `python cli/change_champion.py` |
| `business-alignment-agent` | HR→business OKR cascade, strategy translation, and quarterly business review narratives | `python cli/business_alignment.py` |
| `stakeholder-influence-agent` | Power/interest mapping, influence paths, and coalition building for HR initiatives | `python cli/stakeholder_influence.py` |
| `workforce-shaping-agent` | Scenario-based workforce shaping: demand/supply gaps, build/buy/borrow/bot tradeoffs | `python cli/workforce_shaping.py` |
| `hrbp-coaching-agent` | HRBP as coach: GROW-based leader coaching, contracting, and impact evidence | `python cli/hrbp_coaching.py` |
| `transformation-lead-agent` | HR operating model & digital transformation roadmaps with maturity staging | `python cli/transformation_lead.py` |
| `people-analytics-storyteller-agent` | People analytics → executive narrative: hypothesis, viz choice, and so-what | `python cli/people_analytics_storyteller.py` |
| `strategic-workforce-advisor-agent` | Strategic workforce planning (SWP): 3-horizon headcount and skills forecast | `python cli/strategic_workforce_advisor.py` |
| `hr-risk-compliance-agent` | Employment law, policy compliance, audit readiness, and mitigation playbooks | `python cli/hr_risk_compliance.py` |
| `future-of-work-architect-agent` | Hybrid/remote, skills-based org, and AI-augmented work design | `python cli/future_of_work_architect.py` |

### Talent & Hiring Excellence (6)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `talent-intelligence-agent` | Market talent mapping, competitor flow, and availability/cost heatmaps | `python cli/talent_intelligence.py` |
| `employer-value-agent` | EVP articulation, employer brand audit, and career site narratives | `python cli/employer_value.py` |
| `candidate-experience-agent` | Candidate journey mapping, friction scoring, and NPS recovery | `python cli/candidate_experience.py` |
| `hiring-manager-enablement-agent` | Hiring manager intake, calibration, and inclusive interviewing capability | `python cli/hiring_manager_enablement.py` |
| `assessment-validation-agent` | Selection assessment design, adverse impact, reliability/validity, and fairness | `python cli/assessment_validation.py` |
| `internal-mobility-marketplace-agent` | Internal talent marketplace: skills inference, matching, and career nudges | `python cli/internal_mobility_marketplace.py` |

### Performance, Succession & Career (7)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `performance-enablement-agent` | Continuous performance enablement vs annual review: check-ins, feed-forward, and calibration | `python cli/performance_enablement.py` |
| `goal-alignment-agent` | Goal cascade, OKR quality, measurability, and vertical/horizontal alignment | `python cli/goal_alignment.py` |
| `feedback-culture-agent` | Feedback cadence, psychological safety, and 360/peer feedback systems | `python cli/feedback_culture.py` |
| `nine-box-talent-agent` | 9-box facilitation, placement, bias flags, and development vs reward actions | `python cli/nine_box_talent.py` |
| `succession-risk-agent` | Bench strength, flight risk, succession slate health, and mitigation | `python cli/succession_risk.py` |
| `career-mobility-agent` | Career lattices, progression frameworks, and internal mobility pathways | `python cli/career_mobility.py` |
| `talent-calibration-agent` | Cross-team talent calibration, distribution health, and bias-safe facilitation | `python cli/talent_calibration.py` |

### Learning Strategy & Skills (6)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `learning-needs-diagnostician-agent` | TNA done right: performance gap → learning vs non-learning root cause | `python cli/learning_needs_diagnostician.py` |
| `skills-ontology-agent` | Skills taxonomy/ontology design, dedup, proficiency scales, and inference | `python cli/skills_ontology.py` |
| `capability-planner-agent` | Future capability planning: critical roles × skills × time horizon matrix | `python cli/capability_planner.py` |
| `learning-strategy-architect-agent` | L&D strategy & operating model: build/buy, governance, and portfolio balance | `python cli/learning_strategy_architect.py` |
| `learning-ecosystem-agent` | Ecosystem curation: LMS/LXP, content, cohorts, mentoring, and social | `python cli/learning_ecosystem.py` |
| `future-skills-scout-agent` | Horizon scanning for emerging skills with adjacency and decay rates | `python cli/future_skills_scout.py` |

### Learning Design & Delivery (8)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `instructional-architect-agent` | ADDIE/SAM, learning objectives (Bloom), and assessment alignment | `python cli/instructional_architect.py` |
| `blended-learning-agent` | Blended journeys: pre-work → live → practice → reinforcement spacing | `python cli/blended_learning.py` |
| `cohort-learning-agent` | Cohort-based courses: pacing, peer learning, accountability, and community | `python cli/cohort_learning.py` |
| `social-learning-agent` | Social learning: community of practice, UGC, and expert network activation | `python cli/social_learning.py` |
| `microlearning-crafter-agent` | Microlearning & nudges: spacing, retrieval practice, and in-flow performance support | `python cli/microlearning_crafter.py` |
| `scenario-simulation-agent` | Branching scenarios & simulations: consequence design and skill transfer | `python cli/scenario_simulation.py` |
| `video-learning-producer-agent` | Learning video production: scripting, retention hooks, and chaptered delivery | `python cli/video_learning_producer.py` |
| `facilitation-master-agent` | Elite facilitation: session design, energy arcs, and difficult-room handling | `python cli/facilitation_master.py` |

### Learning Measurement & Ops (5)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `learning-analytics-agent` | Learning analytics: completion → behavior → business KPI chain | `python cli/learning_analytics.py` |
| `kirkpatrick-evaluator-agent` | Levels 1-4 with leading indicators, control groups, and attribution guardrails | `python cli/kirkpatrick_evaluator.py` |
| `learning-roi-agent` | Phillips ROI: cost capture, monetized benefits, and ROI/story for CFO | `python cli/learning_roi.py` |
| `lms-ops-agent` | LMS/LXP ops: catalog hygiene, assignments, compliance tracking, and integrations | `python cli/lms_ops.py` |
| `learning-vendor-agent` | Vendor selection, SOW/quality gates, and build-vs-buy decisions | `python cli/learning_vendor.py` |

### Culture, Engagement & Wellbeing (6)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `listening-strategy-agent` | Listening architecture: census/pulse/lifecycle/moment plus closed-loop | `python cli/listening_strategy.py` |
| `recognition-rituals-agent` | Recognition systems: peer, milestone, and values-tied rituals | `python cli/recognition_rituals.py` |
| `inclusion-belonging-agent` | Belonging diagnostics, moments that matter, and intervention sequencing | `python cli/inclusion_belonging.py` |
| `wellbeing-strategist-agent` | Wellbeing pillars, program portfolio, and manager enablement | `python cli/wellbeing_strategist.py` |
| `resilience-burnout-agent` | Burnout signals, workload forensics, recovery sprints, and resilience skills | `python cli/resilience_burnout.py` |
| `team-effectiveness-agent` | Team health: trust, clarity, dynamics, and Lencioni-style friction mapping | `python cli/team_effectiveness.py` |

All 50: `python agents/<slug>/cli/<module>.py --help` from any cwd; engines `analyze(text)` + `format_report`; `tests/test_hr50_agents.py` (6 tests).


---

## 📱🎬 70 Social & Video Generation Series — LinkedIn / Instagram / X / YouTube / TikTok + Freebie + Gemini

*70 social/video agents — platform-aware, hook/CTA, license hygiene, ToS throttling. Same contract: SKILL.md + core engine + CLI + smoke tests.*

### LinkedIn — Control, Automation & Growth (12)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `linkedin-scheduler-agent` | Queue, calendar, timezone-aware publishing, and cross-post guards for LinkedIn | `python cli/linkedin_scheduler.py` |
| `linkedin-dm-funnel-agent` | Connection → DM → meeting funnel with personalization and safety throttles | `python cli/linkedin_dm_funnel.py` |
| `linkedin-analytics-radar-agent` | SSI, impressions→leads, dwell-time, and creator-mode telemetry | `python cli/linkedin_analytics_radar.py` |
| `linkedin-lead-scraper-agent` | Compliant prospect discovery, Sales Navigator filters, and enrichment hygiene | `python cli/linkedin_lead_scraper.py` |
| `linkedin-company-page-agent` | Page admin, showcase pages, employee advocacy, and analytics rollup | `python cli/linkedin_company_page.py` |
| `linkedin-newsletter-architect-agent` | Newsletter cadence, issue scaffolding, and subscriber growth loops | `python cli/linkedin_newsletter_architect.py` |
| `linkedin-live-producer-agent` | Live event run-of-show, speaker comms, and replay repurposing | `python cli/linkedin_live_producer.py` |
| `linkedin-ads-optimizer-agent` | Campaign, audience, bid, and creative fatigue for LinkedIn Ads | `python cli/linkedin_ads_optimizer.py` |
| `linkedin-outreach-sequencer-agent` | Value-first sequenced outreach with reply detection and CRM sync | `python cli/linkedin_outreach_sequencer.py` |
| `linkedin-personal-brand-agent` | POV mining from commits/work, voice calibration, and authority cadence | `python cli/linkedin_personal_brand.py` |
| `linkedin-event-networker-agent` | Event attendee mapping, warm-intro paths, and post-event follow-up | `python cli/linkedin_event_networker.py` |
| `linkedin-poll-viral-agent` | Poll hooks, comment-velocity design, and algorithm-friendly timing | `python cli/linkedin_poll_viral.py` |

### Instagram — Control, Automation & Growth (12)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `insta-reels-virality-agent` | Hook-window, sound sync, loop-rate, and retention editing for Reels | `python cli/insta_reels_virality.py` |
| `insta-grid-planner-agent` | Grid aesthetics, color-story, alt-text, and carousel sequencing | `python cli/insta_grid_planner.py` |
| `insta-story-architect-agent` | Story arcs, stickers, polls, swipe-ups, and highlight hygiene | `python cli/insta_story_architect.py` |
| `insta-hashtag-lab-agent` | Hashtag tiering, banned-tag audit, and reach vs niche balance | `python cli/insta_hashtag_lab.py` |
| `insta-dm-automation-agent` | Story-reply → DM, keyword triggers, and human-handoff | `python cli/insta_dm_automation.py` |
| `insta-influencer-match-agent` | Audience overlap, fake-follower audit, and brief→deliverable tracking | `python cli/insta_influencer_match.py` |
| `insta-shop-optimizer-agent` | Product tags, catalog hygiene, and DM→checkout drop analysis | `python cli/insta_shop_optimizer.py` |
| `insta-analytics-insights-agent` | Reach/saves/shares, follower activity windows, and content mix audit | `python cli/insta_analytics_insights.py` |
| `insta-ads-launcher-agent` | Creative variants, audience, placements, and incrementality for IG Ads | `python cli/insta_ads_launcher.py` |
| `insta-ugc-harvester-agent` | UGC discovery, rights requests, and repurpose queue | `python cli/insta_ugc_harvester.py` |
| `insta-comment-guardian-agent` | Toxicity, spam, and brand-safety moderation with allowlists | `python cli/insta_comment_guardian.py` |
| `insta-live-commerce-agent` | Live shopping run-of-show, drops, and checkout telemetry | `python cli/insta_live_commerce.py` |

### X.com — Control, Automation & Growth (12)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `x-thread-architect-agent` | Hook + pacing + cliffhangers for long-form X threads | `python cli/x_thread_architect.py` |
| `x-reply-bot-agent` | Reply-guy strategy, context-aware replies, and rate-limit safety | `python cli/x_reply_bot.py` |
| `x-list-intel-agent` | List curation, signal vs noise, and DM-able prospect surfacing | `python cli/x_list_intel.py` |
| `x-spaces-producer-agent` | Spaces agenda, speaker queue, and clip harvesting | `python cli/x_spaces_producer.py` |
| `x-trend-jacker-agent` | Trend velocity, angle fit, and safe trend-jacking timing | `python cli/x_trend_jacker.py` |
| `x-dm-funnel-agent` | Public → DM permission, value ladders, and auto-qualify | `python cli/x_dm_funnel.py` |
| `x-analytics-pulse-agent` | Views, bookmarks, profile clicks, and follower quality | `python cli/x_analytics_pulse.py` |
| `x-ads-booster-agent` | Creative fatigue, bid, audience, and brand-safety for X Ads | `python cli/x_ads_booster.py` |
| `x-search-scraper-agent` | Advanced search operators, saved searches, and lead/theme mining | `python cli/x_search_scraper.py` |
| `x-community-cultivator-agent` | Community notes, member roles, and UGC flywheel on X | `python cli/x_community_cultivator.py` |
| `x-toxicity-shield-agent` | Harassment, dogpiling, and shadow-ban risk detection | `python cli/x_toxicity_shield.py` |
| `x-viral-hook-lab-agent` | Hook scoring, pattern-bending, and timing optimization | `python cli/x_viral_hook_lab.py` |

### YouTube — Control, Automation & Growth (12)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `youtube-channel-architect-agent` | Channel positioning, trailer, playlists, and subscribe triggers | `python cli/youtube_channel_architect.py` |
| `youtube-shorts-virality-agent` | Hook-window, loop, and binge-path for Shorts | `python cli/youtube_shorts_virality.py` |
| `youtube-seo-optimizer-agent` | Title/tags/chapters, search vs suggested, and CTR from impressions | `python cli/youtube_seo_optimizer.py` |
| `youtube-thumbnail-forge-agent` | Thumbnail contrast, face/eyes, text sparsity, and A/B planning | `python cli/youtube_thumbnail_forge.py` |
| `youtube-chapter-optimizer-agent` | Chaptering, key moments, and seek-intent mapping | `python cli/youtube_chapter_optimizer.py` |
| `youtube-live-ops-agent` | Live run-of-show, chat moderation, and super-chat funnel | `python cli/youtube_live_ops.py` |
| `youtube-membership-monetizer-agent` | Memberships, perks, and churn reduction for YT | `python cli/youtube_membership_monetizer.py` |
| `youtube-analytics-sentinel-agent` | Retention curves, traffic sources, and returning vs new | `python cli/youtube_analytics_sentinel.py` |
| `youtube-comment-manager-agent` | Pinned comment, heart/reply strategy, and toxic filtering | `python cli/youtube_comment_manager.py` |
| `youtube-collab-scout-agent` | Collab fit, audience overlap, and cross-promo planning | `python cli/youtube_collab_scout.py` |
| `youtube-repurpose-engine-agent` | Long→Shorts→Threads atomization and platform reformat | `python cli/youtube_repurpose_engine.py` |
| `youtube-ads-roi-agent` | TrueView, CPM/CPV, view-through, and creative fatigue for YT Ads | `python cli/youtube_ads_roi.py` |

### TikTok — Virality & Commerce (10)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `tiktok-sound-trend-agent` | Sound velocity, dance/format fit, and early-jacking timing | `python cli/tiktok_sound_trend.py` |
| `tiktok-shop-affiliate-agent` | Shop product tags, affiliate match, and commission telemetry | `python cli/tiktok_shop_affiliate.py` |
| `tiktok-live-commerce-agent` | Live run-of-show, gifting, and shop conversion | `python cli/tiktok_live_commerce.py` |
| `tiktok-duet-stitch-agent` | Duet/stitch hooks, response framing, and collab etiquette | `python cli/tiktok_duet_stitch.py` |
| `tiktok-analytics-radar-agent` | Completion rate, rewatch, and follower activity heatmaps | `python cli/tiktok_analytics_radar.py` |
| `tiktok-ads-spark-agent` | Spark Ads, creator licensing, and whitelisting workflow | `python cli/tiktok_ads_spark.py` |
| `tiktok-creator-scout-agent` | Creator discovery, authenticity, and brief→post tracking | `python cli/tiktok_creator_scout.py` |
| `tiktok-script-lab-agent` | 3-sec hook, pattern interrupts, and CTA tailoring | `python cli/tiktok_script_lab.py` |
| `tiktok-hashtag-virality-agent` | Hashtag tiering, challenge fit, and banned-tag hygiene | `python cli/tiktok_hashtag_virality.py` |
| `tiktok-comment-moderator-agent` | Spam, hate, and brand-safety moderation at TikTok scale | `python cli/tiktok_comment_moderator.py` |

### Video Generation — Freebie Sources + Gemini/VeO (12)
| Sub-Agent | What it does | CLI |
|---|---|---|
| `free-stock-scout-agent` | Discover free stock video/images across Pexels/Pixabay/Unsplash/Mixkit/Coverr with license filters | `python cli/free_stock_scout.py` |
| `pexels-pipeline-agent` | Pexels API search, pagination, download, and attribution assembly | `python cli/pexels_pipeline.py` |
| `pixabay-curator-agent` | Pixabay curation, duration/orientation filters, and safe-search guards | `python cli/pixabay_curator.py` |
| `mixkit-video-forge-agent` | Mixkit catalog, cut-downs, and no-attribution clip hygiene | `python cli/mixkit_video_forge.py` |
| `gemini-video-producer-agent` | Gemini/VeO prompt → storyboard → clip plan with cost/latency awareness | `python cli/gemini_video_producer.py` |
| `gemini-script-to-video-agent` | Script → Gemini scene prompts → shot list + B-roll mapping from free stock | `python cli/gemini_script_to_video.py` |
| `veo-storyboard-agent` | Veo 3 prompts, camera moves, and continuity guards | `python cli/veo_storyboard.py` |
| `free-audio-scout-agent` | Free music/SFX (Pixabay Music, Mixkit, YouTube Audio Library) with license hygiene | `python cli/free_audio_scout.py` |
| `subtitle-auto-agent` | Whisper-style timing, speaker diarization, and SRT/VTT export | `python cli/subtitle_auto.py` |
| `video-remixer-free-agent` | Free-source remix: cuts, transitions, and Ken Burns with no-stock watermark | `python cli/video_remixer_free.py` |
| `ai-avatar-free-agent` | Free avatar/voice (Gemini + open tools) with consent and disclosure guards | `python cli/ai_avatar_free.py` |
| `gemini-thumbnail-gen-agent` | Gemini/Imagen thumbnail prompts, text sparsity, and CTR hypothesis | `python cli/gemini_thumbnail_gen.py` |

All 70: `python agents/<slug>/cli/<module>.py --help` from any cwd; engines `analyze(text)` + `format_report`; `tests/test_social70_agents.py` (6 tests).

## ⚡ CLI Hub Discovery

```bash
agent-architect list-agents
```
