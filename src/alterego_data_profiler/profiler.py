"""Profiler orchestrator — wires all modules together."""

from __future__ import annotations

import os
from pathlib import Path

from .dictionary import build_data_dictionary
from .domain_detect import detect_domain
from .encoding_detect import detect_encoding
from .format_detect import detect_format
from .models import ColumnProfile, DatasetProfile, FileMetadata
from .pii_detect import detect_pii
from .reader import read_partial
from .statistics import compute_column_stats
from .type_inference import infer_column_type


def profile_dataset(
    file_path: str,
    *,
    sample_size: int = 1000,
    output: str = "json",
) -> DatasetProfile:
    """Profile a dataset file and return a DatasetProfile."""
    path = Path(file_path)

    # Format detection
    fmt = detect_format(path)

    # Encoding detection (skip for binary formats)
    if fmt.value in ("parquet", "excel"):
        encoding, enc_confidence = "binary", 1.0
    else:
        encoding, enc_confidence = detect_encoding(path)

    # Read partial data
    df = read_partial(path, fmt, encoding=encoding, sample_size=sample_size)

    # File metadata
    file_meta = FileMetadata(
        file_name=path.name,
        path=str(path.resolve()),
        size_bytes=os.path.getsize(path),
        format=fmt,
        encoding=encoding,
        encoding_confidence=round(enc_confidence, 4),
        row_count=len(df),
        column_count=len(df.columns),
    )

    # Column profiling
    columns: list[ColumnProfile] = []
    for i, col_name in enumerate(df.columns):
        col_type = infer_column_type(df[col_name].dtype)
        stats = compute_column_stats(df, col_name, col_type)
        domain = detect_domain(df[col_name])
        pii = detect_pii(df[col_name])

        sample_values = df[col_name].drop_nulls().head(5).to_list()

        columns.append(
            ColumnProfile(
                name=col_name,
                position=i,
                dtype=col_type,
                stats=stats,
                domain=domain,
                pii=pii,
                sample_values=sample_values,
            )
        )

    # Data dictionary
    data_dictionary = build_data_dictionary(columns)

    warnings: list[str] = []
    if len(df) >= sample_size:
        warnings.append(f"Results based on sample of {sample_size} rows")

    return DatasetProfile(
        file=file_meta,
        columns=columns,
        data_dictionary=data_dictionary,
        warnings=warnings,
    )
