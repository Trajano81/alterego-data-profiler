"""Per-column statistics computation."""

from __future__ import annotations

import polars as pl

from .models import (
    BooleanStats,
    ColumnStats,
    ColumnType,
    DateStats,
    NumericStats,
    StringStats,
)


def compute_column_stats(
    df: pl.DataFrame, col_name: str, col_type: ColumnType
) -> ColumnStats:
    """Compute statistics for a single column."""
    series = df[col_name]
    total = len(series)
    null_count = series.null_count()
    null_pct = null_count / total if total > 0 else 0.0
    unique_count = series.n_unique()
    cardinality_ratio = unique_count / total if total > 0 else 0.0

    stats = ColumnStats(
        null_count=null_count,
        null_pct=round(null_pct, 4),
        unique_count=unique_count,
        cardinality_ratio=round(cardinality_ratio, 4),
    )

    non_null = series.drop_nulls()

    if col_type in (ColumnType.integer, ColumnType.float_) and len(non_null) > 0:
        numeric = non_null.cast(pl.Float64)
        stats.numeric = NumericStats(
            min=float(numeric.min()),  # type: ignore[arg-type]
            max=float(numeric.max()),  # type: ignore[arg-type]
            mean=float(numeric.mean()),  # type: ignore[arg-type]
            median=float(numeric.median()),  # type: ignore[arg-type]
            std=float(numeric.std()) if len(numeric) > 1 else 0.0,  # type: ignore[arg-type]
            p25=float(numeric.quantile(0.25)),  # type: ignore[arg-type]
            p75=float(numeric.quantile(0.75)),  # type: ignore[arg-type]
        )

    elif col_type == ColumnType.string and len(non_null) > 0:
        lengths = non_null.cast(pl.Utf8).str.len_chars()
        value_counts = (
            non_null.value_counts()
            .sort("count", descending=True)
            .head(5)
        )
        most_common = [
            {str(col_name): row[col_name], "count": row["count"]}
            for row in value_counts.iter_rows(named=True)
        ]
        stats.string = StringStats(
            min_length=int(lengths.min()),  # type: ignore[arg-type]
            max_length=int(lengths.max()),  # type: ignore[arg-type]
            avg_length=round(float(lengths.mean()), 2),  # type: ignore[arg-type]
            most_common=most_common,
        )

    elif col_type == ColumnType.boolean and len(non_null) > 0:
        true_count = int(non_null.sum())  # type: ignore[arg-type]
        stats.boolean = BooleanStats(
            true_count=true_count,
            false_count=len(non_null) - true_count,
        )

    elif col_type in (ColumnType.date, ColumnType.datetime) and len(non_null) > 0:
        min_val = non_null.min()
        max_val = non_null.max()
        range_days = (max_val - min_val).days if min_val and max_val else None  # type: ignore[union-attr]
        stats.date = DateStats(
            min=str(min_val),
            max=str(max_val),
            range_days=range_days,
        )

    return stats
