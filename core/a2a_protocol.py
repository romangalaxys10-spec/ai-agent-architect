"""
Agent-to-Agent (A2A) Communication Protocol.
Standardized message envelope and distributed bus for multi-agent delegation and swarm meshes.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
import time
import uuid


@dataclass
class A2AMessage:
    sender_id: str
    recipient_id: str
    intent: str  # DELEGATE_TASK, RETURN_RESULT, REQUEST_CLARIFICATION, ADVERSARIAL_CRITIQUE
    payload: Dict[str, Any]
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: float = field(default_factory=time.time)
    message_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])


class A2AMessageBus:
    """Central message broker facilitating Agent-to-Agent communication."""

    def __init__(self):
        self._handlers: Dict[str, List[Callable[[A2AMessage], Optional[A2AMessage]]]] = {}
        self.history: List[A2AMessage] = []

    def subscribe(self, agent_id: str, handler: Callable[[A2AMessage], Optional[A2AMessage]]):
        if agent_id not in self._handlers:
            self._handlers[agent_id] = []
        self._handlers[agent_id].append(handler)

    def publish(self, message: A2AMessage) -> List[A2AMessage]:
        """Delivers message to the target recipient and collects response envelopes."""
        self.history.append(message)
        responses = []
        handlers = self._handlers.get(message.recipient_id, [])
        for h in handlers:
            res = h(message)
            if res:
                self.history.append(res)
                responses.append(res)
        return responses
