"""Tests for the profiler orchestrator and integration."""

import json
from pathlib import Path

import yaml

from alterego_data_profiler.models import FileFormat
from alterego_data_profiler.profiler import profile_dataset

FIXTURES = Path(__file__).parent / "fixtures"


class TestProfileDataset:
    def test_csv_profile(self):
        result = profile_dataset(str(FIXTURES / "sample.csv"), sample_size=100)
        assert result.file.format == FileFormat.csv
        assert result.file.row_count == 10
        assert result.file.column_count == 6
        assert len(result.columns) == 6
        assert result.to_json()
        assert result.to_yaml()

    def test_tsv_profile(self):
        result = profile_dataset(str(FIXTURES / "sample.tsv"), sample_size=100)
        assert result.file.format == FileFormat.tsv

    def test_json_profile(self):
        result = profile_dataset(str(FIXTURES / "sample.json"), sample_size=100)
        assert result.file.format == FileFormat.json
        assert len(result.columns) > 0

    def test_jsonl_profile(self):
        result = profile_dataset(str(FIXTURES / "sample.jsonl"), sample_size=100)
        assert result.file.format == FileFormat.jsonl

    def test_parquet_profile(self):
        result = profile_dataset(str(FIXTURES / "sample.parquet"), sample_size=100)
        assert result.file.format == FileFormat.parquet

    def test_excel_profile(self):
        result = profile_dataset(str(FIXTURES / "sample.xlsx"), sample_size=100)
        assert result.file.format == FileFormat.excel

    def test_data_dictionary_generated(self):
        result = profile_dataset(str(FIXTURES / "sample.csv"), sample_size=100)
        assert len(result.data_dictionary) == 6
        assert result.data_dictionary[0]["column"] == "id"

    def test_column_stats_populated(self):
        result = profile_dataset(str(FIXTURES / "sample.csv"), sample_size=100)
        id_col = next(c for c in result.columns if c.name == "id")
        assert id_col.stats.unique_count > 0

    def test_email_domain_detection(self):
        result = profile_dataset(str(FIXTURES / "sample.csv"), sample_size=100)
        email_col = next(c for c in result.columns if c.name == "email")
        assert email_col.domain.semantic_type.value == "email"
        assert email_col.pii.pii_detected is True

    def test_to_json_valid(self):
        result = profile_dataset(str(FIXTURES / "sample.csv"), sample_size=100)
        parsed = json.loads(result.to_json())
        assert "file" in parsed
        assert "columns" in parsed

    def test_to_yaml_valid(self):
        result = profile_dataset(str(FIXTURES / "sample.csv"), sample_size=100)
        parsed = yaml.safe_load(result.to_yaml())
        assert "file" in parsed
        assert "columns" in parsed

    def test_sample_size_warning(self):
        result = profile_dataset(str(FIXTURES / "sample.csv"), sample_size=5)
        # 10 rows > 5 sample_size, but we only read 5
        assert result.file.row_count == 5
