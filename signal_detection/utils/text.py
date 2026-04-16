from __future__ import annotations

import re


TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")


def normalize_whitespace(value: str) -> str:
    return SPACE_RE.sub(" ", value).strip()


def strip_html(value: str) -> str:
    return normalize_whitespace(TAG_RE.sub(" ", value))


def safe_company_from_text(text: str) -> str:
    tokens = normalize_whitespace(text).split()
    if not tokens:
        return "Unknown"
    candidate = tokens[0].strip(" -:,.")
    return candidate or "Unknown"
