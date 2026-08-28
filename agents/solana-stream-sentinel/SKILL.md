---
name: solana-stream-sentinel
description: Real-time on-chain Solana event sniffer, Yellowstone Geyser gRPC stream parser, Meteora/Raydium DEX instruction decoder, and MEV preflight safety simulator.
version: 1.0.0
author: AI Agent Architect
---

# Solana Stream Sentinel Sub-Agent

> "Real-time on-chain event detection, instruction decoding, and MEV-safe preflight execution on Solana."

## 🎯 Activation Triggers
- `sniff solana pool`
- `decode geyser stream`
- `simulate solana swap`
- `meteora dlmm event`
- `raydium migration sniffer`

## ⚡ Execution Protocol
1. **Stream Subscription**: Subscribe via Yellowstone gRPC / Helius LaserStream with filtered discriminators.
2. **Instruction Decoding**: Decode Anchor vs Native instruction layout and unpack pool parameters.
3. **Preflight Simulation**: Compute liquidity depth, slippage bounds, and sandwich attack risk.
4. **Execution Dispatch**: Return clean JSON telemetry payload to the caller or orchestrator.
