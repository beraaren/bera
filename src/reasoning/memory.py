"""Kısa süreli hafıza: geçmiş olayları ve analizleri saklar."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class MemoryEntry:
    timestamp: float
    content: Dict[str, Any]
    entry_type: str = "event"


class ShortTermMemory:
    """Sliding-window hafıza."""

    def __init__(self, max_entries: int = 100):
        self.max_entries = max_entries
        self.entries: List[MemoryEntry] = []

    def add(self, content: Dict[str, Any], entry_type: str = "event", timestamp: float = 0.0) -> None:
        self.entries.append(MemoryEntry(timestamp=timestamp, content=content, entry_type=entry_type))
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[-self.max_entries:]

    def get_recent(self, n: int = 10) -> List[Dict[str, Any]]:
        return [
            {"timestamp": e.timestamp, "type": e.entry_type, "content": e.content}
            for e in self.entries[-n:]
        ]

    def get_event_chain(self) -> List[Dict[str, Any]]:
        return [e.content for e in self.entries if e.entry_type == "event"]

    def to_prompt_context(self, max_events: int = 10) -> str:
        recent = self.get_recent(max_events)
        if not recent:
            return "Önceki olay geçmişi yok."
        lines = ["Önceki olay geçmişi:"]
        for r in recent:
            content = r["content"]
            if isinstance(content, dict) and "event_type" in content:
                lines.append(f"- {content.get('timestamp', '?')}: {content.get('description', '')}")
            else:
                lines.append(f"- {r.get('timestamp', '?')}: {str(content)[:120]}")
        return "\n".join(lines)
