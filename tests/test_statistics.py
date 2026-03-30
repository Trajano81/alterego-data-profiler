"""Tests for per-column statistics."""

import polars as pl

from alterego_data_profiler.models import ColumnType
from alterego_data_profiler.statistics import compute_column_stats


class TestComputeColumnStats:
    def test_numeric_stats(self):
        df = pl.DataFrame({"val": [1, 2, 3, 4, 5, None]})
        stats = compute_column_stats(df, "val", ColumnType.integer)
        assert stats.null_count == 1
        assert stats.unique_count == 6  # includes null
        assert stats.numeric is not None
        assert stats.numeric.min == 1.0
        assert stats.numeric.max == 5.0
        assert stats.numeric.mean == 3.0

    def test_string_stats(self):
        df = pl.DataFrame({"name": ["alice", "bob", "charlie", "alice", "bob"]})
        stats = compute_column_stats(df, "name", ColumnType.string)
        assert stats.null_count == 0
        assert stats.string is not None
        assert stats.string.min_length == 3  # "bob"
        assert stats.string.max_length == 7  # "charlie"
        assert len(stats.string.most_common) > 0

    def test_boolean_stats(self):
        df = pl.DataFrame({"flag": [True, True, False, True, False]})
        stats = compute_column_stats(df, "flag", ColumnType.boolean)
        assert stats.boolean is not None
        assert stats.boolean.true_count == 3
        assert stats.boolean.false_count == 2

    def test_date_stats(self):
        df = pl.DataFrame({"dt": ["2024-01-01", "2024-06-15", "2024-12-31"]})
        df = df.with_columns(pl.col("dt").str.to_date())
        stats = compute_column_stats(df, "dt", ColumnType.date)
        assert stats.date is not None
        assert stats.date.range_days == 365

    def test_null_pct(self):
        df = pl.DataFrame({"x": [1, None, None, 4, 5]})
        stats = compute_column_stats(df, "x", ColumnType.integer)
        assert stats.null_pct == 0.4

    def test_empty_series(self):
        df = pl.DataFrame({"x": pl.Series([], dtype=pl.Int64)})
        stats = compute_column_stats(df, "x", ColumnType.integer)
        assert stats.null_count == 0
        assert stats.numeric is None
