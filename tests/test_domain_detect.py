"""Tests for semantic domain detection."""

import polars as pl

from alterego_data_profiler.domain_detect import detect_domain
from alterego_data_profiler.models import SemanticType


class TestDetectDomain:
    def test_email_column(self):
        s = pl.Series(["alice@example.com", "bob@test.org", "carol@mail.co"])
        result = detect_domain(s)
        assert result.semantic_type == SemanticType.email
        assert result.confidence > 0.5

    def test_url_column(self):
        s = pl.Series(["https://example.com", "https://test.org", "http://foo.bar"])
        result = detect_domain(s)
        assert result.semantic_type == SemanticType.url

    def test_uuid_column(self):
        s = pl.Series([
            "550e8400-e29b-41d4-a716-446655440000",
            "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
        ])
        result = detect_domain(s)
        assert result.semantic_type == SemanticType.uuid

    def test_no_pattern_match(self):
        s = pl.Series(["apple", "banana", "cherry"])
        result = detect_domain(s)
        assert result.semantic_type == SemanticType.unknown

    def test_empty_series(self):
        s = pl.Series([], dtype=pl.Utf8)
        result = detect_domain(s)
        assert result.semantic_type == SemanticType.unknown

    def test_null_values_skipped(self):
        s = pl.Series(["alice@example.com", None, "bob@test.org", None])
        result = detect_domain(s)
        assert result.semantic_type == SemanticType.email
