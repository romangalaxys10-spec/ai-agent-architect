---
name: binary-reverse-sentinel
description: Mach-O binary & iOS IPA security analyzer, cloud credential leak hunter, private API endpoint mapper, and ATS audit sub-agent.
version: 1.0.0
author: AI Agent Architect
---

# Binary Reverse Sentinel Sub-Agent

> "Automated Mach-O & iOS binary reversing, leaked credential detection, and network security mapping."

## 🎯 Activation Triggers
- `reverse binary`
- `scan ipa for secrets`
- `audit mach-o`
- `extract api endpoints`

## ⚡ Execution Protocol
1. **Binary Header & Symbol Extraction**: Parse Mach-O architecture and symbol tables.
2. **Secret Detection**: High-entropy regex scanner for AWS, Supabase, Firebase, and OpenAI API keys.
3. **Endpoint Mapping**: Extract hardcoded HTTP/WebSocket endpoints and ATS configurations.
4. **Audit Report**: Compute security score and mitigation steps.
