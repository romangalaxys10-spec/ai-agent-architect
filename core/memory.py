"""
Hierarchical Memory Subsystem for Autonomous Agents.
Layers:
1. Working Memory (Short-term scratchpad & active context)
2. Episodic Memory (Chronological trajectory of interactions)
3. Semantic Memory (Knowledge, facts, and embeddings)
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time
import json


@dataclass
class MemoryRecord:
    key: str
    value: Any
    category: str
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


class WorkingMemory:
    """Fast, transient in-flight scratchpad."""
    def __init__(self):
        self._store: Dict[str, Any] = {}

    def set(self, key: str, value: Any):
        self._store[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._store.get(key, default)

    def clear(self):
        self._store.clear()

    def snapshot(self) -> Dict[str, Any]:
        return self._store.copy()


class EpisodicMemory:
    """Chronological event and action trajectory."""
    def __init__(self):
        self._episodes: List[MemoryRecord] = []

    def record(self, event_type: str, details: Any, metadata: Optional[Dict[str, Any]] = None):
        rec = MemoryRecord(key=event_type, value=details, category="episodic", metadata=metadata or {})
        self._episodes.append(rec)

    def get_recent(self, n: int = 10) -> List[MemoryRecord]:
        return self._episodes[-n:]

    def export_timeline(self) -> List[Dict[str, Any]]:
        return [{"event": e.key, "details": e.value, "timestamp": e.timestamp, "metadata": e.metadata} for e in self._episodes]


class SemanticMemory:
    """Persistent facts, heuristics, and domain rules."""
    def __init__(self):
        self._facts: Dict[str, MemoryRecord] = {}

    def store_fact(self, key: str, fact: Any, confidence: float = 1.0):
        self._facts[key] = MemoryRecord(key=key, value=fact, category="semantic", metadata={"confidence": confidence})

    def retrieve(self, key: str) -> Optional[Any]:
        rec = self._facts.get(key)
        return rec.value if rec else None

    def search_by_prefix(self, prefix: str) -> Dict[str, Any]:
        return {k: v.value for k, v in self._facts.items() if k.startswith(prefix)}


class HierarchicalMemory:
    """Master Unified Memory Controller."""
    def __init__(self):
        self.working = WorkingMemory()
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()

    def summarize_state(self) -> Dict[str, Any]:
        return {
            "working_keys": list(self.working.snapshot().keys()),
            "episodic_count": len(self.episodic._episodes),
            "semantic_keys": list(self.semantic._facts.keys()),
        }
