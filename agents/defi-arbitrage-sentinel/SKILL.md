---
name: defi-arbitrage-sentinel
description: High-Frequency DeFi & DEX Arbitrage Sentinel. Monitors price spreads across Meteora DLMM, Raydium CLMM, and Orca Whirlpools, simulating flashloan routing, slippage, and net PnL after MEV priority fees.
version: 1.0.0
author: AI Agent Architect
---

# DeFi Arbitrage Sentinel

> "Sub-millisecond cross-DEX spread scanning, flashloan capital routing, and preflight MEV safety simulation."

## 🎯 Activation Triggers
- `scan defi arbitrage`
- `compare dex prices`
- `simulate flashloan route`
- `calculate meteora vs raydium spread`

## ⚡ Core Capabilities
1. **Cross-DEX Spread Analysis**: Compares token pairs across Meteora DLMM, Raydium CLMM, and Orca Whirlpools.
2. **Flashloan PnL Simulation**: Calculates net profit after 0.09% flashloan borrowing fees and Jito priority tip fees.
3. **MEV Preflight Safety**: Verifies that price impact and slippage boundaries prevent sandwich attacks.
