---
name: colab-t4-gpu-agent
description: 'Google Colab T4 GPU plugin — detect, setup, benchmark and run inference on free NVIDIA T4'
version: 1.0.0
author: AI Agent Architect
category: 'SysAdmin: Local LLM'
---

# Colab T4 GPU Agent

> "Google Colab T4 GPU plugin — detect, setup, benchmark and run inference on free NVIDIA T4."

**Demand basis:** Free T4 (16GB VRAM, ~8.1 TFLOPS) is the highest-searched free GPU path for local LLM/video workloads. This agent gives you detection, one-shot setup, VRAM-aware model routing, and Colab-native benchmark loops — offline-testable, then live in Colab.

## 🎯 Activation Triggers
- `colab t4`
- `colab gpu`
- `free gpu`
- `colab setup`
- `t4 benchmark`

## ⚡ Execution Protocol
1. Detect environment — Colab vs local, CUDA availability, T4 vs other (A100/V100/no-GPU) via `torch`/`nvidia-smi`.
2. Setup — idempotent `pip` for `torch+cu121`, `accelerate`, `bitsandbytes`, `xformers`, `flash-attn` guards, and VRAM budget (16GB → model/quant routing).
3. Run/benchmark — `ttft`/`tps`, VRAM high-water, and T4-aware fallbacks (4-bit, GGUF, CPU offload) with `format_report`.

## 🧠 Cognitive Depth Protocols
- `ds-deep-think`: map 3 non-obvious failure modes before run (driver, runtime restart, quota).
- `ds-adversary`: worst-case quota/OOM inputs.
- `ds-excavate`: hidden assumptions (Colab idle timeout, T4 driver).

## 🔌 I/O Contract
- **CLI:** `python agents/colab-t4-gpu-agent/cli/colab_t4.py --help`
- **Input:** `--check` (detect), `--setup` (dry-run or live), `--benchmark`, `--run "prompt"`; also `--json`
- **Output:** markdown report (verdict/score/metrics/findings/next_steps); `--json` for machine
- **Runtime:** offline deterministic locally; live CUDA only inside Colab T4. No API keys.

## 🛡️ Framework Wiring
- Guards: secret scrubbing, dry-run default, VRAM ceiling (16GB T4), 3-currency budgets.
- Observability: JSONL + cost entries via bus; OTel span per setup/bench.

## 🔗 See Also
- Hub: [`agents/AGENTS.md`](../AGENTS.md)
- Demo notebook: [`notebook/colab_t4_gpu.ipynb`](./notebook/colab_t4_gpu.ipynb)
- Plugin: [`plugin/colab_t4_plugin.py`](./plugin/colab_t4_plugin.py)
