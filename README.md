# 🧠 AI Agent Architect
### *Create Your Powerful Agents — From Scratch to Maximum*

[![CI](https://github.com/romangalaxys10-spec/ai-agent-architect/actions/workflows/ci.yml/badge.svg)](https://github.com/romangalaxys10-spec/ai-agent-architect/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Agents Hub: 9 Sub-Agents](https://img.shields.io/badge/Agents%20Hub-9%20Active%20Agents-brightgreen.svg)]()
[![Steve Jobs DNA](https://img.shields.io/badge/Design-Insanely%20Great-black.svg)]()

> **"An AI Agent is not a chatbot with a system prompt. It is an autonomous cognitive engine built with uncompromising taste, radical focus, and resilient architecture."**

---

## 🌟 Overview

**AI Agent Architect** is a comprehensive, production-grade framework, cognitive engine, and monorepo sub-agent factory designed to architect, scaffold, test, and deploy world-class autonomous agents.

Born at the intersection of **Senior Systems Architecture**, **Skill Factory Engineering**, and the **Steve Jobs Product Philosophy**, this framework unites modular sub-agents under a central orchestrator.

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
│ SuperDesign   │   │ SolanaStream  │  │ CareerHunter  │   │ ModelBridge   │   │ BinaryReverse │
│ Agent (v2.0)  │   │ Sentinel      │  │ Orchestrator  │   │ Router        │   │ Sentinel      │
└───────────────┘   └───────────────┘  └───────────────┘   └───────────────┘   └───────────────┘
 (Anti-AI-Slop)      (gRPC + Sniff)     (ATS + CRM)         (GLM / Claude)      (Mach-O / Sec)
```

---

## 🏭 Agents Factory: Specialized Sub-Agent Suite

All specialized sub-agents are housed inside the [`agents/`](./agents) directory, each equipped with its own `SKILL.md`, CLI tools, core logic, and test suites.

### 2. 🎨 `superdesign-agent` (Anti-AI-Slop Design & Keynote Engine)
* **Location:** [`agents/superdesign-agent/`](./agents/superdesign-agent)
* **What It Does:** 100% credit-free design engine producing responsive websites, 16:9 keynote decks, and Teenage Engineering telemetry HUDs.
* **Anti-Slop Guarantee:** Built-in `AntiSlopAuditor` banishes purple gradient blobs, generic Inter fonts, and buzzwords.
* **CLI Command:** `superdesign site --theme swiss_international` | `superdesign audit --file site.html`

### 3. ⚡ `solana-stream-sentinel` (Real-Time On-Chain Stream & DEX Decoder)
* **Location:** [`agents/solana-stream-sentinel/`](./agents/solana-stream-sentinel)
* **What It Does:** Ingests Yellowstone Geyser gRPC streams, auto-decodes instruction discriminators (Meteora DLMM, Raydium CPMM/AMMv4, PumpSwap), and simulates MEV/sandwich attack preflight safety.
* **CLI Command:** `python agents/solana-stream-sentinel/cli/sentinel.py sniff`

### 4. 🎯 `career-hunter-orchestrator` (Headless Job Scout, ATS Resume & Lead CRM)
* **Location:** [`agents/career-hunter-orchestrator/`](./agents/career-hunter-orchestrator)
* **What It Does:** Scouts high-ticket engineering opportunities, constructs zero-fluff ATS-compliant Markdown resumes with quantifiable metrics, and generates bespoke cover letter PDFs.
* **CLI Command:** `python agents/career-hunter-orchestrator/cli/career.py scout --title "Senior AI Architect"`

### 5. 🧠 `model-bridge-router` (Multi-LLM GLM / Claude Adaptive Gateway)
* **Location:** [`agents/model-bridge-router/`](./agents/model-bridge-router)
* **What It Does:** Classifies task reasoning depth, routes coding tasks to GLM-4.7/5.3 and architecture to Claude 3.7 Sonnet, and normalizes function calling schemas between OpenAI and Anthropic formats.
* **CLI Command:** `python agents/model-bridge-router/cli/bridge.py route --prompt "Audit smart contract" --code`

### 6. 🛡️ `binary-reverse-sentinel` (Mach-O / IPA Security Scanner & Secret Hunter)
* **Location:** [`agents/binary-reverse-sentinel/`](./agents/binary-reverse-sentinel)
* **What It Does:** Decompiles and inspects Mach-O binaries and iOS IPAs, scans for leaked cloud credentials (AWS, Supabase, Firebase, OpenAI) with false-positive filtering, and maps hidden endpoints.
* **CLI Command:** `python agents/binary-reverse-sentinel/cli/reverser.py scan --file app.bin`

### 7. 🧾 `invoice-billing-sentinel` (Deterministic Multi-Currency Invoicing)
* **Location:** [`agents/invoice-billing-sentinel/`](./agents/invoice-billing-sentinel)
* **What It Does:** Calculates billable hours, formats balances across USD, EUR, SOL, and USDT, and renders Swiss Bauhaus vector HTML/PDF invoices ready for client delivery.
* **CLI Command:** `python agents/invoice-billing-sentinel/cli/billing.py create --client "Superteam" --hours 25`

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

### 3. Run Cognitive Loop

```python
from core.engine import AgentEngine

agent = AgentEngine(name="LeadArchitect", system_prompt="You are a senior system architect.")
result = agent.run_lifecycle("Design high-throughput distributed message bus")
print(result)
```

---

## 🧪 Running Tests

```bash
python3 -m unittest discover tests
```

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](./LICENSE) for details.
