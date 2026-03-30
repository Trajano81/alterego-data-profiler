"""Semantic domain detection via pattern matching."""

from __future__ import annotations

import polars as pl

from .models import DomainDetection, SemanticType
from .patterns import get_patterns


def detect_domain(series: pl.Series) -> DomainDetection:
    """Detect the semantic domain of a column by sampling values against patterns."""
    non_null = series.drop_nulls().cast(pl.Utf8)
    total = len(non_null)
    if total == 0:
        return DomainDetection()

    sample = non_null.head(min(total, 200))
    sample_size = len(sample)
    values = sample.to_list()

    best_type = SemanticType.unknown
    best_matches = 0

    for pattern in get_patterns():
        matches = sum(1 for v in values if pattern.regex.match(v))
        if matches > best_matches:
            best_matches = matches
            best_type = pattern.semantic_type

    if best_matches == 0:
        return DomainDetection()

    confidence = best_matches / sample_size
    return DomainDetection(
        semantic_type=best_type,
        confidence=round(confidence, 4),
        sample_matches=best_matches,
        total=total,
    )
