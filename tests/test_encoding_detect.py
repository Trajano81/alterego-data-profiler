"""Tests for encoding detection."""

from pathlib import Path

from alterego_data_profiler.encoding_detect import detect_encoding

FIXTURES = Path(__file__).parent / "fixtures"


class TestDetectEncoding:
    def test_utf8_file(self):
        enc, conf = detect_encoding(FIXTURES / "sample.csv")
        assert enc.lower().replace("-", "") in ("utf8", "ascii")
        assert conf > 0.5

    def test_latin1_file(self):
        enc, conf = detect_encoding(FIXTURES / "sample_latin1.csv")
        # charset-normalizer should detect it as a latin variant or windows-1252
        assert conf > 0.0
        assert enc is not None

    def test_returns_tuple(self):
        result = detect_encoding(FIXTURES / "sample.csv")
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert isinstance(result[1], float)
