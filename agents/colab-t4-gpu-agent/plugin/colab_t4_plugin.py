"""
colab_t4_plugin — drop-in helper for Google Colab notebooks.
Usage in Colab (T4 runtime):
  from plugin.colab_t4_plugin import setup_t4, benchmark_t4, run_prompt

Locally it degrades gracefully (dry-run / mock).
"""

import subprocess
import shutil
import sys

def _in_colab() -> bool:
    try:
        import google.colab  # noqa
        return True
    except Exception:
        return False

def setup_t4(dry_run=None) -> None:
    """One-shot T4 setup. Dry-run locally, live in Colab."""
    if dry_run is None:
        dry_run = not _in_colab()
    print(f"[colab-t4] setup_t4 dry_run={dry_run} in_colab={_in_colab()}")
    cmds = [
        "pip install -q torch torchvision --index-url https://download.pytorch.org/whl/cu121",
        "pip install -q accelerate bitsandbytes transformers",
    ]
    for c in cmds:
        if dry_run:
            print(f"  dry-run: {c}")
        else:
            print(f"  exec: {c}")
            subprocess.run(c, shell=True)
    # Verify
    try:
        import torch
        print(f"  torch.cuda.is_available()={torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"  device={torch.cuda.get_device_name(0)}")
    except Exception as e:
        print(f"  torch check skipped: {e}")
    if shutil.which("nvidia-smi"):
        subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv"],)

def benchmark_t4() -> dict:
    """Return VRAM/TTFT mock or live benchmark."""
    try:
        import torch
        cuda = torch.cuda.is_available()
        name = torch.cuda.get_device_name(0) if cuda else "no-cuda"
        vram = round(torch.cuda.get_device_properties(0).total_memory/1024**3,1) if cuda else None
        print(f"[colab-t4] benchmark cuda={cuda} device={name} vram={vram}GB")
        return {"cuda": cuda, "device": name, "vram_gb": vram}
    except Exception as e:
        print(f"[colab-t4] benchmark mock (no torch/cuda): {e}")
        return {"cuda": False, "note": "run in Colab T4 for live benchmark"}

def run_prompt(prompt: str, model: str = "Qwen/Qwen2-0.5B-Instruct") -> str:
    """Tiny LLM run — 4-bit on T4, simulated locally."""
    try:
        import torch
        if not torch.cuda.is_available():
            return f"[mock] prompt={prompt!r} — no CUDA here; live run in Colab T4 with {model}"
        from transformers import AutoModelForCausalLM, AutoTokenizer
        tok = AutoTokenizer.from_pretrained(model)
        mdl = AutoModelForCausalLM.from_pretrained(model, device_map="auto", load_in_4bit=True)
        ids = tok(prompt, return_tensors="pt").to(mdl.device)
        out = mdl.generate(**ids, max_new_tokens=64)
        return tok.decode(out[0], skip_special_tokens=True)
    except Exception as e:
        return f"[mock/error] {e} — prompt={prompt!r}"
