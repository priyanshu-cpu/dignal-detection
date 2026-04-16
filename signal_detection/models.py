from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class SourceDocument:
    source_url: str
    title: str
    summary: str
    published_at: str
    raw_text: str


@dataclass(slots=True)
class SignalMatch:
    company: str
    signal_type: str
    source_url: str
    matched_keywords: list[str]
    signal_score: int
    detected_at: str
    reason: str
    title: str
    published_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
