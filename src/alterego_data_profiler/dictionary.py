"""Data dictionary generation from column profiles."""

from __future__ import annotations

from typing import Any

from .models import ColumnProfile


def build_data_dictionary(columns: list[ColumnProfile]) -> list[dict[str, Any]]:
    """Build a data dictionary from a list of ColumnProfile objects."""
    dictionary = []
    for col in columns:
        entry: dict[str, Any] = {
            "column": col.name,
            "position": col.position,
            "type": col.dtype.value,
            "null_pct": col.stats.null_pct,
            "unique_count": col.stats.unique_count,
            "cardinality_ratio": col.stats.cardinality_ratio,
        }
        if col.domain.semantic_type.value != "unknown":
            entry["semantic_type"] = col.domain.semantic_type.value
            entry["domain_confidence"] = col.domain.confidence
        if col.pii.pii_detected:
            entry["pii"] = True
            entry["pii_types"] = [t.value for t in col.pii.pii_types]
        if col.description:
            entry["description"] = col.description
        dictionary.append(entry)
    return dictionary
