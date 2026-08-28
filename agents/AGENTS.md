# 🤖 Sub-Agents Hub
### *Specialized Autonomous Sub-Agents Organized Under AI Agent Architect*

All specialized sub-agents are organized in this dedicated `agents/` directory. Each sub-agent is modular, self-contained, and dynamically discoverable by the master orchestrator.

---

## 🌟 Complete Sub-Agent Catalog (65 Specialized Sub-Agents)

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

## ⚡ CLI Hub Discovery

```bash
agent-architect list-agents
```
