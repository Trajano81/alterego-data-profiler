"""Partial file reader — loads a sample of rows from various formats."""

from __future__ import annotations

from pathlib import Path

import polars as pl

from .models import FileFormat


def read_partial(
    file_path: str | Path,
    format: FileFormat,
    encoding: str = "utf-8",
    sample_size: int = 1000,
) -> pl.DataFrame:
    """Read up to *sample_size* rows from *file_path* in the given format."""
    path = Path(file_path)

    if format == FileFormat.csv:
        return pl.read_csv(
            path, encoding=encoding, n_rows=sample_size, infer_schema_length=sample_size
        )

    if format == FileFormat.tsv:
        return pl.read_csv(
            path,
            separator="\t",
            encoding=encoding,
            n_rows=sample_size,
            infer_schema_length=sample_size,
        )

    if format == FileFormat.excel:
        df = pl.read_excel(path)
        return df.head(sample_size)

    if format == FileFormat.json:
        df = pl.read_json(path)
        return df.head(sample_size)

    if format == FileFormat.jsonl:
        return pl.read_ndjson(path, n_rows=sample_size)

    if format == FileFormat.parquet:
        return pl.read_parquet(path, n_rows=sample_size)

    msg = f"Unsupported format: {format.value}"
    raise ValueError(msg)
