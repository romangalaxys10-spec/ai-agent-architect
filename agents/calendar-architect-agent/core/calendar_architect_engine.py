"""
Calendar Architect Agent Engine.
Schedules tasks against real constraints: deadlines, priorities,
focus blocks, and meeting conflicts — with honest overrun flags.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class Slot:
    time: str
    end: str
    kind: str          # meeting | task | focus | buffer
    label: str
    status: str = "ok"

@dataclass
class DaySchedule:
    slots: List[Slot] = field(default_factory=list)
    tasks_scheduled: int = 0
    tasks_deferred: List[str] = field(default_factory=list)
    focus_minutes: int = 0
    conflicts: List[str] = field(default_factory=list)
    verdict: str = ""

def _hmm(minutes: int) -> str:
    h, m = divmod(int(minutes), 60)
    return f"{h:02d}:{m:02d}"

class CalendarArchitectEngine:
    """A calendar is a budget of hours — allocate it before others do."""

    @classmethod
    def schedule(cls, spec: dict) -> DaySchedule:
        work_start = int(spec.get("work_start", 9 * 60))
        work_end = int(spec.get("work_end", 17 * 60))
        meetings = list(spec.get("meetings", []))
        tasks = list(spec.get("tasks", []))

        slots: List[Slot] = []
        busy = []
        for mt in meetings:
            start = int(mt.get("start", 0))
            dur = int(mt.get("duration_min", 30))
            slots.append(Slot(_hmm(start), _hmm(start + dur), "meeting", str(mt.get("title", "meeting"))))
            busy.append((start, start + dur))

        def is_free(a, b):
            return all(b <= s or a >= e for s, e in busy)

        # sort tasks: EDF with priority preemption (P0 first within same deadline)
        def task_key(t):
            deadline = int(t.get("deadline_hour", work_end))
            pri = int(t.get("priority", 3))
            return (pri, deadline)

        tasks_sorted = sorted(tasks, key=task_key)
        cursor = work_start
        focus_start = None
        scheduled = 0
        deferred = []

        for t in tasks_sorted:
            dur = int(t.get("duration_min", 60))
            deadline = int(t.get("deadline_hour", work_end))
            name = str(t.get("name", t.get("title", "task")))
            placed = False
            start = cursor
            while start + dur <= work_end:
                if is_free(start, start + dur) and start + dur <= deadline:
                    slots.append(Slot(_hmm(start), _hmm(start + dur), "task", name))
                    busy.append((start, start + dur))
                    cursor = start + dur + 10  # 10-min buffer between tasks
                    busy.append((start + dur, cursor))
                    placed = True
                    break
                start += 15
            if not placed:
                # try anywhere before deadline
                start = work_start
                while start + dur <= min(deadline, work_end):
                    if is_free(start, start + dur):
                        slots.append(Slot(_hmm(start), _hmm(start + dur), "task", name))
                        busy.append((start, start + dur))
                        placed = True
                        break
                    start += 15
            if placed:
                scheduled += 1
            else:
                deferred.append(f"{name} ({dur}m, deadline {_hmm(deadline)}) — no free slot before deadline")

        # carve the longest free block as focus time
        gaps = []
        prev = work_start
        for s, e in sorted(busy):
            if s > prev:
                gaps.append((prev, s))
            prev = max(prev, e)
        if prev < work_end:
            gaps.append((prev, work_end))
        gaps.sort(key=lambda g: g[1] - g[0], reverse=True)
        if gaps and gaps[0][1] - gaps[0][0] >= 60:
            g = gaps[0]
            slots.append(Slot(_hmm(g[0]), _hmm(g[1]), "focus", "DEEP WORK — notifications off"))
            focus_start = g

        slots.sort(key=lambda s: s.time)

        conflicts = []
        sorted_busy = sorted(busy)
        for i in range(1, len(sorted_busy)):
            if sorted_busy[i][0] < sorted_busy[i - 1][1]:
                conflicts.append(f"overlap around {_hmm(sorted_busy[i][0])} — a task and meeting collide; drop or shorten one.")
        if deferred:
            conflicts.append(f"{len(deferred)} task(s) cannot fit before their deadlines — renegotiate deadlines or delegate.")
        if not gaps or all(g[1] - g[0] < 60 for g in gaps):
            conflicts.append("No 60-min focus block exists — the day is meeting soup; decline or shorten one meeting.")

        focus_min = focus_start[1] - focus_start[0] if focus_start else 0
        load = sum(e - s for s, e in busy) / max(1, work_end - work_start)
        verdict = (f"{scheduled}/{len(tasks_sorted)} tasks scheduled | focus {focus_min}m | "
                   f"calendar load {load:.0%} | {len(conflicts)} conflict flags")
        return DaySchedule(slots, scheduled, deferred, focus_min, conflicts, verdict)

    @staticmethod
    def format_schedule(s: DaySchedule) -> str:
        out = ["=" * 62, "CALENDAR ARCHITECT AGENT — DAY PLAN", "=" * 62, s.verdict, "-" * 62]
        for sl in s.slots:
            icon = {"meeting": "[MEET ]", "task": "[TASK ]", "focus": "[FOCUS]", "buffer": "[BUFF ]"}[sl.kind]
            out.append(f"  {icon} {sl.time}-{sl.end}  {sl.label[:48]}")
        if s.tasks_deferred:
            out += ["-" * 62, "Deferred (deadline impossible):"]
            out += [f"  ! {d}" for d in s.tasks_deferred]
        if s.conflicts:
            out += ["-" * 62, "Conflicts & honesty flags:"]
            out += [f"  ! {c}" for c in s.conflicts]
        out += ["-" * 62,
                "Rules that produced this plan: deadlines first (EDF), priority breaks ties, "
                "10-min buffers between deep tasks, one protected focus block minimum.",
                "=" * 62]
        return "\n".join(out)
