"""Tests for data dictionary generation."""

from alterego_data_profiler.dictionary import build_data_dictionary
from alterego_data_profiler.models import (
    ColumnProfile,
    ColumnStats,
    ColumnType,
    DomainDetection,
    PIIResult,
    SemanticType,
)


class TestBuildDataDictionary:
    def test_basic_columns(self):
        columns = [
            ColumnProfile(name="id", position=0, dtype=ColumnType.integer),
            ColumnProfile(name="name", position=1, dtype=ColumnType.string),
        ]
        dd = build_data_dictionary(columns)
        assert len(dd) == 2
        assert dd[0]["column"] == "id"
        assert dd[0]["type"] == "integer"
        assert dd[1]["column"] == "name"

    def test_includes_domain(self):
        col = ColumnProfile(
            name="email",
            position=0,
            domain=DomainDetection(
                semantic_type=SemanticType.email, confidence=0.95
            ),
        )
        dd = build_data_dictionary([col])
        assert dd[0]["semantic_type"] == "email"
        assert dd[0]["domain_confidence"] == 0.95

    def test_includes_pii(self):
        col = ColumnProfile(
            name="ssn",
            position=0,
            pii=PIIResult(
                pii_detected=True,
                pii_types=[SemanticType.ssn],
                confidence=0.9,
            ),
        )
        dd = build_data_dictionary([col])
        assert dd[0]["pii"] is True
        assert "ssn" in dd[0]["pii_types"]

    def test_empty_columns(self):
        dd = build_data_dictionary([])
        assert dd == []

    def test_no_domain_no_pii(self):
        col = ColumnProfile(name="x", position=0)
        dd = build_data_dictionary([col])
        assert "semantic_type" not in dd[0]
        assert "pii" not in dd[0]
