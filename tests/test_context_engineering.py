"""Tests: context engineering (compaction, notes, sliding window, token estimation)."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from core.context_engineering import (
    Compactor, CompactionPolicy, ContextEngine, ContextWindow, StructuredNotes,
    estimate_tokens, messages_tokens,
)
from core.llm.providers import Message, Role


def conv(n, filler="word " * 30):
    msgs = [Message.user("initial goal statement that must survive compaction")]
    for i in range(n):
        msgs.append(Message.user(f"{filler} turn {i}"))
        msgs.append(Message.assistant(f"{filler} reply {i}"))
    return msgs


class TestTokenEstimation(unittest.TestCase):
    def test_estimate_tokens_positive(self):
        self.assertGreater(estimate_tokens("hello world this is a test"), 0)

    def test_messages_tokens_counts(self):
        tokens = messages_tokens([Message.user("x" * 400)])
        self.assertGreater(tokens, 50)


class TestCompactor(unittest.TestCase):
    def test_needs_compaction_by_ratio(self):
        c = Compactor(context_window_tokens=1000)  # tiny window
        self.assertTrue(c.needs_compaction(conv(30)))
        self.assertFalse(c.needs_compaction(conv(1)))

    def test_compact_protects_head_and_tail(self):
        c = Compactor(context_window_tokens=10_000, policy=CompactionPolicy(
            keep_recent_turns=2, keep_first_turns=1))
        messages = conv(10)
        out = c.compact(messages)
        # head preserved
        self.assertEqual(out[0].content, "initial goal statement that must survive compaction")
        # boundary marker present
        self.assertTrue(any((m.content or "").startswith("[COMPACTION") for m in out))
        # fewer messages than before
        self.assertLess(len(out), len(messages))

    def test_clip_tool_results(self):
        c = Compactor()
        msgs = [Message(role=Role.TOOL, content="x" * 5000, tool_call_id="t1")]
        out = c.clip_tool_results(msgs)
        self.assertIn("truncated", out[0].content)
        self.assertLess(len(out[0].content), 3000)

    def test_custom_summarizer_used(self):
        c = Compactor(summarizer=lambda text: "SUMMARY")
        out = c.compact(conv(6))
        marker = [m for m in out if (m.content or "").startswith("[COMPACTION")][0]
        self.assertIn("SUMMARY", marker.content)


class TestStructuredNotes(unittest.TestCase):
    def test_todo_recitation(self):
        notes = StructuredNotes()
        notes.set_todos(["gather", "build", "verify"])
        notes.complete(0)
        rendered = notes.render()
        self.assertIn("[x] gather", rendered)
        self.assertIn("[ ] build", rendered)
        self.assertEqual(notes.progress_ratio(), 1 / 3)

    def test_facts_persist(self):
        notes = StructuredNotes()
        notes.note_fact("repo", "/tmp/x")
        self.assertIn("repo: /tmp/x", notes.render())


class TestContextWindow(unittest.TestCase):
    def test_four_block_assembly_order(self):
        w = ContextWindow(system_block="SYS", tools_block="TOOLS", notes_block="NOTES",
                          conversation=[Message.user("hi")])
        msgs = w.assemble()
        self.assertEqual(msgs[0].role, Role.SYSTEM)
        self.assertIn("SYS", msgs[0].content)
        self.assertIn("TOOLS", msgs[0].content)
        self.assertIn("NOTES", msgs[0].content)
        self.assertEqual(msgs[-1].content, "hi")

    def test_context_engine_step_integrates_notes(self):
        engine = ContextEngine()
        engine.notes.set_todos(["step one"])
        msgs = engine.step("SYSTEM PROMPT", [Message.user("task")])
        self.assertIn("step one", msgs[0].content)


if __name__ == "__main__":
    unittest.main()
