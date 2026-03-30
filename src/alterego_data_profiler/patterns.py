"""Shared regex pattern registry for domain and PII detection."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .models import SemanticType


@dataclass
class Pattern:
    name: str
    semantic_type: SemanticType
    regex: re.Pattern[str]
    tier: int = 1  # 1 = structural, 2 = heuristic
    is_pii: bool = False


_REGISTRY: list[Pattern] = []


def register_pattern(
    name: str,
    semantic_type: SemanticType,
    regex: str,
    *,
    tier: int = 1,
    is_pii: bool = False,
    flags: int = 0,
) -> Pattern:
    """Register a new pattern in the global registry."""
    pattern = Pattern(
        name=name,
        semantic_type=semantic_type,
        regex=re.compile(regex, flags),
        tier=tier,
        is_pii=is_pii,
    )
    _REGISTRY.append(pattern)
    return pattern


def get_patterns(*, pii_only: bool = False, max_tier: int = 2) -> list[Pattern]:
    """Return patterns from the registry, optionally filtered."""
    return [
        p
        for p in _REGISTRY
        if p.tier <= max_tier and (not pii_only or p.is_pii)
    ]


def clear_registry() -> None:
    """Clear all registered patterns (useful for testing)."""
    _REGISTRY.clear()


# ── Tier 1: Structural patterns ─────────────────────────────────────────────

register_pattern(
    "email",
    SemanticType.email,
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    is_pii=True,
)

register_pattern(
    "url",
    SemanticType.url,
    r"^https?://[^\s]+$",
)

register_pattern(
    "uuid",
    SemanticType.uuid,
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
)

register_pattern(
    "ip_address",
    SemanticType.ip_address,
    r"^(?:\d{1,3}\.){3}\d{1,3}$",
)

register_pattern(
    "credit_card",
    SemanticType.credit_card,
    r"^\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}$",
    is_pii=True,
)

register_pattern(
    "ssn",
    SemanticType.ssn,
    r"^\d{3}-\d{2}-\d{4}$",
    is_pii=True,
)

# ── Tier 2: Heuristic patterns ──────────────────────────────────────────────

register_pattern(
    "phone",
    SemanticType.phone,
    r"^[\+]?[\d\s\-\(\)]{7,15}$",
    tier=2,
    is_pii=True,
)

register_pattern(
    "zip_code",
    SemanticType.zip_code,
    r"^\d{5}(?:-\d{4})?$",
    tier=2,
)

register_pattern(
    "boolean_like",
    SemanticType.boolean_like,
    r"^(?:true|false|yes|no|si|sí|0|1)$",
    tier=2,
    flags=re.IGNORECASE,
)

register_pattern(
    "currency",
    SemanticType.currency,
    r"^[\$€£¥]\s?\d[\d,.]*$",
    tier=2,
)

register_pattern(
    "percentage",
    SemanticType.percentage,
    r"^\d+(?:\.\d+)?%$",
    tier=2,
)
