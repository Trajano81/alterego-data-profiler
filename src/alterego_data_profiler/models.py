"""Pydantic models — the contract layer for alterego-data-profiler."""

from __future__ import annotations

import json
from enum import Enum
from typing import Any

import yaml
from pydantic import BaseModel, Field


# ── Enums ────────────────────────────────────────────────────────────────────


class FileFormat(str, Enum):
    csv = "csv"
    tsv = "tsv"
    excel = "excel"
    json = "json"
    jsonl = "jsonl"
    parquet = "parquet"
    sql_dump = "sql_dump"
    google_sheets = "google_sheets"
    unknown = "unknown"


class ColumnType(str, Enum):
    string = "string"
    integer = "integer"
    float_ = "float"
    boolean = "boolean"
    date = "date"
    datetime = "datetime"
    null = "null"


class SemanticType(str, Enum):
    email = "email"
    phone = "phone"
    url = "url"
    ip_address = "ip_address"
    uuid = "uuid"
    credit_card = "credit_card"
    ssn = "ssn"
    boolean_like = "boolean_like"
    date_like = "date_like"
    categorical = "categorical"
    currency = "currency"
    percentage = "percentage"
    zip_code = "zip_code"
    unknown = "unknown"


# ── Stats sub-models ─────────────────────────────────────────────────────────


class NumericStats(BaseModel):
    min: float | None = None
    max: float | None = None
    mean: float | None = None
    median: float | None = None
    std: float | None = None
    p25: float | None = None
    p75: float | None = None


class StringStats(BaseModel):
    min_length: int | None = None
    max_length: int | None = None
    avg_length: float | None = None
    most_common: list[dict[str, Any]] = Field(default_factory=list)


class BooleanStats(BaseModel):
    true_count: int = 0
    false_count: int = 0


class DateStats(BaseModel):
    min: str | None = None
    max: str | None = None
    range_days: int | None = None


class ColumnStats(BaseModel):
    null_count: int = 0
    null_pct: float = 0.0
    unique_count: int = 0
    cardinality_ratio: float = 0.0
    numeric: NumericStats | None = None
    string: StringStats | None = None
    boolean: BooleanStats | None = None
    date: DateStats | None = None


# ── Domain / PII ─────────────────────────────────────────────────────────────


class DomainDetection(BaseModel):
    semantic_type: SemanticType = SemanticType.unknown
    confidence: float = 0.0
    sample_matches: int = 0
    total: int = 0


class PIIResult(BaseModel):
    pii_detected: bool = False
    pii_types: list[SemanticType] = Field(default_factory=list)
    confidence: float = 0.0


# ── Column profile ───────────────────────────────────────────────────────────


class ColumnProfile(BaseModel):
    name: str
    position: int
    dtype: ColumnType = ColumnType.string
    stats: ColumnStats = Field(default_factory=ColumnStats)
    domain: DomainDetection = Field(default_factory=DomainDetection)
    pii: PIIResult = Field(default_factory=PIIResult)
    sample_values: list[Any] = Field(default_factory=list)
    description: str = ""


# ── File metadata ────────────────────────────────────────────────────────────


class FileMetadata(BaseModel):
    file_name: str = ""
    path: str = ""
    size_bytes: int = 0
    format: FileFormat = FileFormat.unknown
    encoding: str = "utf-8"
    encoding_confidence: float = 0.0
    row_count: int = 0
    column_count: int = 0


# ── Top-level profile ───────────────────────────────────────────────────────


class DatasetProfile(BaseModel):
    file: FileMetadata = Field(default_factory=FileMetadata)
    columns: list[ColumnProfile] = Field(default_factory=list)
    data_dictionary: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def to_yaml(self) -> str:
        return yaml.dump(
            self.to_dict(),
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
