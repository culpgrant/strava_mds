from datetime import datetime
from unittest.mock import patch

import polars as pl
import pytest
from polars.testing import assert_frame_equal

from core_library.utilities import polars_dataframe_utils


def test_pl_create_df():
    # Arrange
    data = {
        "Name": ["Alice", "Bob", "Charlie", "David"],
        "Age": [25, 22, 24, 23],
        "Grade": ["A", "B", "C", "B"],
    }

    expected_df = pl.DataFrame(
        {
            "Name": ["Alice", "Bob", "Charlie", "David"],
            "Age": [25, 22, 24, 23],
            "Grade": ["A", "B", "C", "B"],
        }
    )

    # Act
    result_df = polars_dataframe_utils.pl_create_df(data=data)

    assert_frame_equal(expected_df, result_df)


def test_pl_df_cols_to_standard():
    # Arrange
    input_df = pl.DataFrame({"$name": [1], "testCol": [1], "final_col": [1]})

    expected_df = pl.DataFrame({"_NAME": [1], "TEST_COL": [1], "FINAL_COL": [1]})

    # Act
    result_df = polars_dataframe_utils.pl_df_cols_to_standard(input_df)

    assert_frame_equal(result_df, expected_df)


def test_pl_concat_dfs():
    # Arrange
    df_1 = pl.DataFrame(
        {
            "Name": ["Alice", "Bob"],
            "Age": [25, 22],
        }
    )
    df_2 = pl.DataFrame(
        {
            "Name": ["Charlie", "David"],
            "Age": [24, 23],
        }
    )

    expected_df = pl.DataFrame(
        {
            "Name": ["Alice", "Bob", "Charlie", "David"],
            "Age": [25, 22, 24, 23],
        }
    )

    # Act
    result_df = polars_dataframe_utils.pl_concat_dfs([df_1, df_2])

    assert_frame_equal(expected_df, result_df)


def test_pl_aggregate_column():
    # Arrange
    source_df = pl.DataFrame(
        {
            "Name": ["Alice", "Bob", "Charlie", "David"],
            "Age": [25, 22, 24, 23],
        }
    )

    # Act
    max_age = polars_dataframe_utils.pl_aggregate_column(
        source_df, "Age", agg_type="max"
    )
    min_age = polars_dataframe_utils.pl_aggregate_column(
        source_df, "Age", agg_type="min"
    )

    # Assert
    assert max_age == 25
    assert min_age == 22

    # Arrange
    source_df = pl.DataFrame()

    # Act
    result = polars_dataframe_utils.pl_aggregate_column(source_df, "test", "max")

    assert result is None


def test_pl_log_dataframe():
    source_df = pl.DataFrame()

    result = polars_dataframe_utils.pl_log_dataframe(source_df)

    assert result is None

    with pytest.raises(Exception) as exc:
        result = polars_dataframe_utils.pl_log_dataframe(source_df, order_by="test")
        assert str(exc.value) == "order_by and ascending arguments are both required"


def test_pl_check_empty_df():
    source_df = pl.DataFrame()

    result = polars_dataframe_utils.pl_check_empty_df(source_df)

    assert result is True

    source_df = pl.DataFrame(
        {
            "Name": ["Alice", "Bob", "Charlie", "David"],
            "Age": [25, 22, 24, 23],
        }
    )

    result = polars_dataframe_utils.pl_check_empty_df(source_df)

    assert result is False


def test_pl_concat_str():
    # Arrange
    source_df = pl.DataFrame(
        {
            "Name": ["Alice", "Bob", "Charlie"],
            "Age": [25, 22, 24],
        }
    )

    expected_df = pl.DataFrame(
        {
            "Name": ["Alice", "Bob", "Charlie"],
            "Age": [25, 22, 24],
            "CUSTOM_CONT": ["Alice25", "Bob22", "Charlie24"],
        }
    )

    actual_df = polars_dataframe_utils.pl_concat_str(
        source_df, cols=["Name", "Age"], alias="CUSTOM_CONT"
    )

    assert_frame_equal(expected_df, actual_df)


def test_pl_hash_func():
    # Arrange
    source_df = pl.DataFrame(
        {
            "Name": ["Alice", "Bob", "Charlie"],
            "Age": [25, 22, 24],
        }
    )

    expected_df = pl.DataFrame(
        {
            "Name": ["Alice", "Bob", "Charlie"],
            "Age": [25, 22, 24],
            "HASH_NAME": [
                "3bc51062973c458d5a6f2d8d64a023246354ad7e064b1e4e009ec8a0699a3043",
                "cd9fb1e148ccd8442e5aa74904cc73bf6fb54d1d54d333bd596aa9bb4bb4e961",
                "6e81b1255ad51bb201a2b8afa9b66653297ae0217f833b14b39b5231228bf968",
            ],
        }
    )

    actual_df = polars_dataframe_utils.pl_hash_func(
        source_df, cols="Name", alias="HASH_NAME", drop_concat_col=True
    )

    assert_frame_equal(expected_df, actual_df)


@patch("core_library.utilities.polars_dataframe_utils.datetime")
def test_pl_add_standard_cols(mock_dt):
    expected_dt = datetime(2024, 1, 28, 13, 00, 29, 362840)

    mock_dt.now.return_value = expected_dt

    # Arrange
    source_df = pl.DataFrame(
        {
            "Name": ["Alice", "Bob", "Charlie"],
            "Age": [25, 22, 24],
        }
    )

    result_df = polars_dataframe_utils.pl_add_standard_cols(
        source_df, hash_cols=["Name", "Age"]
    )

    expected_df = pl.DataFrame(
        {
            "Name": ["Alice", "Bob", "Charlie"],
            "Age": [25, 22, 24],
            "KEY_CONCAT": ["Alice25", "Bob22", "Charlie24"],
            "KEY_HASH": [
                "82d5bee2b2424626580aaab8a72724e7f01ad63302eef674db9849f2dbc5d8d9",
                "91abcb6238966bc9c402f3ce1113fb3e7f4bee6d972b702f041ab98845a53fa6",
                "dc027e69b00988c9cfc869997584bf01367c2d8bc3dfe3418efe3daa3af3b675",
            ],
            "INGESTION_DATE_TIME": [expected_dt, expected_dt, expected_dt],
        }
    )

    assert_frame_equal(result_df, expected_df)
