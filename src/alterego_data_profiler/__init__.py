"""alterego-data-profiler — dataset profiling for the AlterEgo ecosystem."""

from ._version import __version__
from .models import (
    BooleanStats,
    ColumnProfile,
    ColumnStats,
    ColumnType,
    DatasetProfile,
    DateStats,
    DomainDetection,
    FileFormat,
    FileMetadata,
    NumericStats,
    PIIResult,
    SemanticType,
    StringStats,
)
from .profiler import profile_dataset

__all__ = [
    "__version__",
    "profile_dataset",
    "DatasetProfile",
    "ColumnProfile",
    "ColumnStats",
    "ColumnType",
    "FileFormat",
    "FileMetadata",
    "SemanticType",
    "NumericStats",
    "StringStats",
    "BooleanStats",
    "DateStats",
    "DomainDetection",
    "PIIResult",
]
