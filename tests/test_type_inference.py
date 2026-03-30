"""Tests for column type inference."""

import polars as pl

from alterego_data_profiler.models import ColumnType
from alterego_data_profiler.type_inference import infer_column_type


class TestInferColumnType:
    def test_integer(self):
        assert infer_column_type(pl.Int64()) == ColumnType.integer
        assert infer_column_type(pl.Int32()) == ColumnType.integer
        assert infer_column_type(pl.UInt8()) == ColumnType.integer

    def test_float(self):
        assert infer_column_type(pl.Float64()) == ColumnType.float_
        assert infer_column_type(pl.Float32()) == ColumnType.float_

    def test_boolean(self):
        assert infer_column_type(pl.Boolean()) == ColumnType.boolean

    def test_string(self):
        assert infer_column_type(pl.Utf8()) == ColumnType.string

    def test_date(self):
        assert infer_column_type(pl.Date()) == ColumnType.date

    def test_datetime(self):
        assert infer_column_type(pl.Datetime()) == ColumnType.datetime

    def test_null(self):
        assert infer_column_type(pl.Null()) == ColumnType.null

    def test_unknown_defaults_to_string(self):
        assert infer_column_type(pl.Binary()) == ColumnType.string
