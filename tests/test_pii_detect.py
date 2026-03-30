"""Tests for PII detection."""

import polars as pl

from alterego_data_profiler.models import SemanticType
from alterego_data_profiler.pii_detect import detect_pii


class TestDetectPII:
    def test_email_pii(self):
        s = pl.Series(["alice@example.com", "bob@test.org", "carol@mail.co"])
        result = detect_pii(s)
        assert result.pii_detected is True
        assert SemanticType.email in result.pii_types
        assert result.confidence > 0.5

    def test_credit_card_pii(self):
        s = pl.Series(["4111111111111111", "5500000000000004", "3400000000000009"])
        result = detect_pii(s)
        assert result.pii_detected is True
        assert SemanticType.credit_card in result.pii_types

    def test_ssn_pii(self):
        s = pl.Series(["123-45-6789", "987-65-4321", "111-22-3333"])
        result = detect_pii(s)
        assert result.pii_detected is True
        assert SemanticType.ssn in result.pii_types

    def test_no_pii(self):
        s = pl.Series(["apple", "banana", "cherry", "date"])
        result = detect_pii(s)
        assert result.pii_detected is False
        assert result.pii_types == []

    def test_empty_series(self):
        s = pl.Series([], dtype=pl.Utf8)
        result = detect_pii(s)
        assert result.pii_detected is False

    def test_below_threshold(self):
        # Only 1 out of 100 values is a match = 1% < 5% threshold
        values = ["not-pii"] * 99 + ["alice@example.com"]
        s = pl.Series(values)
        result = detect_pii(s)
        assert result.pii_detected is False
