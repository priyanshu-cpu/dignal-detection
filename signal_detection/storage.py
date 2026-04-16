from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from signal_detection.models import SignalMatch


def write_json(output_path: str, signals: list[SignalMatch]) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [signal.to_dict() for signal in signals]
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_sqlite(output_path: str, signals: list[SignalMatch]) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS signals (
                company TEXT NOT NULL,
                signal_type TEXT NOT NULL,
                source_url TEXT NOT NULL,
                matched_keywords TEXT NOT NULL,
                signal_score INTEGER NOT NULL,
                detected_at TEXT NOT NULL,
                reason TEXT NOT NULL,
                title TEXT NOT NULL,
                published_at TEXT NOT NULL
            )
            """
        )
        connection.execute("DELETE FROM signals")
        connection.executemany(
            """
            INSERT INTO signals (
                company, signal_type, source_url, matched_keywords,
                signal_score, detected_at, reason, title, published_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    signal.company,
                    signal.signal_type,
                    signal.source_url,
                    json.dumps(signal.matched_keywords),
                    signal.signal_score,
                    signal.detected_at,
                    signal.reason,
                    signal.title,
                    signal.published_at,
                )
                for signal in signals
            ],
        )
        connection.commit()
