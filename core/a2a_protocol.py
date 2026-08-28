"""
Agent-to-Agent (A2A) Communication Protocol — v2.0.

v2 upgrades (Google A2A / Linux Foundation spec + Microsoft L7 doctrine):
- AgentCard: JSON capability manifest served at /.well-known/agent-card.json
  with identity, skills (tags/examples), I/O modalities, security schemes.
- Task lifecycle: submitted -> working -> (input-required <-> working) ->
  completed | failed | canceled; task store; artifacts with typed Parts.
- Discovery: find agents by URL or by skill query across a registry.
- Legacy A2AMessage envelope bus retained for in-process meshes.

A2A = horizontal agent<->agent protocol; MCP = vertical agent<->tools protocol.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Sequence


# ---------------------------------------------------------------------------
# Legacy message envelope bus (retained API)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# v2: Agent Card
# ---------------------------------------------------------------------------

@dataclass
class AgentSkill:
    id: str
    name: str
    description: str
    tags: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)


@dataclass
class AgentCard:
    """
    The capability manifest (A2A spec). Served at /.well-known/agent-card.json.
    Enables dynamic discovery and best-agent selection.
    """
    name: str
    description: str
    url: str
    version: str = "1.0.0"
    skills: List[AgentSkill] = field(default_factory=list)
    capabilities: Dict[str, bool] = field(default_factory=lambda: {"streaming": False, "pushNotifications": False})
    input_modalities: List[str] = field(default_factory=lambda: ["text"])
    output_modalities: List[str] = field(default_factory=lambda: ["text"])
    security_schemes: Dict[str, str] = field(default_factory=lambda: {"none": "no auth (dev)"})
    provider: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "url": self.url,
            "version": self.version,
            "skills": [
                {"id": s.id, "name": s.name, "description": s.description,
                 "tags": s.tags, "examples": s.examples}
                for s in self.skills
            ],
            "capabilities": self.capabilities,
            "defaultInputModes": self.input_modalities,
            "defaultOutputModes": self.output_modalities,
            "securitySchemes": self.security_schemes,
            "provider": self.provider,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentCard":
        return cls(
            name=data["name"],
            description=data.get("description", ""),
            url=data.get("url", ""),
            version=data.get("version", "1.0.0"),
            skills=[
                AgentSkill(
                    id=s.get("id", uuid.uuid4().hex[:6]),
                    name=s["name"],
                    description=s.get("description", ""),
                    tags=s.get("tags", []),
                    examples=s.get("examples", []),
                )
                for s in data.get("skills", [])
            ],
            capabilities=data.get("capabilities", {"streaming": False, "pushNotifications": False}),
            input_modalities=data.get("defaultInputModes", ["text"]),
            output_modalities=data.get("defaultOutputModes", ["text"]),
            security_schemes=data.get("securitySchemes", {}),
            provider=data.get("provider", {}),
        )


WELL_KNOWN_PATH = "/.well-known/agent-card.json"


# ---------------------------------------------------------------------------
# v2: Task lifecycle
# ---------------------------------------------------------------------------

class TaskState(str, Enum):
    SUBMITTED = "submitted"
    WORKING = "working"
    INPUT_REQUIRED = "input-required"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"
    UNKNOWN = "unknown"


TERMINAL_STATES = {TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELED}


@dataclass
class Part:
    """Typed message part (Text / File / Data) enabling UX negotiation."""
    kind: str  # "text" | "file" | "data"
    text: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    file_uri: Optional[str] = None
    mime_type: str = "text/plain"


@dataclass
class Artifact:
    artifact_id: str
    name: str
    parts: List[Part] = field(default_factory=list)


@dataclass
class A2ATask:
    """
    Task created by the client; state maintained by the remote agent.
    Task = {id, sessionId, status, history, artifacts, metadata}.
    """
    task_id: str
    session_id: str
    description: str
    state: TaskState = TaskState.SUBMITTED
    history: List[Dict[str, Any]] = field(default_factory=list)
    artifacts: List[Artifact] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def transition(self, new_state: TaskState, note: str = "") -> None:
        if self.state in TERMINAL_STATES:
            raise ValueError(f"task is terminal ({self.state.value}); cannot transition to {new_state.value}")
        self.history.append({"from": self.state.value, "to": new_state.value, "note": note, "ts": time.time()})
        self.state = new_state
        self.updated_at = time.time()

    def add_artifact(self, name: str, parts: Optional[List[Part]] = None) -> Artifact:
        art = Artifact(artifact_id=f"art_{uuid.uuid4().hex[:8]}", name=name, parts=parts or [Part(kind="text", text="")])
        self.artifacts.append(art)
        return art

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.task_id,
            "sessionId": self.session_id,
            "description": self.description,
            "status": {"state": self.state.value},
            "history": self.history,
            "artifacts": [
                {"artifactId": a.artifact_id, "name": a.name,
                 "parts": [{"kind": p.kind, "text": p.text, "data": p.data, "fileUri": p.file_uri} for p in a.parts]}
                for a in self.artifacts
            ],
            "metadata": self.metadata,
        }


class TaskStore:
    """Persistence for A2A tasks (in-memory; swap for DB in prod)."""

    def __init__(self):
        self._tasks: Dict[str, A2ATask] = {}

    def create(self, description: str, session_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> A2ATask:
        task = A2ATask(
            task_id=f"task_{uuid.uuid4().hex[:10]}",
            session_id=session_id or f"sess_{uuid.uuid4().hex[:8]}",
            description=description,
            metadata=metadata or {},
        )
        self._tasks[task.task_id] = task
        return task

    def get(self, task_id: str) -> Optional[A2ATask]:
        return self._tasks.get(task_id)

    def active_tasks(self) -> List[A2ATask]:
        return [t for t in self._tasks.values() if t.state not in TERMINAL_STATES]


# ---------------------------------------------------------------------------
# v2: A2A participant (serves a card + executes tasks)
# ---------------------------------------------------------------------------

class A2AParticipant:
    """
    One agent exposed as an A2A service:
    - serves its Agent Card at the well-known path,
    - accepts tasks, walks them through the lifecycle,
    - handler function does the actual work.
    """

    def __init__(self, card: AgentCard, handler: Optional[Callable[[A2ATask], Any]] = None,
                 store: Optional[TaskStore] = None):
        self.card = card
        self.handler = handler
        self.store = store or TaskStore()

    def well_known(self) -> Dict[str, Any]:
        """GET /.well-known/agent-card.json"""
        return self.card.to_dict()

    def matches(self, query: str) -> bool:
        """Skill-based discovery match."""
        q = query.lower()
        if q in self.card.description.lower() or q in self.card.name.lower():
            return True
        return any(
            q in s.name.lower() or q in s.description.lower() or any(q in t.lower() for t in s.tags)
            for s in self.card.skills
        )

    def submit_task(self, description: str, metadata: Optional[Dict[str, Any]] = None) -> A2ATask:
        task = self.store.create(description, metadata=metadata)
        task.transition(TaskState.WORKING, "accepted by participant")
        return task

    def execute(self, task: A2ATask) -> A2ATask:
        if self.handler is None:
            task.transition(TaskState.FAILED, "no handler bound")
            return task
        try:
            result = self.handler(task)
            if isinstance(result, dict) and result.get("input_required"):
                task.transition(TaskState.INPUT_REQUIRED, result.get("reason", "needs human input"))
                return task
            task.add_artifact(
                name="result",
                parts=[Part(kind="data", data=result if isinstance(result, dict) else {"text": str(result)})],
            )
            task.transition(TaskState.COMPLETED, "handler finished")
        except Exception as exc:
            task.transition(TaskState.FAILED, str(exc))
        return task


class A2ADiscovery:
    """Registry of participants; discovery by URL or skill query."""

    def __init__(self):
        self.participants: Dict[str, A2AParticipant] = {}

    def register(self, participant: A2AParticipant) -> None:
        self.participants[participant.card.url] = participant

    def find_by_url(self, url: str) -> Optional[A2AParticipant]:
        return self.participants.get(url)

    def find_by_skill(self, query: str) -> List[A2AParticipant]:
        return [p for p in self.participants.values() if p.matches(query)]

    def catalog(self) -> List[Dict[str, Any]]:
        return [p.card.to_dict() for p in self.participants.values()]
