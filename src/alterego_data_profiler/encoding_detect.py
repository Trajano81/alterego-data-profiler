"""Encoding detection using charset-normalizer."""

from __future__ import annotations

from pathlib import Path

from charset_normalizer import from_path


def detect_encoding(file_path: str | Path) -> tuple[str, float]:
    """Detect the encoding of a file.

    Returns (encoding_name, confidence) where confidence is 0.0–1.0.
    """
    result = from_path(str(file_path))
    best = result.best()
    if best is None:
        return ("utf-8", 0.0)
    encoding = best.encoding
    confidence = 1.0 - best.chaos  # chaos is 0.0 (clean) to 1.0 (garbage)
    return (encoding, max(0.0, min(1.0, confidence)))
