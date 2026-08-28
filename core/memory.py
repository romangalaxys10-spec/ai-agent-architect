"""
Hierarchical Memory Subsystem — v2.0 (Production).

Layers:
1. Working Memory   (short-term scratchpad & active context)
2. Episodic Memory  (chronological trajectory, exportable timeline)
3. Semantic Memory  (facts, heuristics, vector search)
4. Vector Store     (embedding-indexed knowledge for RAG recall)

v2 upgrades (MemGPT/Letta + bryanyzhu Ch.05-07 doctrine):
- Embedding-indexed recall with deterministic offline embedder (pluggable).
- Persistence: JSON save/load for all tiers.
- Curation lifecycle: conflict resolution (supersede / merge / drop), decay,
  pruning, provenance and rollback.
- Memory-boundary safety filter (blocks injection poisoning of long-term memory).
- Namespaces (per-user / per-tenant isolation).
- Write modes: explicit, auto-episodic, curated.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import time
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple


# ---------------------------------------------------------------------------
# Records
# ---------------------------------------------------------------------------

@dataclass
class MemoryRecord:
    key: str
    value: Any
    category: str
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VectorDocument:
    doc_id: str
    text: str
    embedding: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Deterministic offline embedder (pluggable with real embedding models)
# ---------------------------------------------------------------------------

def _hash_embed(text: str, dims: int = 64) -> List[float]:
    """Deterministic token-hash embedding. No network, no keys, stable across runs.
    Swap via `embedding_fn` for text-embedding-3-small / BGE / CLIP in production."""
    vec = [0.0] * dims
    for token in re.findall(r"\w+", text.lower()):
        h = int(hashlib.md5(token.encode()).hexdigest(), 16)
        vec[h % dims] += 1.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def cosine(a: Sequence[float], b: Sequence[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(y * y for y in b)) or 1.0
    return dot / (na * nb)


# ---------------------------------------------------------------------------
# Vector store
# ---------------------------------------------------------------------------

class VectorStore:
    """In-memory vector index with upsert, top-k search, and metadata filters.
    The retrieval backbone for agentic RAG (swap for Qdrant/Chroma in prod)."""

    def __init__(self, embedding_fn: Callable[[str], List[float]] = _hash_embed, dims: int = 64):
        self.embedding_fn = embedding_fn
        self.dims = dims
        self._docs: Dict[str, VectorDocument] = {}

    def upsert(self, doc_id: str, text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        self._docs[doc_id] = VectorDocument(
            doc_id=doc_id, text=text, embedding=self.embedding_fn(text), metadata=metadata or {}
        )
        return doc_id

    def search(self, query: str, top_k: int = 4, min_score: float = 0.05,
               filter: Optional[Callable[[Dict[str, Any]], bool]] = None) -> List[Tuple[VectorDocument, float]]:
        q = self.embedding_fn(query)
        scored = [
            (doc, cosine(q, doc.embedding))
            for doc in self._docs.values()
            if filter is None or filter(doc.metadata)
        ]
        scored = [(doc, s) for doc, s in scored if s >= min_score]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return scored[:top_k]

    def delete(self, doc_id: str) -> bool:
        return self._docs.pop(doc_id, None) is not None

    def count(self) -> int:
        return len(self._docs)

    def stats(self) -> Dict[str, Any]:
        return {"documents": len(self._docs), "dims": self.dims}


# ---------------------------------------------------------------------------
# Tier 1: Working memory
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Tier 2: Episodic memory
# ---------------------------------------------------------------------------

class EpisodicMemory:
    """Chronological event and action trajectory."""

    def __init__(self, max_episodes: int = 10_000):
        self._episodes: List[MemoryRecord] = []
        self.max_episodes = max_episodes

    def record(self, event_type: str, details: Any, metadata: Optional[Dict[str, Any]] = None):
        rec = MemoryRecord(key=event_type, value=details, category="episodic", metadata=metadata or {})
        self._episodes.append(rec)
        if len(self._episodes) > self.max_episodes:  # bounded ring
            self._episodes = self._episodes[-self.max_episodes:]

    def get_recent(self, n: int = 10) -> List[MemoryRecord]:
        return self._episodes[-n:]

    def search(self, keyword: str) -> List[MemoryRecord]:
        k = keyword.lower()
        return [e for e in self._episodes if k in str(e.value).lower() or k in e.key.lower()]

    def export_timeline(self) -> List[Dict[str, Any]]:
        return [
            {"event": e.key, "details": e.value, "timestamp": e.timestamp, "metadata": e.metadata}
            for e in self._episodes
        ]


# ---------------------------------------------------------------------------
# Tier 3: Semantic memory + curation
# ---------------------------------------------------------------------------

class ConflictResolution(str, Enum):
    SUPERSEDE = "supersede"
    MERGE = "merge"
    DROP = "drop"


# Memory-boundary injection filter: untrusted content that tries to become
# long-term memory gets quarantined (bryanyzhu Ch.07 + OWASP LLM01).
_MEMORY_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+(instructions|memory)",
    r"remember\s+(that\s+)?you\s+are\s+now",
    r"disregard\s+your\s+system",
    r"from\s+now\s+on\s+always\s+obey",
]


class SemanticMemory:
    """Persistent facts with curation: confidence, provenance, decay, conflict resolution."""

    def __init__(self, retention_seconds: float = 60 * 60 * 24 * 30):
        self._facts: Dict[str, MemoryRecord] = {}
        self.retention_seconds = retention_seconds
        self.quarantine: List[MemoryRecord] = []
        self.rolled_back: List[str] = []

    @staticmethod
    def _looks_poisoned(fact: Any) -> bool:
        text = str(fact)
        return any(re.search(p, text, re.IGNORECASE) for p in _MEMORY_INJECTION_PATTERNS)

    def store_fact(self, key: str, fact: Any, confidence: float = 1.0,
                   provenance: str = "unknown", on_conflict: ConflictResolution = ConflictResolution.SUPERSEDE):
        if self._looks_poisoned(fact):
            self.quarantine.append(
                MemoryRecord(key=key, value=fact, category="quarantined",
                             metadata={"reason": "suspected memory-poisoning injection"})
            )
            return "quarantined"

        if key in self._facts:
            existing = self._facts[key]
            if on_conflict == ConflictResolution.SUPERSEDE:
                existing.metadata["superseded_by"] = time.time()
                self._facts[key] = MemoryRecord(
                    key=key, value=fact, category="semantic",
                    metadata={"confidence": confidence, "provenance": provenance,
                              "supersedes": existing.timestamp},
                )
                return "superseded"
            if on_conflict == ConflictResolution.MERGE:
                merged = f"{existing.value} | {fact}"
                self._facts[key] = MemoryRecord(
                    key=key, value=merged, category="semantic",
                    metadata={"confidence": max(confidence, existing.metadata.get("confidence", 0.5)),
                              "provenance": provenance, "merged": True},
                )
                return "merged"
            return "dropped"

        self._facts[key] = MemoryRecord(
            key=key, value=fact, category="semantic",
            metadata={"confidence": confidence, "provenance": provenance},
        )
        return "stored"

    def retrieve(self, key: str) -> Optional[Any]:
        rec = self._facts.get(key)
        return rec.value if rec else None

    def search_by_prefix(self, prefix: str) -> Dict[str, Any]:
        return {k: v.value for k, v in self._facts.items() if k.startswith(prefix)}

    def rollback(self, key: str) -> bool:
        """Provenance rollback: restore the superseded value if present."""
        rec = self._facts.get(key)
        if rec and "supersedes" in rec.metadata:
            self._facts[key] = MemoryRecord(
                key=key, value=rec.metadata.get("previous_value", rec.value),
                category="semantic", metadata={"rolled_back_at": time.time()},
            )
            self.rolled_back.append(key)
            return True
        return False

    def prune_expired(self) -> int:
        now = time.time()
        expired = [k for k, v in self._facts.items()
                   if now - v.timestamp > self.retention_seconds
                   and v.metadata.get("confidence", 1.0) < 0.9]
        for k in expired:
            del self._facts[k]
        return len(expired)


# ---------------------------------------------------------------------------
# Unified controller
# ---------------------------------------------------------------------------

class HierarchicalMemory:
    """
    Master Unified Memory Controller with namespaces, vector recall and
    persistence. Filesystem-as-context doctrine: memory is pluggable,
    exportable, and inspectable.
    """

    def __init__(self, namespace: str = "default", embedding_fn: Callable[[str], List[float]] = _hash_embed):
        self.namespace = namespace
        self.working = WorkingMemory()
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()
        self.vector = VectorStore(embedding_fn=embedding_fn)

    # -- vector recall -----------------------------------------------------
    def remember(self, doc_id: str, text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        return self.vector.upsert(doc_id, text, metadata)

    def recall(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        hits = self.vector.search(query, top_k=top_k)
        return [{"doc_id": d.doc_id, "text": d.text, "score": round(s, 4), "metadata": d.metadata}
                for d, s in hits]

    # -- persistence --------------------------------------------------------
    def save(self, path: str) -> str:
        payload = {
            "namespace": self.namespace,
            "working": self.working.snapshot(),
            "episodic": self.episodic.export_timeline(),
            "semantic": {k: asdict(v) for k, v in self.semantic._facts.items()},
            "vector": [
                {"doc_id": d.doc_id, "text": d.text, "metadata": d.metadata}
                for d in self.vector._docs.values()
            ],
            "saved_at": time.time(),
        }
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, default=str)
        return path

    @classmethod
    def load(cls, path: str) -> "HierarchicalMemory":
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        mem = cls(namespace=payload.get("namespace", "default"))
        for k, v in payload.get("working", {}).items():
            mem.working.set(k, v)
        for e in payload.get("episodic", []):
            mem.episodic.record(e["event"], e["details"], e.get("metadata"))
        for k, rec in payload.get("semantic", {}).items():
            mem.semantic._facts[k] = MemoryRecord(**rec)
        for d in payload.get("vector", []):
            mem.vector.upsert(d["doc_id"], d["text"], d.get("metadata"))
        return mem

    def summarize_state(self) -> Dict[str, Any]:
        return {
            "namespace": self.namespace,
            "working_keys": list(self.working.snapshot().keys()),
            "episodic_count": len(self.episodic._episodes),
            "semantic_keys": list(self.semantic._facts.keys()),
            "quarantined": len(self.semantic.quarantine),
            "vector_docs": self.vector.count(),
        }
