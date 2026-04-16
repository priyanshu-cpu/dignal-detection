from __future__ import annotations

from datetime import datetime, timezone

from signal_detection.models import SignalMatch, SourceDocument
from signal_detection.utils.text import safe_company_from_text


RECRUITING_KEYWORDS = {
    "talent acquisition": 26,
    "recruitment": 18,
    "recruiting platform": 22,
    "candidate pipeline": 18,
    "campus hiring": 22,
    "interview process": 16,
    "hiring managers": 14,
    "recruiters": 14,
    "workforce planning": 24,
}


def detect(document: SourceDocument) -> SignalMatch | None:
    text = f"{document.title} {document.summary} {document.raw_text}".lower()
    matched_keywords = [keyword for keyword in RECRUITING_KEYWORDS if keyword in text]
    score = sum(RECRUITING_KEYWORDS[keyword] for keyword in matched_keywords)

    if score < 30:
        return None

    return SignalMatch(
        company=safe_company_from_text(document.title),
        signal_type="recruiting_signal",
        source_url=document.source_url,
        matched_keywords=matched_keywords,
        signal_score=min(score, 100),
        detected_at=datetime.now(timezone.utc).isoformat(),
        reason="Recruiting-process or talent-acquisition signal detected",
        title=document.title,
        published_at=document.published_at,
    )
