import polars as pl
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

    expected_df = pl.DataFrame({"_name": [1], "test_col": [1], "final_col": [1]})

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
