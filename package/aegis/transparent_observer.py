"""AegisBrain Transparent Observer & Live Progress Streamer.

Prevents black-box execution by running a dedicated companion observer alongside
worker agents. Emits real-time micro-status updates, progress bars, and execution
checkpoints directly to the user so they remain engaged, informed, and capable of
early intervention/steering before tokens are wasted.
"""

import sys
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class ObserverEvent:
    phase: str  # RESEARCH, ALIGNMENT, ARCHITECTURE, WORKER, GATE, TEST, VERIFIED
    step_num: int
    total_steps: int
    title: str
    detail: str = ""
    timestamp: float = field(default_factory=time.time)


class TransparentObserver:
    """Live progress reporter and early-intervention steering bus."""

    PHASE_ICONS = {
        "RESEARCH": "🔍",
        "ALIGNMENT": "🤝",
        "ARCHITECTURE": "📐",
        "WORKER": "⚙️",
        "GATE": "🛡️",
        "TEST": "🧪",
        "VERIFIED": "✅",
        "INTERRUPT": "🛑",
        "FALLBACK": "🔄"
    }

    def __init__(self, task_name: str, total_steps: int = 5, verbose: bool = True):
        self.task_name = task_name
        self.total_steps = total_steps
        self.verbose = verbose
        self.history: List[ObserverEvent] = []
        self.listeners: List[Callable[[ObserverEvent], None]] = []
        self.paused = False
        self.steering_notes: List[str] = []

    def add_listener(self, callback: Callable[[ObserverEvent], None]) -> None:
        self.listeners.append(callback)

    def emit(self, phase: str, step_num: int, title: str, detail: str = "") -> ObserverEvent:
        """Publish a granular progress update."""
        evt = ObserverEvent(
            phase=phase,
            step_num=step_num,
            total_steps=self.total_steps,
            title=title,
            detail=detail,
            timestamp=time.time()
        )
        self.history.append(evt)

        if self.verbose:
            icon = self.PHASE_ICONS.get(phase.upper(), "📌")
            progress_str = f"[{step_num}/{self.total_steps}]" if self.total_steps > 0 else ""
            line = f"[Aegis Observer] {icon} {progress_str} {phase}: {title}"
            if detail:
                line += f"\n                 ↪ {detail}"
            print(line, flush=True)

        for listener in self.listeners:
            try:
                listener(evt)
            except Exception:
                pass

        return evt

    def steer(self, note: str) -> None:
        """Allows user to inject course-correction instructions mid-task."""
        self.steering_notes.append(note)
        self.emit("INTERRUPT", len(self.history), "User Course Correction Injected", detail=note)

    def get_active_steering(self) -> str:
        """Retrieve any steering directions provided by the user."""
        return "\n".join(self.steering_notes)


# Global default observer instance for CLI sessions
_current_observer: Optional[TransparentObserver] = None


def get_current_observer() -> Optional[TransparentObserver]:
    return _current_observer


def start_observer_session(task_name: str, total_steps: int = 5) -> TransparentObserver:
    global _current_observer
    _current_observer = TransparentObserver(task_name=task_name, total_steps=total_steps)
    return _current_observer
