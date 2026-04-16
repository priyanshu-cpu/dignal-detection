from __future__ import annotations

from signal_detection.models import SignalMatch
from signal_detection.parser import parse_source
from signal_detection.signals import hiring, recruiting
from signal_detection.storage import write_json, write_sqlite
from signal_detection.utils.fetch import fetch_source


DEFAULT_SOURCES = [
    "sample_data/company_blog_rss.xml",
    "sample_data/news_feed_rss.xml",
]


def run_pipeline(
    sources: list[str] | None = None,
    json_output: str = "outputs/signals.json",
    sqlite_output: str = "outputs/signals.db",
) -> list[SignalMatch]:
    active_sources = sources or DEFAULT_SOURCES
    signals: list[SignalMatch] = []

    for source in active_sources:
        content = fetch_source(source)
        documents = parse_source(content, source)
        for document in documents:
            for detector in (hiring.detect, recruiting.detect):
                match = detector(document)
                if match is not None:
                    signals.append(match)

    deduped = dedupe_signals(signals)
    write_json(json_output, deduped)
    write_sqlite(sqlite_output, deduped)
    return deduped


def dedupe_signals(signals: list[SignalMatch]) -> list[SignalMatch]:
    seen: set[tuple[str, str, str]] = set()
    deduped: list[SignalMatch] = []
    for signal in sorted(signals, key=lambda item: item.signal_score, reverse=True):
        key = (signal.company, signal.signal_type, signal.source_url)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(signal)
    return deduped
