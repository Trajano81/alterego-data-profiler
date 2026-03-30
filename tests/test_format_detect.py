"""Tests for file format detection."""

from pathlib import Path

from alterego_data_profiler.format_detect import detect_format
from alterego_data_profiler.models import FileFormat

FIXTURES = Path(__file__).parent / "fixtures"


class TestDetectFormat:
    def test_csv(self):
        assert detect_format(FIXTURES / "sample.csv") == FileFormat.csv

    def test_tsv(self):
        assert detect_format(FIXTURES / "sample.tsv") == FileFormat.tsv

    def test_json(self):
        assert detect_format(FIXTURES / "sample.json") == FileFormat.json

    def test_jsonl(self):
        assert detect_format(FIXTURES / "sample.jsonl") == FileFormat.jsonl

    def test_parquet(self):
        assert detect_format(FIXTURES / "sample.parquet") == FileFormat.parquet

    def test_excel(self):
        assert detect_format(FIXTURES / "sample.xlsx") == FileFormat.excel

    def test_google_sheets_url(self):
        url = "https://docs.google.com/spreadsheets/d/abc123/edit"
        assert detect_format(url) == FileFormat.google_sheets

    def test_unknown_file(self, tmp_path):
        f = tmp_path / "mystery.xyz"
        f.write_text("some random content")
        result = detect_format(f)
        # Extension unknown, sniffing might pick it up as csv or unknown
        assert isinstance(result, FileFormat)
