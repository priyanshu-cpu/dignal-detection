from __future__ import annotations

from signal_detection.pipeline import run_pipeline


def handler(event: dict | None = None, context: object | None = None) -> dict:
    event = event or {}
    results = run_pipeline(
        sources=event.get("sources"),
        json_output=event.get("json_output", "outputs/signals.json"),
        sqlite_output=event.get("sqlite_output", "outputs/signals.db"),
    )
    return {
        "statusCode": 200,
        "count": len(results),
        "signals": [signal.to_dict() for signal in results],
    }
