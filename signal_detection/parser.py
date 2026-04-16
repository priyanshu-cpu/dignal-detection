from __future__ import annotations

import xml.etree.ElementTree as ET
from html.parser import HTMLParser

from signal_detection.models import SourceDocument
from signal_detection.utils.text import normalize_whitespace, strip_html


class SimpleHTMLTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data.strip():
            self._parts.append(data.strip())

    def text(self) -> str:
        return normalize_whitespace(" ".join(self._parts))


def parse_source(content: str, source_url: str) -> list[SourceDocument]:
    content = content.strip()
    if content.startswith("<") and "<rss" in content.lower():
        return parse_rss(content, source_url)
    if content.startswith("<") and "<feed" in content.lower():
        return parse_atom(content, source_url)
    return [parse_html(content, source_url)]


def parse_rss(content: str, source_url: str) -> list[SourceDocument]:
    root = ET.fromstring(content)
    docs: list[SourceDocument] = []
    for item in root.findall(".//item"):
        title = item.findtext("title", default="")
        link = item.findtext("link", default=source_url)
        summary = item.findtext("description", default="")
        published_at = item.findtext("pubDate", default="")
        docs.append(
            SourceDocument(
                source_url=link.strip() or source_url,
                title=normalize_whitespace(title),
                summary=strip_html(summary),
                published_at=normalize_whitespace(published_at),
                raw_text=normalize_whitespace(f"{title} {strip_html(summary)}"),
            )
        )
    return docs


def parse_atom(content: str, source_url: str) -> list[SourceDocument]:
    root = ET.fromstring(content)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    docs: list[SourceDocument] = []
    for entry in root.findall("atom:entry", ns):
        title = entry.findtext("atom:title", default="", namespaces=ns)
        summary = entry.findtext("atom:summary", default="", namespaces=ns)
        published_at = entry.findtext("atom:updated", default="", namespaces=ns)
        link_el = entry.find("atom:link", ns)
        link = link_el.attrib.get("href", source_url) if link_el is not None else source_url
        docs.append(
            SourceDocument(
                source_url=link.strip() or source_url,
                title=normalize_whitespace(title),
                summary=strip_html(summary),
                published_at=normalize_whitespace(published_at),
                raw_text=normalize_whitespace(f"{title} {strip_html(summary)}"),
            )
        )
    return docs


def parse_html(content: str, source_url: str) -> SourceDocument:
    parser = SimpleHTMLTextParser()
    parser.feed(content)
    text = parser.text()
    title = text.split(".")[0][:120] if text else source_url
    return SourceDocument(
        source_url=source_url,
        title=normalize_whitespace(title),
        summary=text[:280],
        published_at="",
        raw_text=text,
    )
