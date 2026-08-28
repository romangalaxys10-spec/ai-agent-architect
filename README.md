# 🧠 AI Agent Architect
### *Create Your Powerful Agents — From Scratch to Maximum*

[![CI](https://github.com/romangalaxys10-spec/ai-agent-architect/actions/workflows/ci.yml/badge.svg)](https://github.com/romangalaxys10-spec/ai-agent-architect/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Agents Hub: 14 Active Sub-Agents](https://img.shields.io/badge/Agents%20Hub-14%20Active%20Agents-brightgreen.svg)]()
[![Steve Jobs DNA](https://img.shields.io/badge/Design-Insanely%20Great-black.svg)]()

> **"An AI Agent is not a chatbot with a system prompt. It is an autonomous cognitive engine built with uncompromising taste, radical focus, and resilient architecture."**

---

## 🌟 Overview

**AI Agent Architect** is a comprehensive, production-grade framework, cognitive engine, and monorepo sub-agent factory designed to architect, scaffold, test, and deploy world-class autonomous agents.

Born at the intersection of **Senior Systems Architecture**, **Skill Factory Engineering**, and the **Steve Jobs Product Philosophy**, this framework houses 14 specialized sub-agents under a unified orchestrator.

---

## 🏛️ System Architecture

```
                               ┌────────────────────────────────┐
                               │     AI AGENT ARCHITECT HUB     │
                               └───────────────┬────────────────┘
                                               │
        ┌───────────────────┬──────────────────┼───────────────────┬───────────────────┐
        ▼                   ▼                  ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐  ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ SuperDesign   │   │ SolanaStream  │  │ LinkedIn      │   │ Discord Radar │   │ ProductLaunch │
│ Agent (v2.0)  │   │ Sentinel      │  │ Intent Sniper │   │ Community     │   │ Orchestrator  │
└───────────────┘   └───────────────┘  └───────────────┘   └───────────────┘   └───────────────┘
 (Anti-AI-Slop)      (gRPC + Sniff)     (B2B Outreach)      (Telemetry Lead)    (Show HN / PH)
```

---

## 🏭 Agents Factory: Specialized Sub-Agent Suite

All specialized sub-agents are housed inside the [`agents/`](./agents) directory, each equipped with its own `SKILL.md`, CLI tools, core logic, and test suites.

### 2. 🎨 Design, Product & Telemetry
* **`superdesign-agent`**: 100% credit-free design engine producing responsive websites, 16:9 keynote decks, and Teenage Engineering telemetry HUDs with built-in `AntiSlopAuditor`. (`agents/superdesign-agent`)
* **`steve-jobs-agent`**: Product taste and radical focus sub-agent. Evaluates designs, cuts 80% bloat, enforces *The Whole Widget*, and delivers binary quality verdicts. (`agents/steve-jobs-agent`)

### 3. ⚡ Web3, Streaming & Security
* **`solana-stream-sentinel`**: Real-time Yellowstone Geyser gRPC stream parser, Meteora DLMM / Raydium pool decoder, and MEV preflight safety simulator. (`agents/solana-stream-sentinel`)
* **`binary-reverse-sentinel`**: Mach-O binary & iOS IPA security analyzer, cloud credential leak hunter (AWS, Supabase, Firebase), and private API endpoint mapper. (`agents/binary-reverse-sentinel`)

### 4. 📈 Marketing, Discord & Lead Generation
* **`linkedin-intent-sniper`**: Analyzes LinkedIn profile signals, detects technical buying intent, and drafts value-first, anti-salesy outreach messages. (`agents/linkedin-intent-sniper`)
* **`discord-community-radar`**: Real-time Discord server telemetry, paid gig/bounty signal detection, and authoritative technical reply generator. (`agents/discord-community-radar`)
* **`anti-slop-content-engine`**: Converts raw Git commits and benchmark graphs into high-CTR viral X/Twitter threads and LinkedIn case studies. (`agents/anti-slop-content-engine`)
* **`product-launch-orchestrator`**: Multi-platform launch campaign generator for GitHub repos, Show HN posts, Product Hunt launches, and Reddit developer subs. (`agents/product-launch-orchestrator`)
* **`cold-outreach-dealflow`**: Constructs 3-step high-deliverability technical email sequences, spam-word linter, and formal Statement of Work (SOW) proposals. (`agents/cold-outreach-dealflow`)

### 5. 🛠️ Architecture, Career & Financial Ops
* **`career-hunter-orchestrator`**: Ingests job descriptions, constructs ATS-optimized Markdown resumes with quantifiable metrics, and generates bespoke cover letter PDFs. (`agents/career-hunter-orchestrator`)
* **`model-bridge-router`**: Adaptive multi-model router (GLM-4.7/5.3, Claude 3.7 Sonnet, Local) with unified tool schema translation. (`agents/model-bridge-router`)
* **`invoice-billing-sentinel`**: Calculates billable hours across USD, EUR, SOL, and USDT, and renders Swiss Bauhaus vector HTML/PDF invoices. (`agents/invoice-billing-sentinel`)
* **`senior-architect-agent`**: Cognitive DAG state-machine design, modular decomposition, and zero-trust verification. (`agents/senior-architect-agent`)
* **`skill-factory-agent`**: Automated scaffolding of universal `SKILL.md` packages with verification fixtures. (`agents/skill-factory-agent`)

---

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/romangalaxys10-spec/ai-agent-architect.git
cd ai-agent-architect
pip install -e .
```

### 2. Discover All Registered Sub-Agents

```bash
agent-architect list-agents
```

### 3. Run Any Specialized Agent CLI

```bash
# Generate Swiss Anti-Slop Site
superdesign site --theme swiss_international --title "NexusFlow"

# Analyze LinkedIn Prospect Intent
python agents/linkedin-intent-sniper/cli/sniper.py snipe --name "Alex Rivera" --headline "CTO at SolanaScale"

# Scan Discord Feed for Gigs
python agents/discord-community-radar/cli/radar.py scan --msg "Looking for an engineer to build a gRPC indexer, $5k budget"

# Generate Viral Technical X Thread & LinkedIn Post
python agents/anti-slop-content-engine/cli/content.py create --topic "Zero-Credit Anti-Slop Agent Engine"

# Create Multi-Platform Launch Package
python agents/product-launch-orchestrator/cli/launch.py create --name "SuperDesign Agent"

# Generate 3-Step B2B Email Sequence
python agents/cold-outreach-dealflow/cli/dealflow.py sequence --name "Sarah Jenkins" --company "MantleFinance"
```

---

## 🧪 Running Tests

```bash
python3 -m unittest discover tests
```

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](./LICENSE) for details.
