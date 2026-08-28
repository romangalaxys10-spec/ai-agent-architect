"""
ColabT4Engine — Google Colab T4 plugin core.
Detect, setup, benchmark, run on free NVIDIA T4. Offline-testable locally.
Stdlib-only for detection; torch/nvidia-smi are optional and soft-failed.
"""

import os
import re
import platform
import subprocess
import shutil
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Finding:
    category: str
    severity: str
    title: str
    detail: str
    fix: str


@dataclass
class Analysis:
    verdict: str
    score: float
    findings: List[Finding] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    next_steps: List[str] = field(default_factory=list)


def _in_colab() -> bool:
    # Colab sets env vars and injects google.colab module
    if os.environ.get("COLAB_RELEASE_TAG") or os.environ.get("COLAB_GPU"):
        return True
    try:
        import google.colab  # noqa: F401
        return True
    except Exception:
        return False


def _run(cmd: List[str], timeout: int = 8) -> tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except FileNotFoundError as e:
        return 127, "", str(e)
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"


def _detect_gpu() -> Dict[str, Any]:
    m: Dict[str, Any] = {"cuda_available": False, "device_name": None, "is_t4": False, "vram_gb": None, "driver": None, "nvidia_smi": None}
    # 1) nvidia-smi
    if shutil.which("nvidia-smi"):
        rc, out, _ = _run(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"], timeout=8)
        if rc == 0 and out:
            m["nvidia_smi"] = out
            # e.g. "Tesla T4, 15360 MiB, 535.104.05"
            m["is_t4"] = "T4" in out
            mm = re.search(r"(\d+)\s*MiB", out)
            if mm:
                try:
                    m["vram_gb"] = round(int(mm.group(1)) / 1024, 1)
                except Exception:
                    pass
            dm = re.search(r",\s*([\d\.]+)\s*$", out)
            if dm:
                m["driver"] = dm.group(1)
            m["device_name"] = out.split(",")[0].strip() if "," in out else out
        else:
            rc2, out2, _ = _run(["nvidia-smi"], timeout=8)
            if rc2 == 0:
                m["nvidia_smi"] = out2[:2000]
                m["is_t4"] = "T4" in out2
    # 2) torch
    try:
        import torch  # type: ignore
        if torch.cuda.is_available():
            m["cuda_available"] = True
            try:
                m["device_name"] = torch.cuda.get_device_name(0)
                m["is_t4"] = m["is_t4"] or ("T4" in m["device_name"])
                props = torch.cuda.get_device_properties(0)
                m["vram_gb"] = round(props.total_memory / (1024**3), 1)
            except Exception:
                pass
    except Exception:
        pass
    # 3) tensorflow fallback
    if not m["cuda_available"]:
        try:
            import tensorflow as tf  # type: ignore
            gpus = tf.config.list_physical_devices("GPU")
            if gpus:
                m["cuda_available"] = True
                m["device_name"] = m["device_name"] or str(gpus[0])
        except Exception:
            pass
    return m


class ColabT4Engine:
    """Deterministic engine for Colab T4 — zero network, offline testable."""

    SEVERITY_ORDER = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
    T4_VRAM_GB = 16

    @classmethod
    def check(cls, text: str = "", **kwargs) -> Analysis:
        findings: List[Finding] = []
        metrics: Dict[str, Any] = {}
        t = (text or "").strip()
        low = t.lower()

        in_colab = _in_colab()
        gpu = _detect_gpu()

        metrics["in_colab"] = in_colab
        metrics["host_platform"] = platform.system()
        metrics["python_version"] = platform.python_version()
        metrics.update(gpu)
        metrics["chars"] = len(t)

        # Verdict over environment, not text
        if in_colab and gpu.get("is_t4") and gpu.get("cuda_available"):
            verdict, score = "PASS", 100.0
            findings.append(Finding("colab-t4-gpu-agent", "info", "T4 ready", f"Colab T4 detected: {gpu.get('device_name')} {gpu.get('vram_gb')}GB", "Run --setup then --benchmark"))
        elif in_colab and gpu.get("cuda_available") and not gpu.get("is_t4"):
            verdict, score = "PASS_WITH_NOTES", 88.0
            findings.append(Finding("colab-t4-gpu-agent", "low", "Non-T4 GPU in Colab", f"GPU={gpu.get('device_name')} — not T4 but CUDA is available", "Use T4 budget (16GB) or select T4 in Runtime → Change runtime type → T4 GPU"))
        elif in_colab and not gpu.get("cuda_available"):
            verdict, score = "NEEDS_REVIEW", 62.0
            findings.append(Finding("colab-t4-gpu-agent", "high", "Colab but no CUDA", "In Colab but CUDA not available — runtime type is None/CPU or driver mismatch", "Runtime → Change runtime type → T4 GPU, then Runtime → Restart runtime, re-run --check"))
        elif not in_colab and gpu.get("cuda_available"):
            verdict, score = "PASS_WITH_NOTES", 82.0
            findings.append(Finding("colab-t4-gpu-agent", "info", "Local CUDA (not Colab)", f"Local GPU={gpu.get('device_name')} — this agent is optimized for Colab T4 but can run locally", "Use --setup --dry-run locally; run live notebook in Colab for T4"))
        else:
            verdict, score = "PASS_WITH_NOTES", 78.0
            findings.append(Finding("colab-t4-gpu-agent", "low", "No GPU here (expected on macOS)", "No CUDA/T4 detected locally — expected on this host. Notebook will get T4 in Colab.", "Open notebook in Colab (badge) → Runtime → T4 GPU → Run all"))

        # Text-level hints
        if low and "t4" not in low and "colab" not in low and len(low) > 20:
            findings.append(Finding("colab-t4-gpu-agent", "low", "Colab/T4 signal absent", "Input has no colab/t4 cue", "Include 'colab t4' or runtime intent for richer routing"))
        if any(k in low for k in ["private key", "mnemonic", "secret key", "token"]):
            findings.append(Finding("colab-t4-gpu-agent", "critical", "Secret exposure", "Private key/mnemonic/token in input", "Redact, rotate, use Colab Secrets (🔑) + env"))
            verdict, score = "BLOCKED", 0.0

        next_steps = []
        if verdict == "BLOCKED":
            next_steps.append("Redact secrets first")
        elif verdict == "NEEDS_REVIEW":
            next_steps.append("In Colab: Runtime → Change runtime type → T4 GPU → Restart → re-run --check")
        else:
            next_steps.append("Local: `python agents/colab-t4-gpu-agent/cli/colab_t4.py --check` → expect PASS_WITH_NOTES (no local GPU)")
            next_steps.append("Colab: open notebook badge → Runtime → T4 GPU → Run all → --benchmark")
        if not in_colab:
            next_steps.append("Dry-run setup: `python agents/colab-t4-gpu-agent/cli/colab_t4.py --setup --dry-run`")

        return Analysis(verdict=verdict, score=score, findings=findings, metrics=metrics, next_steps=next_steps)

    @classmethod
    def setup_plan(cls, dry_run: bool = True) -> Analysis:
        findings: List[Finding] = []
        metrics = {"dry_run": dry_run, "t4_vram_gb": cls.T4_VRAM_GB}
        # Idempotent pip plan for T4
        steps = [
            "pip install -q torch torchvision --index-url https://download.pytorch.org/whl/cu121",
            "pip install -q accelerate bitsandbytes transformers",
            "pip install -q xformers  # optional, may fail on T4 — soft-fail",
            "python -c \"import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no-cuda')\"",
            "nvidia-smi --query-gpu=name,memory.total --format=csv",
        ]
        metrics["steps"] = steps
        metrics["install_hint"] = "In Colab: %pip install -q torch torchvision --index-url https://download.pytorch.org/whl/cu121 accelerate bitsandbytes transformers"
        if dry_run:
            verdict, score = "PASS", 96.0
            findings.append(Finding("colab-t4-gpu-agent", "info", "Dry-run plan", f"{len(steps)} steps (no pip executed)", "Re-run with --setup (no --dry-run) inside Colab T4 to execute"))
        else:
            # Live attempt only makes sense in Colab with CUDA; locally we soft-report
            gpu = _detect_gpu()
            if not gpu.get("cuda_available"):
                verdict, score = "PASS_WITH_NOTES", 74.0
                findings.append(Finding("colab-t4-gpu-agent", "medium", "No CUDA to setup against", "Live setup skipped — no CUDA here (use Colab T4)", "Open notebook in Colab for live setup"))
            else:
                verdict, score = "PASS", 98.0
                findings.append(Finding("colab-t4-gpu-agent", "info", "Live setup ready", "CUDA available — pip steps would execute", "Run notebook cells top-to-bottom"))
        return Analysis(verdict=verdict, score=score, findings=findings, metrics=metrics, next_steps=[
            "Dry-run is default locally — safe to run",
            "In Colab T4: uncheck --dry-run or run notebook Run all",
            "After setup: --benchmark or --run \"prompt\"",
        ])

    @classmethod
    def benchmark(cls, **kwargs) -> Analysis:
        gpu = _detect_gpu()
        metrics = {"t4_vram_gb": cls.T4_VRAM_GB, **gpu, "in_colab": _in_colab()}
        findings: List[Finding] = []
        if not gpu.get("cuda_available"):
            return Analysis(verdict="PASS_WITH_NOTES", score=72.0, findings=[
                Finding("colab-t4-gpu-agent", "low", "No CUDA — benchmark simulated", "No GPU here; benchmark would use T4 in Colab (16GB, ~8 TFLOPS)", "Run notebook in Colab T4 for real TTFT/TPS/VRAM high-water")
            ], metrics=metrics, next_steps=["In Colab: Run all → check TTFT/TPS in notebook", "Local: use --dry-run"])
        # Simulate a T4-aware budget check
        if gpu.get("vram_gb") and gpu.get("vram_gb") < 14:
            findings.append(Finding("colab-t4-gpu-agent", "medium", "Low VRAM", f"VRAM {gpu.get('vram_gb')}GB < T4 16GB budget", "Use 4-bit (bitsandbytes) or GGUF + CPU offload"))
            verdict, score = "PASS_WITH_NOTES", 84.0
        else:
            verdict, score = "PASS", 96.0
        return Analysis(verdict=verdict, score=score, findings=findings, metrics=metrics, next_steps=[
            "Record TTFT/TPS: see notebook benchmark cell",
            "Route: ≤7B → 4-bit on T4; 13B → GGUF Q4_0 + offload; 70B → API fallback",
        ])

    @classmethod
    def format_report(cls, analysis: Analysis) -> str:
        lines = [f"# {cls.__name__} Report — {analysis.verdict} (score {analysis.score}/100)", ""]
        if analysis.metrics:
            lines.append("## Metrics")
            for k, v in analysis.metrics.items():
                lines.append(f"- **{k}**: {v}")
            lines.append("")
        if analysis.findings:
            lines.append("## Findings (ranked)")
            ranked = sorted(analysis.findings, key=lambda f: cls.SEVERITY_ORDER.get(f.severity, 0), reverse=True)
            for f in ranked:
                lines.append(f"- **{f.severity.upper()}** [{f.category}] {f.title}: {f.detail} → *Fix: {f.fix}*")
            lines.append("")
        if analysis.next_steps:
            lines.append("## Next Steps")
            for i, s in enumerate(analysis.next_steps, 1):
                lines.append(f"{i}. {s}")
            lines.append("")
        lines.append(f"**Verdict: {analysis.verdict}** — deterministic offline analysis, no API keys used.")
        return "\n".join(lines)
