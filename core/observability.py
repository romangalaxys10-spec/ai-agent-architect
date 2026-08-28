"""
Distributed OpenTelemetry-Compatible Tracing & Cost Telemetry.
Tracks step-by-step latency spans, token burn rates, and execution trajectories.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import time


@dataclass
class TelemetrySpan:
    span_id: str
    parent_span_id: Optional[str]
    name: str
    start_time: float
    end_time: float
    duration_ms: float
    attributes: Dict[str, Any]


class TelemetryTracer:
    """Traces agent lifecycle execution with microsecond precision."""

    def __init__(self, trace_name: str = "AgentTrace"):
        self.trace_name = trace_name
        self.spans: List[TelemetrySpan] = []
        self._active_spans: Dict[str, Dict[str, Any]] = {}

    def start_span(self, name: str, parent_id: Optional[str] = None, attributes: Dict[str, Any] = None) -> str:
        span_id = f"span_{len(self.spans) + len(self._active_spans) + 1}"
        self._active_spans[span_id] = {
            "name": name,
            "parent_id": parent_id,
            "start": time.time(),
            "attributes": attributes or {}
        }
        return span_id

    def end_span(self, span_id: str, extra_attributes: Dict[str, Any] = None):
        if span_id in self._active_spans:
            data = self._active_spans.pop(span_id)
            end = time.time()
            dur = (end - data["start"]) * 1000
            attrs = {**data["attributes"], **(extra_attributes or {})}
            self.spans.append(TelemetrySpan(
                span_id=span_id,
                parent_span_id=data["parent_id"],
                name=data["name"],
                start_time=data["start"],
                end_time=end,
                duration_ms=round(dur, 3),
                attributes=attrs
            ))

    def export_summary(self) -> Dict[str, Any]:
        total_ms = sum(s.duration_ms for s in self.spans)
        return {
            "trace_name": self.trace_name,
            "total_spans": len(self.spans),
            "total_duration_ms": round(total_ms, 3),
            "spans": [s.__dict__ for s in self.spans]
        }
