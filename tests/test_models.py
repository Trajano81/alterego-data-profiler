"""Tests for Pydantic models."""

import json

import yaml

from alterego_data_profiler.models import (
    ColumnProfile,
    ColumnStats,
    ColumnType,
    DatasetProfile,
    FileFormat,
    FileMetadata,
    NumericStats,
    SemanticType,
    StringStats,
)


class TestEnums:
    def test_file_format_values(self):
        assert FileFormat.csv.value == "csv"
        assert FileFormat.parquet.value == "parquet"
        assert FileFormat.unknown.value == "unknown"

    def test_column_type_values(self):
        assert ColumnType.string.value == "string"
        assert ColumnType.integer.value == "integer"
        assert ColumnType.float_.value == "float"

    def test_semantic_type_values(self):
        assert SemanticType.email.value == "email"
        assert SemanticType.unknown.value == "unknown"


class TestColumnStats:
    def test_defaults(self):
        stats = ColumnStats()
        assert stats.null_count == 0
        assert stats.null_pct == 0.0
        assert stats.unique_count == 0
        assert stats.numeric is None
        assert stats.string is None

    def test_with_numeric(self):
        stats = ColumnStats(
            null_count=2,
            null_pct=0.2,
            unique_count=8,
            cardinality_ratio=0.8,
            numeric=NumericStats(min=1.0, max=100.0, mean=50.0),
        )
        assert stats.numeric.min == 1.0
        assert stats.numeric.max == 100.0

    def test_with_string(self):
        stats = ColumnStats(
            string=StringStats(min_length=3, max_length=50, avg_length=15.5),
        )
        assert stats.string.min_length == 3


class TestColumnProfile:
    def test_defaults(self):
        col = ColumnProfile(name="test_col", position=0)
        assert col.name == "test_col"
        assert col.dtype == ColumnType.string
        assert col.stats.null_count == 0
        assert col.pii.pii_detected is False

    def test_full_column(self):
        col = ColumnProfile(
            name="age",
            position=2,
            dtype=ColumnType.integer,
            sample_values=[25, 30, 35],
            description="User age in years",
        )
        assert col.dtype == ColumnType.integer
        assert len(col.sample_values) == 3


class TestFileMetadata:
    def test_defaults(self):
        meta = FileMetadata()
        assert meta.format == FileFormat.unknown
        assert meta.encoding == "utf-8"

    def test_populated(self):
        meta = FileMetadata(
            file_name="data.csv",
            path="/tmp/data.csv",
            size_bytes=1024,
            format=FileFormat.csv,
            encoding="utf-8",
            encoding_confidence=0.99,
            row_count=100,
            column_count=5,
        )
        assert meta.format == FileFormat.csv
        assert meta.row_count == 100


class TestDatasetProfile:
    def test_defaults(self):
        profile = DatasetProfile()
        assert profile.file.format == FileFormat.unknown
        assert profile.columns == []

    def test_to_dict(self):
        profile = DatasetProfile(
            file=FileMetadata(file_name="test.csv", format=FileFormat.csv),
            columns=[ColumnProfile(name="id", position=0, dtype=ColumnType.integer)],
        )
        d = profile.to_dict()
        assert d["file"]["file_name"] == "test.csv"
        assert d["file"]["format"] == "csv"
        assert len(d["columns"]) == 1
        assert d["columns"][0]["name"] == "id"

    def test_to_json(self):
        profile = DatasetProfile(
            file=FileMetadata(file_name="test.csv", format=FileFormat.csv),
        )
        j = profile.to_json()
        parsed = json.loads(j)
        assert parsed["file"]["file_name"] == "test.csv"

    def test_to_yaml(self):
        profile = DatasetProfile(
            file=FileMetadata(file_name="test.csv", format=FileFormat.csv),
        )
        y = profile.to_yaml()
        parsed = yaml.safe_load(y)
        assert parsed["file"]["file_name"] == "test.csv"

    def test_roundtrip_json(self):
        profile = DatasetProfile(
            file=FileMetadata(
                file_name="data.parquet",
                format=FileFormat.parquet,
                row_count=500,
                column_count=10,
            ),
            columns=[
                ColumnProfile(name="id", position=0, dtype=ColumnType.integer),
                ColumnProfile(name="name", position=1, dtype=ColumnType.string),
            ],
            warnings=["Sampled 500 of 10000 rows"],
        )
        j = profile.to_json()
        parsed = json.loads(j)
        restored = DatasetProfile(**parsed)
        assert restored.file.format == FileFormat.parquet
        assert len(restored.columns) == 2
        assert restored.warnings == ["Sampled 500 of 10000 rows"]
