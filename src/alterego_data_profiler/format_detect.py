"""Feature 2: File format detection using filetype + CSV/TSV sniffing."""

from __future__ import annotations

import csv
import io
from pathlib import Path

import filetype

from .models import FileFormat

_EXTENSION_MAP: dict[str, FileFormat] = {
    ".csv": FileFormat.csv,
    ".tsv": FileFormat.tsv,
    ".json": FileFormat.json,
    ".jsonl": FileFormat.jsonl,
    ".ndjson": FileFormat.jsonl,
    ".parquet": FileFormat.parquet,
    ".xlsx": FileFormat.excel,
    ".xls": FileFormat.excel,
    ".sql": FileFormat.sql_dump,
}

_GOOGLE_SHEETS_PREFIXES = (
    "https://docs.google.com/spreadsheets/",
    "http://docs.google.com/spreadsheets/",
)


def detect_format(file_path: str | Path) -> FileFormat:
    """Detect the format of a data file."""
    path_str = str(file_path)

    # Google Sheets URL check
    if any(path_str.startswith(p) for p in _GOOGLE_SHEETS_PREFIXES):
        return FileFormat.google_sheets

    path = Path(file_path)

    # Try filetype (binary magic-bytes detection) first
    guess = filetype.guess(str(path))
    if guess is not None:
        mime = guess.mime
        if "spreadsheet" in mime or "excel" in mime:
            return FileFormat.excel
        if "parquet" in mime:
            return FileFormat.parquet

    # Extension-based lookup
    ext = path.suffix.lower()
    if ext in _EXTENSION_MAP:
        return _EXTENSION_MAP[ext]

    # Text sniffing for CSV/TSV/JSON
    try:
        with open(path, "rb") as fh:
            head = fh.read(8192)
        text = head.decode("utf-8", errors="replace").strip()
    except OSError:
        return FileFormat.unknown

    if not text:
        return FileFormat.unknown

    # JSON / JSONL
    if text.startswith(("[", "{")):
        if "\n" in text and all(
            line.strip().startswith("{") for line in text.splitlines() if line.strip()
        ):
            return FileFormat.jsonl
        return FileFormat.json

    # CSV / TSV via csv.Sniffer
    try:
        dialect = csv.Sniffer().sniff(text)
        if dialect.delimiter == "\t":
            return FileFormat.tsv
        return FileFormat.csv
    except csv.Error:
        pass

    return FileFormat.unknown
