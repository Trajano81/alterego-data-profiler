"""PII detection — flags columns likely containing personal data."""

from __future__ import annotations

import polars as pl

from .models import PIIResult, SemanticType
from .patterns import get_patterns

_PII_THRESHOLD = 0.05  # 5% of sampled values must match


def detect_pii(series: pl.Series) -> PIIResult:
    """Check a column for PII patterns. Returns PIIResult."""
    non_null = series.drop_nulls().cast(pl.Utf8)
    total = len(non_null)
    if total == 0:
        return PIIResult()

    sample = non_null.head(min(total, 200))
    sample_size = len(sample)
    values = sample.to_list()

    detected_types: list[SemanticType] = []
    max_confidence = 0.0

    for pattern in get_patterns(pii_only=True):
        matches = sum(1 for v in values if pattern.regex.match(v))
        ratio = matches / sample_size
        if ratio >= _PII_THRESHOLD:
            detected_types.append(pattern.semantic_type)
            max_confidence = max(max_confidence, ratio)

    if not detected_types:
        return PIIResult()

    return PIIResult(
        pii_detected=True,
        pii_types=detected_types,
        confidence=round(max_confidence, 4),
    )
