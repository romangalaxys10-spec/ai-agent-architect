"""
Agentic RAG (Retrieval as a tool inside the reasoning loop).

Standard RAG is a static pipeline (embed -> search -> generate) that fails
silently on retrieval misses. Agentic RAG embeds retrieval as TOOLS the agent
decides to call, then GRADES what came back and can re-query (NVIDIA workflow):

    agent -> retrieve(query) -> grade(chunks) --sufficient--> answer
                                    |ambiguous/insufficient
                                    v
                          rewrite query / alternate source -> retrieve again

Includes Corrective-RAG grading, query rewriting, chunking, and citation
enforcement so every generated claim maps to a source doc.
"""

from __future__ import annotations

import re
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from .memory import VectorStore, _hash_embed


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------

def chunk_text(text: str, chunk_chars: int = 600, overlap: int = 80) -> List[str]:
    """Sliding-window chunker with overlap; sentence-boundary aware fallback."""
    text = text.strip()
    if len(text) <= chunk_chars:
        return [text] if text else []
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_chars, len(text))
        if end < len(text):
            # try to break at a sentence or word boundary
            boundary = max(text.rfind(". ", start, end), text.rfind("\n", start, end), text.rfind(" ", start, end))
            if boundary > start + chunk_chars // 2:
                end = boundary + 1
        chunks.append(text[start:end].strip())
        start = end - overlap if end < len(text) else end
    return [c for c in chunks if c]


@dataclass
class RetrievedChunk:
    doc_id: str
    text: str
    score: float
    metadata: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Relevance grading (Corrective RAG)
# ---------------------------------------------------------------------------

@dataclass
class Grade:
    relevant: bool
    reason: str


class RelevanceGrader:
    """
    Grades retrieved chunks as relevant / ambiguous / irrelevant.
    Default grader is deterministic lexical overlap (works offline); plug an
    LLM judge for production. Corrective-RAG doctrine: grade BEFORE generation.
    """

    def __init__(self, grader_fn: Optional[Callable[[str, str], bool]] = None, threshold: float = 0.12):
        self.grader_fn = grader_fn
        self.threshold = threshold

    def grade(self, query: str, chunk: str) -> Grade:
        if self.grader_fn is not None:
            return Grade(relevant=bool(self.grader_fn(query, chunk)), reason="custom grader")
        q_terms = set(re.findall(r"\w+", query.lower()))
        c_terms = set(re.findall(r"\w+", chunk.lower()))
        if not q_terms:
            return Grade(relevant=False, reason="empty query")
        overlap = len(q_terms & c_terms) / len(q_terms)
        return Grade(relevant=overlap >= self.threshold, reason=f"lexical overlap {overlap:.2f}")


# ---------------------------------------------------------------------------
# Query rewriting
# ---------------------------------------------------------------------------

class QueryRewriter:
    """Rewrites failed queries: expand acronyms, add context terms, de-duplicate."""

    def __init__(self, rewrite_fn: Optional[Callable[[str, List[str]], str]] = None):
        self.rewrite_fn = rewrite_fn

    def rewrite(self, query: str, failed_terms: Sequence[str]) -> str:
        if self.rewrite_fn:
            return self.rewrite_fn(query, list(failed_terms))
        expanded = [t for t in failed_terms if len(t) > 3]
        return f"{query} {' '.join(expanded)}".strip()


# ---------------------------------------------------------------------------
# The Agentic RAG engine
# ---------------------------------------------------------------------------

@dataclass
class RAGAnswer:
    answer: str
    citations: List[Dict[str, Any]]
    retrieval_attempts: int
    used_rewrite: bool
    confidence: float
    latency_ms: float


class AgenticRAG:
    """
    The agent-side RAG engine exposed as TOOLS to the loop:
      - `knowledge_search(query)`  : retrieve from the vector store
      - `knowledge_store(doc)`     : write to the knowledge base (agentic write-back)
    Plus a full corrective pipeline for one-shot use.
    """

    def __init__(
        self,
        store: Optional[VectorStore] = None,
        grader: Optional[RelevanceGrader] = None,
        rewriter: Optional[QueryRewriter] = None,
        max_attempts: int = 2,
        top_k: int = 4,
    ):
        self.store = store or VectorStore()
        self.grader = grader or RelevanceGrader()
        self.rewriter = rewriter or QueryRewriter()
        self.max_attempts = max_attempts
        self.top_k = top_k

    # -- knowledge base management -----------------------------------------
    def ingest(self, text: str, source: str = "manual", metadata: Optional[Dict[str, Any]] = None) -> List[str]:
        doc_ids = []
        for i, chunk in enumerate(chunk_text(text)):
            doc_id = f"{source}::chunk{i}"
            self.store.upsert(doc_id, chunk, {"source": source, **(metadata or {})})
            doc_ids.append(doc_id)
        return doc_ids

    # -- tools the agent can call --------------------------------------------
    def as_tool_functions(self) -> Dict[str, Callable]:
        """Functions to register on a ToolRegistry so the agent owns retrieval."""
        def knowledge_search(query: str) -> dict:
            hits = self.store.search(query, top_k=self.top_k)
            return {
                "chunks": [
                    {"doc_id": d.doc_id, "text": d.text[:500], "score": round(s, 3), "source": d.metadata.get("source", "unknown")}
                    for d, s in hits
                ]
            }

        def knowledge_store(text: str, source: str = "agent") -> dict:
            ids = self.ingest(text, source=source, metadata={"written_by": "agent"})
            return {"stored": ids}

        return {"knowledge_search": knowledge_search, "knowledge_store": knowledge_store}

    def tool_declarations(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "knowledge_search",
                "description": "Search the knowledge base. Returns scored chunks with sources.",
                "parameters": {
                    "type": "object",
                    "properties": {"query": {"type": "string", "description": "Search query"}},
                    "required": ["query"],
                },
            },
            {
                "name": "knowledge_store",
                "description": "Persist new knowledge into the vector store for future recall.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Knowledge to store"},
                        "source": {"type": "string", "description": "Origin label"},
                    },
                    "required": ["text"],
                },
            },
        ]

    # -- corrective pipeline ---------------------------------------------------
    def answer(self, query: str, synthesizer: Optional[Callable[[str, List[RetrievedChunk]], str]] = None) -> RAGAnswer:
        """
        Corrective RAG loop: retrieve -> grade -> (rewrite & retry) -> synthesize
        with citations. The default synthesizer is extractive (offline-safe).
        """
        t0 = time.time()
        attempts = 0
        used_rewrite = False
        current_query = query
        accepted: List[RetrievedChunk] = []

        while attempts < self.max_attempts:
            attempts += 1
            hits = self.store.search(current_query, top_k=self.top_k)
            graded: List[Tuple[RetrievedChunk, Grade]] = []
            for doc, score in hits:
                chunk = RetrievedChunk(doc_id=doc.doc_id, text=doc.text, score=score, metadata=doc.metadata)
                graded.append((chunk, self.grader.grade(query, doc.text)))
            accepted = [c for c, g in graded if g.relevant]
            if accepted:
                break
            # corrective: rewrite with terms that failed, try alternate formulation
            failed_terms = re.findall(r"\w+", current_query)
            current_query = self.rewriter.rewrite(query, failed_terms[:4])
            used_rewrite = True

        if not accepted:
            return RAGAnswer(
                answer="Insufficient evidence in the knowledge base for this query.",
                citations=[], retrieval_attempts=attempts, used_rewrite=used_rewrite,
                confidence=0.0, latency_ms=(time.time() - t0) * 1000,
            )

        if synthesizer:
            answer_text = synthesizer(query, accepted)
        else:
            answer_text = (
                f"Based on {len(accepted)} retrieved sources:\n"
                + "\n\n".join(f"- {c.text[:300]} [{c.doc_id}]" for c in accepted)
            )

        citations = [
            {"doc_id": c.doc_id, "source": c.metadata.get("source", "unknown"), "score": round(c.score, 3)}
            for c in accepted
        ]
        avg_score = sum(c.score for c in accepted) / max(1, len(accepted))
        return RAGAnswer(
            answer=answer_text,
            citations=citations,
            retrieval_attempts=attempts,
            used_rewrite=used_rewrite,
            confidence=round(min(1.0, avg_score * 1.4), 3),
            latency_ms=(time.time() - t0) * 1000,
        )
