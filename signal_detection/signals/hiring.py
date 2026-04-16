from __future__ import annotations

import re
from datetime import datetime, timezone

from signal_detection.models import SignalMatch, SourceDocument
from signal_detection.utils.text import safe_company_from_text


HIRING_KEYWORDS = {
    "hiring": 18,
    "hiring spree": 35,
    "recruiting": 16,
    "open roles": 22,
    "careers": 10,
    "new office": 12,
    "expanding team": 24,
    "engineers": 10,
    "sales team": 12,
}

HEADCOUNT_PATTERNS = [
    re.compile(r"\b(\d{2,5})\s+(?:new\s+)?(?:hires|employees|engineers|roles|people)\b", re.I),
    re.compile(r"\b(?:hire|hiring)\s+(\d{2,5})\b", re.I),
]


def detect(document: SourceDocument) -> SignalMatch | None:
    text = f"{document.title} {document.summary} {document.raw_text}".lower()
    matched_keywords = [keyword for keyword in HIRING_KEYWORDS if keyword in text]
    score = sum(HIRING_KEYWORDS[keyword] for keyword in matched_keywords)

    headcount_mentions: list[str] = []
    for pattern in HEADCOUNT_PATTERNS:
        for match in pattern.findall(text):
            headcount_mentions.append(str(match))

    if headcount_mentions:
        matched_keywords.extend(headcount_mentions)
        score += min(40, 10 * len(headcount_mentions))

    matched_keywords = list(dict.fromkeys(matched_keywords))

    if score < 30:
        return None

    company = safe_company_from_text(document.title)
    reason = "Hiring-related growth signal detected"
    if headcount_mentions:
        unique_mentions = list(dict.fromkeys(headcount_mentions))
        reason = f"Hiring language found with explicit headcount mention(s): {', '.join(unique_mentions)}"

    return SignalMatch(
        company=company,
        signal_type="mass_hiring" if headcount_mentions else "hiring_activity",
        source_url=document.source_url,
        matched_keywords=matched_keywords,
        signal_score=min(score, 100),
        detected_at=datetime.now(timezone.utc).isoformat(),
        reason=reason,
        title=document.title,
        published_at=document.published_at,
    )
