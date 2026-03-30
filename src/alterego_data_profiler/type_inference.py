"""Column type inference — maps Polars dtypes to ColumnType."""

from __future__ import annotations

import polars as pl

from .models import ColumnType

_DTYPE_MAP: dict[type, ColumnType] = {
    pl.Int8: ColumnType.integer,
    pl.Int16: ColumnType.integer,
    pl.Int32: ColumnType.integer,
    pl.Int64: ColumnType.integer,
    pl.UInt8: ColumnType.integer,
    pl.UInt16: ColumnType.integer,
    pl.UInt32: ColumnType.integer,
    pl.UInt64: ColumnType.integer,
    pl.Float32: ColumnType.float_,
    pl.Float64: ColumnType.float_,
    pl.Boolean: ColumnType.boolean,
    pl.Date: ColumnType.date,
    pl.Datetime: ColumnType.datetime,
    pl.Utf8: ColumnType.string,
    pl.String: ColumnType.string,
    pl.Null: ColumnType.null,
}


def infer_column_type(dtype: pl.DataType) -> ColumnType:
    """Map a Polars dtype to our ColumnType enum."""
    for pl_type, col_type in _DTYPE_MAP.items():
        if isinstance(dtype, pl_type):
            return col_type
    return ColumnType.string
