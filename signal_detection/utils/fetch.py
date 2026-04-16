from __future__ import annotations

from pathlib import Path
from urllib.request import Request, urlopen


def fetch_source(source: str, timeout: int = 10) -> str:
    if source.startswith(("http://", "https://")):
        request = Request(source, headers={"User-Agent": "signal-detector/1.0"})
        with urlopen(request, timeout=timeout) as response:
            return response.read().decode("utf-8", errors="ignore")

    return Path(source).read_text(encoding="utf-8", errors="ignore")
