"""
Handoff Protocol (OpenAI Agents SDK doctrine).

- Agents expose handoffs as `transfer_to_<agent>` tools the model can call.
- `on_handoff` callback fires on transfer; typed handoff inputs carry structured
  context (e.g. escalation reason); input filters control what history the
  receiver sees (trim tools, summarize, or pass through).
- Manager pattern (agents-as-tools) keeps coordinator control; peer handoffs
  transfer control fully. Both are supported here.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Sequence

from .llm.providers import Message, Role


class HandoffScope(str, Enum):
    PEER = "peer"        # control fully transfers to destination
    MANAGER = "manager"  # destination runs as a tool; control returns


@dataclass
class HandoffRequest:
    from_agent: str
    to_agent: str
    input_data: Optional[Dict[str, Any]] = None  # typed handoff args (e.g. escalation reason)
    scope: HandoffScope = HandoffScope.PEER
    history: List[Message] = field(default_factory=list)
    handoff_id: str = field(default_factory=lambda: f"ho_{uuid.uuid4().hex[:8]}")
    ts: float = field(default_factory=time.time)


@dataclass
class HandoffResult:
    request: HandoffRequest
    output: Any = None
    accepted: bool = True
    notes: str = ""


class InputFilter:
    """Controls what of the conversation the receiving agent sees."""

    def __init__(self, drop_tool_messages: bool = False, max_messages: Optional[int] = None,
                 summarize_older: bool = False):
        self.drop_tool_messages = drop_tool_messages
        self.max_messages = max_messages
        self.summarize_older = summarize_older

    def apply(self, history: Sequence[Message]) -> List[Message]:
        msgs = list(history)
        if self.drop_tool_messages:
            msgs = [m for m in msgs if m.role != Role.TOOL]
        if self.max_messages is not None and len(msgs) > self.max_messages:
            dropped = len(msgs) - self.max_messages
            head, tail = msgs[:dropped], msgs[dropped:]
            summary = Message(
                role=Role.SYSTEM,
                content=f"[HANDOFF SUMMARY] {dropped} earlier messages elided. "
                        f"Key points: " + " | ".join((m.content or "")[:80] for m in head if m.content)[:500],
            )
            msgs = [summary] + tail
        return msgs


class Handoff:
    """A single declarative handoff edge: source -> destination."""

    def __init__(
        self,
        destination: str,
        description: str = "",
        input_type: Optional[Dict[str, Any]] = None,  # JSON schema for handoff args
        on_handoff: Optional[Callable[[HandoffRequest], None]] = None,
        input_filter: Optional[InputFilter] = None,
        scope: HandoffScope = HandoffScope.PEER,
        is_enabled: bool = True,
    ):
        self.destination = destination
        self.description = description or f"Transfer the conversation to {destination}."
        self.input_type = input_type
        self.on_handoff = on_handoff
        self.input_filter = input_filter or InputFilter()
        self.scope = scope
        self.is_enabled = is_enabled

    def to_tool_declaration(self) -> Dict[str, Any]:
        """Expose as `transfer_to_<agent>` tool for the model."""
        schema = self.input_type or {"type": "object", "properties": {}}
        return {
            "name": f"transfer_to_{self.destination}",
            "description": self.description,
            "parameters": schema,
        }


class HandoffRegistry:
    """
    Per-agent handoff sets + shared execution semantics:
    - fires on_handoff callbacks
    - applies input filters to the transferred history
    - records an audit trail of every transfer
    """

    def __init__(self) -> None:
        self._handoffs: Dict[str, List[Handoff]] = {}
        self.trail: List[Dict[str, Any]] = []

    def add(self, source_agent: str, handoff: Handoff) -> None:
        self._handoffs.setdefault(source_agent, []).append(handoff)

    def available(self, source_agent: str) -> List[Handoff]:
        return [h for h in self._handoffs.get(source_agent, []) if h.is_enabled]

    def tool_declarations(self, source_agent: str) -> List[Dict[str, Any]]:
        return [h.to_tool_declaration() for h in self.available(source_agent)]

    def execute(self, request: HandoffRequest) -> HandoffResult:
        candidates = {h.destination: h for h in self.available(request.from_agent)}
        handoff = candidates.get(request.to_agent)
        if handoff is None:
            result = HandoffResult(request=request, accepted=False,
                                   notes=f"no handoff from '{request.from_agent}' to '{request.to_agent}'")
            self.trail.append({"handoff_id": request.handoff_id, "accepted": False, "ts": request.ts})
            return result

        request.history = handoff.input_filter.apply(request.history)
        if handoff.on_handoff:
            handoff.on_handoff(request)

        self.trail.append(
            {
                "handoff_id": request.handoff_id,
                "from": request.from_agent,
                "to": request.to_agent,
                "scope": request.scope.value,
                "accepted": True,
                "ts": request.ts,
                "input_keys": list((request.input_data or {}).keys()),
            }
        )
        return HandoffResult(request=request, accepted=True, notes="control transferred")
