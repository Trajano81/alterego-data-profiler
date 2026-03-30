"""Tests for the partial file reader."""

from pathlib import Path

import polars as pl
import pytest

from alterego_data_profiler.models import FileFormat
from alterego_data_profiler.reader import read_partial

FIXTURES = Path(__file__).parent / "fixtures"


class TestReadPartial:
    def test_read_csv(self):
        df = read_partial(FIXTURES / "sample.csv", FileFormat.csv)
        assert isinstance(df, pl.DataFrame)
        assert len(df) == 10
        assert "id" in df.columns
        assert "name" in df.columns

    def test_read_tsv(self):
        df = read_partial(FIXTURES / "sample.tsv", FileFormat.tsv)
        assert len(df) == 10
        assert "email" in df.columns

    def test_read_json(self):
        df = read_partial(FIXTURES / "sample.json", FileFormat.json)
        assert len(df) == 10

    def test_read_jsonl(self):
        df = read_partial(FIXTURES / "sample.jsonl", FileFormat.jsonl)
        assert len(df) == 10

    def test_read_parquet(self):
        df = read_partial(FIXTURES / "sample.parquet", FileFormat.parquet)
        assert len(df) == 10

    def test_read_excel(self):
        df = read_partial(FIXTURES / "sample.xlsx", FileFormat.excel)
        assert len(df) == 10

    def test_sample_size_limit(self):
        df = read_partial(FIXTURES / "sample.csv", FileFormat.csv, sample_size=3)
        assert len(df) == 3

    def test_unsupported_format(self):
        with pytest.raises(ValueError, match="Unsupported format"):
            read_partial(FIXTURES / "sample.csv", FileFormat.sql_dump)
