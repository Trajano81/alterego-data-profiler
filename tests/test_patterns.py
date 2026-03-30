"""Tests for the shared regex pattern registry."""

from alterego_data_profiler.models import SemanticType
from alterego_data_profiler.patterns import get_patterns, register_pattern, clear_registry


class TestPatternRegistry:
    def test_default_patterns_loaded(self):
        patterns = get_patterns()
        assert len(patterns) > 0
        names = [p.name for p in patterns]
        assert "email" in names
        assert "url" in names
        assert "uuid" in names

    def test_pii_filter(self):
        pii = get_patterns(pii_only=True)
        assert all(p.is_pii for p in pii)
        names = [p.name for p in pii]
        assert "email" in names
        assert "credit_card" in names

    def test_tier_filter(self):
        tier1 = get_patterns(max_tier=1)
        assert all(p.tier <= 1 for p in tier1)

    def test_email_pattern_matches(self):
        patterns = get_patterns()
        email_pat = next(p for p in patterns if p.name == "email")
        assert email_pat.regex.match("user@example.com")
        assert not email_pat.regex.match("not-an-email")

    def test_uuid_pattern_matches(self):
        patterns = get_patterns()
        uuid_pat = next(p for p in patterns if p.name == "uuid")
        assert uuid_pat.regex.match("550e8400-e29b-41d4-a716-446655440000")
        assert not uuid_pat.regex.match("not-a-uuid")

    def test_credit_card_pattern(self):
        patterns = get_patterns()
        cc_pat = next(p for p in patterns if p.name == "credit_card")
        assert cc_pat.regex.match("4111111111111111")
        assert cc_pat.regex.match("4111-1111-1111-1111")

    def test_boolean_like_pattern(self):
        patterns = get_patterns()
        bool_pat = next(p for p in patterns if p.name == "boolean_like")
        for val in ("true", "false", "yes", "no", "True", "YES", "0", "1"):
            assert bool_pat.regex.match(val), f"Should match: {val}"
