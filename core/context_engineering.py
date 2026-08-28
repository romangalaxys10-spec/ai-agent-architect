"""
Context Engineering subsystem.

Implements the 2024-2025 long-horizon triad (Anthropic):
1. Compaction — summarize near the limit, restart window from the summary;
   lightest safe lever is tool-result clearing.
2. Structured note-taking — agent writes notes outside the context (todo.md
   recitation pattern) and re-reads them each turn.
3. Sub-agent contexts — clean-context workers; lead agent keeps the plan.

Plus: token estimation before send (bryanyzhu Ch.17) and the four-block
sliding-window assembly (bryanyzhu Ch.04).
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence

from .llm.providers import LLMProvider, Message, Role


def estimate_tokens(text: str) -> int:
    """Cheap token estimate (~4 chars/token heuristic). Never blocks on send."""
    return max(1, len(text or "") // 4)


def messages_tokens(messages: Sequence[Message]) -> int:
    total = 0
    for m in messages:
        total += estimate_tokens(m.content or "") + 8
        if m.tool_calls:
            total += estimate_tokens(str(m.tool_calls))
    return total


# ---------------------------------------------------------------------------
# Compaction
# ---------------------------------------------------------------------------

@dataclass
class CompactionPolicy:
    trigger_ratio: float = 0.75        # compact when tokens > ratio * window
    keep_recent_turns: int = 4         # protect both ends...
    keep_first_turns: int = 1          # ...compress the middle (asymmetric reduction)
    max_tool_result_chars: int = 2_000  # clip tool outputs at the boundary


DEFAULT_SUMMARY_PROMPT = (
    "Summarize this agent conversation for continuation. Preserve: goals, decisions made, "
    "bugs/findings, artifacts produced, open TODOs. Drop: redundant tool outputs, pleasantries, "
    "failed dead-ends. Output a compact briefing under 300 words."
)


class Compactor:
    """Collapse-then-summarize with a compaction boundary marker."""

    def __init__(self, context_window_tokens: int = 32_000, policy: Optional[CompactionPolicy] = None,
                 summarizer: Optional[Callable[[str], str]] = None):
        self.context_window_tokens = context_window_tokens
        self.policy = policy or CompactionPolicy()
        self._summarizer = summarizer
        self.compactions = 0

    def needs_compaction(self, messages: Sequence[Message]) -> bool:
        return messages_tokens(messages) > self.policy.trigger_ratio * self.context_window_tokens

    def clip_tool_results(self, messages: Sequence[Message]) -> List[Message]:
        """Lightest safe lever: truncate tool outputs to budget."""
        out: List[Message] = []
        for m in messages:
            if m.role == Role.TOOL and m.content and len(m.content) > self.policy.max_tool_result_chars:
                out.append(
                    Message(
                        role=m.role,
                        content=m.content[: self.policy.max_tool_result_chars] + "\n...[tool output truncated]",
                        tool_call_id=m.tool_call_id,
                        name=m.name,
                    )
                )
            else:
                out.append(m)
        return out

    def _default_summarizer(self, text: str) -> str:
        # Deterministic extractive fallback (works offline; LLM summarizer pluggable).
        lines = [ln for ln in text.splitlines() if ln.strip()]
        keep = max(12, len(lines) // 4)
        return "\n".join(lines[:keep])

    def compact(self, messages: Sequence[Message]) -> List[Message]:
        """
        Asymmetric reduction: protect the first turn(s) and the most recent
        turns; summarize everything between into one boundary-marker message.
        """
        if len(messages) <= self.policy.keep_recent_turns + self.policy.keep_first_turns:
            return list(messages)
        head = list(messages[: self.policy.keep_first_turns])
        middle = messages[self.policy.keep_first_turns : -self.policy.keep_recent_turns]
        tail = list(messages[-self.policy.keep_recent_turns :])

        transcript = "\n".join((m.content or "") for m in middle if m.content)
        summarize = self._summarizer or self._default_summarizer
        summary = summarize(transcript) or transcript[:500]

        boundary = Message(
            role=Role.SYSTEM,
            content=f"[COMPACTION #{self.compactions + 1} at {time.time():.0f}] "
            f"Earlier conversation summarized ({len(middle)} messages -> briefing):\n{summary}",
        )
        self.compactions += 1
        compacted = head + [boundary] + tail
        return self.clip_tool_results(compacted)


# ---------------------------------------------------------------------------
# Structured note-taking (agentic memory outside the context window)
# ---------------------------------------------------------------------------

class StructuredNotes:
    """
    The todo.md recitation pattern: agent rewrites its notes every turn, which
    pushes goals into recent attention and counters lost-in-the-middle.
    """

    def __init__(self) -> None:
        self.todos: List[Dict[str, Any]] = []
        self.facts: Dict[str, str] = {}
        self.updated_at: float = time.time()

    def set_todos(self, items: Sequence[str]) -> None:
        self.todos = [{"text": t, "done": False} for t in items]
        self.updated_at = time.time()

    def complete(self, index: int) -> None:
        if 0 <= index < len(self.todos):
            self.todos[index]["done"] = True
            self.updated_at = time.time()

    def note_fact(self, key: str, value: str) -> None:
        self.facts[key] = value
        self.updated_at = time.time()

    def render(self) -> str:
        """Recitation block injected into the system prompt each turn."""
        lines = ["## CURRENT PLAN (recited each turn)"]
        for i, t in enumerate(self.todos):
            mark = "x" if t["done"] else " "
            lines.append(f"- [{mark}] {t['text']}")
        if self.facts:
            lines.append("## PERSISTENT FACTS")
            for k, v in self.facts.items():
                lines.append(f"- {k}: {v}")
        return "\n".join(lines)

    def progress_ratio(self) -> float:
        if not self.todos:
            return 0.0
        return sum(1 for t in self.todos if t["done"]) / len(self.todos)


# ---------------------------------------------------------------------------
# Four-block sliding window assembly (bryanyzhu Ch.04)
# ---------------------------------------------------------------------------

@dataclass
class ContextWindow:
    """
    The prompt is an assembled structure of four stable-ordered blocks:
    [identity/system] [skills/tools] [notes] [conversation]. Stable prefixes
    preserve provider KV-caches (Manus rule #1: design around the cache).
    """
    system_block: str = ""
    tools_block: str = ""
    notes_block: str = ""
    conversation: List[Message] = field(default_factory=list)

    def assemble(self) -> List[Message]:
        out: List[Message] = []
        sys_parts = [p for p in (self.system_block, self.tools_block, self.notes_block) if p]
        if sys_parts:
            out.append(Message(role=Role.SYSTEM, content="\n\n".join(sys_parts)))
        out.extend(self.conversation)
        return out

    def token_estimate(self) -> int:
        return messages_tokens(self.assemble())


class ContextEngine:
    """
    Facade binding the pieces together per step-boundary:
    estimate -> maybe compact -> recite notes -> assemble window.
    """

    def __init__(self, context_window_tokens: int = 32_000, summarizer: Optional[Callable[[str], str]] = None):
        self.compactor = Compactor(context_window_tokens=context_window_tokens, summarizer=summarizer)
        self.notes = StructuredNotes()

    def step(self, system_prompt: str, conversation: List[Message], tools_digest: str = "") -> List[Message]:
        window = ContextWindow(
            system_block=system_prompt,
            tools_block=f"## AVAILABLE TOOLS\n{tools_digest}" if tools_digest else "",
            notes_block=self.notes.render(),
            conversation=conversation,
        )
        msgs = window.assemble()
        if self.compactor.needs_compaction(msgs):
            conversation = self.compactor.compact(msgs)
            window.conversation = [
                m for m in conversation if m.role != Role.SYSTEM or not (m.content or "").startswith("[COMPACTION")
            ] if conversation else conversation
            # rebuild preserving the compaction boundary marker
            boundary = [m for m in conversation if (m.content or "").startswith("[COMPACTION")]
            regular = [m for m in conversation if not (m.content or "").startswith("[COMPACTION")]
            window.conversation = regular
            msgs = window.assemble()
            # insert boundary right after system
            insert_at = 1 if sys_parts else 0
            for b in boundary:
                msgs.insert(insert_at, b)
                insert_at += 1
        return msgs
