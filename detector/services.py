from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.db import transaction
from django.utils.dateparse import parse_datetime

from detector.models import DetectionRun, SignalRecord
from signal_detection.models import SignalMatch
from signal_detection.parser import parse_source
from signal_detection.signals import hiring, recruiting
from signal_detection.storage import write_json
from signal_detection.utils.fetch import fetch_source


DEFAULT_SOURCES = [
    "sample_data/company_blog_rss.xml",
    "sample_data/news_feed_rss.xml",
]


def run_detection(sources: list[str] | None = None) -> DetectionRun:
    active_sources = sources or DEFAULT_SOURCES
    collected: list[SignalMatch] = []

    for source in active_sources:
        content = fetch_source(source)
        documents = parse_source(content, source)
        for document in documents:
            for detector in (hiring.detect, recruiting.detect):
                match = detector(document)
                if match is not None:
                    collected.append(match)

    signals = _dedupe(collected)

    output_dir = Path(settings.BASE_DIR) / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(str(output_dir / "signals.json"), signals)

    with transaction.atomic():
        run = DetectionRun.objects.create(
            source_count=len(active_sources),
            signal_count=len(signals),
            notes="Run from Django dashboard",
        )
        SignalRecord.objects.bulk_create(
            [
                SignalRecord(
                    run=run,
                    company=signal.company,
                    signal_type=signal.signal_type,
                    source_url=signal.source_url,
                    matched_keywords=signal.matched_keywords,
                    signal_score=signal.signal_score,
                    detected_at=parse_datetime(signal.detected_at),
                    reason=signal.reason,
                    title=signal.title,
                    published_at=signal.published_at,
                )
                for signal in signals
            ]
        )
    return run


def _dedupe(signals: list[SignalMatch]) -> list[SignalMatch]:
    seen: set[tuple[str, str, str]] = set()
    deduped: list[SignalMatch] = []
    for signal in sorted(signals, key=lambda item: item.signal_score, reverse=True):
        key = (signal.company, signal.signal_type, signal.source_url)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(signal)
    return deduped
