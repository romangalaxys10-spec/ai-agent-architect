"""
Distributed OpenTelemetry-Compatible Tracing, JSONL Events & Cost Telemetry — v2.0.

Four pillars (bryanyzhu Ch.16): logs, metrics, traces, eval-as-observability.
- Tracer now emits OTel-compatible span JSON with correlation IDs and
  redaction at the trace boundary (PII never enters spans).
- JSONL structured event log (GeneArnold M1 doctrine): every llm_call /
  tool_call / completion is a machine-parseable line with latency, tokens, cost.
- CostLedger: per-model, per-agent, per-tenant cost accounting as a first-class metric.
- Trace summary + flameview-style export for offline debugging.
"""

from __future__ import annotations

import json
import os
import threading
import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, TextIO

from .guardrails import mask_pii

# OTel GenAI semantic-convention-ish attribute keys
SPAN_ATTRS = {
    "gen_ai.system": "ai-agent-architect",
    "gen_ai.operation.name": "agent_step",
}


def new_correlation_id() -> str:
    return uuid.uuid4().hex[:16]


@dataclass
class TelemetrySpan:
    span_id: str
    parent_span_id: Optional[str]
    name: str
    start_time: float
    end_time: float
    duration_ms: float
    attributes: Dict[str, Any]

    def to_otel(self, trace_id: str) -> Dict[str, Any]:
        """Render as an OTel-compatible span record."""
        return {
            "traceId": trace_id,
            "spanId": self.span_id,
            "parentSpanId": self.parent_span_id,
            "name": self.name,
            "kind": "INTERNAL",
            "startTimeUnixNano": int(self.start_time * 1e9),
            "endTimeUnixNano": int(self.end_time * 1e9),
            "durationMs": self.duration_ms,
            "attributes": {**SPAN_ATTRS, **{k: v for k, v in self.attributes.items()}},
            "status": {"code": "OK" if not self.attributes.get("error") else "ERROR"},
        }


class TelemetryTracer:
    """Traces agent lifecycle execution with OTel-compatible export + redaction."""

    def __init__(self, trace_name: str = "AgentTrace", trace_id: Optional[str] = None,
                 redact: bool = True):
        self.trace_name = trace_name
        self.trace_id = trace_id or new_correlation_id()
        self.redact = redact
        self.spans: List[TelemetrySpan] = []
        self._active_spans: Dict[str, Dict[str, Any]] = {}

    def start_span(self, name: str, parent_id: Optional[str] = None, attributes: Dict[str, Any] = None) -> str:
        span_id = f"span_{uuid.uuid4().hex[:12]}"
        self._active_spans[span_id] = {
            "name": name,
            "parent_id": parent_id,
            "start": time.time(),
            "attributes": self._scrub(attributes or {}),
        }
        return span_id

    def end_span(self, span_id: str, extra_attributes: Dict[str, Any] = None):
        if span_id in self._active_spans:
            data = self._active_spans.pop(span_id)
            end = time.time()
            dur = (end - data["start"]) * 1000
            attrs = {**data["attributes"], **self._scrub(extra_attributes or {})}
            self.spans.append(TelemetrySpan(
                span_id=span_id,
                parent_span_id=data["parent_id"],
                name=data["name"],
                start_time=data["start"],
                end_time=end,
                duration_ms=round(dur, 3),
                attributes=attrs,
            ))

    def _scrub(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Redaction at the trace boundary: PII never enters spans."""
        if not self.redact:
            return dict(attributes)
        out = {}
        for k, v in attributes.items():
            out[k] = mask_pii(v) if isinstance(v, str) else v
        return out

    # ------------------------------------------------------------------
    # Exports
    # ------------------------------------------------------------------

    def export_summary(self) -> Dict[str, Any]:
        total_ms = sum(s.duration_ms for s in self.spans)
        return {
            "trace_name": self.trace_name,
            "trace_id": self.trace_id,
            "total_spans": len(self.spans),
            "total_duration_ms": round(total_ms, 3),
            "spans": [asdict(s) for s in self.spans],
        }

    def export_otel(self) -> List[Dict[str, Any]]:
        """OTel JSON records (feed to any OTLP collector / Phoenix / Jaeger)."""
        return [s.to_otel(self.trace_id) for s in self.spans]

    def export_flameview(self) -> List[Dict[str, Any]]:
        """Waterfall rows for offline debugging."""
        t0 = self.spans[0].start_time if self.spans else 0
        rows = []
        for s in self.spans:
            rows.append({
                "name": s.name,
                "offset_ms": round((s.start_time - t0) * 1000, 2),
                "duration_ms": s.duration_ms,
                "parent": s.parent_span_id,
            })
        return rows

    def save_otel(self, path: str) -> str:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"resourceSpans": [{"spans": self.export_otel()}]}, f, indent=2)
        return path


# ---------------------------------------------------------------------------
# JSONL structured event log
# ---------------------------------------------------------------------------

class JSONLLogger:
    """
    Machine-parseable event log: one JSON object per line.
    Events: llm_call | tool_call | hitl_decision | guardrail | completion | error.
    Thread-safe; file + optional in-memory ring for tests.
    """

    def __init__(self, path: Optional[str] = None, also_memory: bool = True, max_memory: int = 5000):
        self.path = path
        self.also_memory = also_memory
        self.max_memory = max_memory
        self._ring: List[Dict[str, Any]] = []
        self._lock = threading.Lock()
        self._fh: Optional[TextIO] = None
        if path:
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            self._fh = open(path, "a", encoding="utf-8")

    def log_event(self, event_type: str, **fields: Any) -> Dict[str, Any]:
        event = {
            "ts": time.time(),
            "type": event_type,
            "event_id": uuid.uuid4().hex[:12],
            **{k: (mask_pii(v) if isinstance(v, str) else v) for k, v in fields.items()},
        }
        with self._lock:
            if self.also_memory:
                self._ring.append(event)
                if len(self._ring) > self.max_memory:
                    self._ring = self._ring[-self.max_memory:]
            if self._fh:
                self._fh.write(json.dumps(event, default=str) + "\n")
                self._fh.flush()
        return event

    def events(self, event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        if event_type is None:
            return list(self._ring)
        return [e for e in self._ring if e["type"] == event_type]

    def close(self) -> None:
        if self._fh:
            self._fh.close()


# ---------------------------------------------------------------------------
# Cost ledger
# ---------------------------------------------------------------------------

class CostLedger:
    """First-class cost accounting per model / agent / tenant."""

    def __init__(self):
        self._by_model: Dict[str, Dict[str, float]] = {}
        self._by_agent: Dict[str, Dict[str, float]] = {}
        self._lock = threading.Lock()

    def record(self, model: str, agent: str, prompt_tokens: int, completion_tokens: int, cost_usd: float):
        with self._lock:
            m = self._by_model.setdefault(model, {"tokens": 0.0, "usd": 0.0})
            m["tokens"] += prompt_tokens + completion_tokens
            m["usd"] += cost_usd
            a = self._by_agent.setdefault(agent, {"tokens": 0.0, "usd": 0.0})
            a["tokens"] += prompt_tokens + completion_tokens
            a["usd"] += cost_usd

    def total_usd(self) -> float:
        return round(sum(m["usd"] for m in self._by_model.values()), 6)

    def report(self) -> Dict[str, Any]:
        return {
            "total_usd": self.total_usd(),
            "by_model": {k: {"tokens": int(v["tokens"]), "usd": round(v["usd"], 6)} for k, v in self._by_model.items()},
            "by_agent": {k: {"tokens": int(v["tokens"]), "usd": round(v["usd"], 6)} for k, v in self._by_agent.items()},
        }


# ---------------------------------------------------------------------------
# Metrics catalog (Prometheus-style counters/gauges, dependency-free)
# ---------------------------------------------------------------------------

class MetricsRegistry:
    """Minimal counter/gauge/histogram registry with textual exposition."""

    def __init__(self):
        self._counters: Dict[str, float] = {}
        self._gauges: Dict[str, float] = {}
        self._histograms: Dict[str, List[float]] = {}
        self._lock = threading.Lock()

    def inc(self, name: str, value: float = 1.0):
        with self._lock:
            self._counters[name] = self._counters.get(name, 0.0) + value

    def gauge(self, name: str, value: float):
        with self._lock:
            self._gauges[name] = value

    def observe(self, name: str, value: float):
        with self._lock:
            self._histograms.setdefault(name, []).append(value)

    def exposition(self) -> str:
        lines = []
        for k, v in sorted(self._counters.items()):
            lines.append(f"# TYPE {k} counter\n{k} {v}")
        for k, v in sorted(self._gauges.items()):
            lines.append(f"# TYPE {k} gauge\n{k} {v}")
        for k, vals in sorted(self._histograms.items()):
            if vals:
                svals = sorted(vals)
                p50 = svals[len(svals) // 2]
                p95 = svals[min(len(svals) - 1, int(len(svals) * 0.95))]
                lines.append(f"# TYPE {k} summary\n{k}_count {len(vals)}\n{k}_p50 {p50:.3f}\n{k}_p95 {p95:.3f}")
        return "\n".join(lines)
