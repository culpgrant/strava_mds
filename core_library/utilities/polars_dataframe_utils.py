"""
Utilities for working with polars dataframes
"""
from datetime import datetime
from typing import Dict, List, Optional, Union

import polars as pl
from polars.type_aliases import FrameInitTypes

from core_library.utilities.custom_log import setup_console_logger
from core_library.utilities.text_utils import cols_text_to_standard

mds_logger = setup_console_logger()


def pl_create_df(data: FrameInitTypes, schema: Optional[Dict] = None) -> pl.DataFrame:
    """Create a Polars Dataframe

    :param data: Data to create DF
    :type data: FrameInitTypes
    :param schema: Schema dictionary for the polars dataframe
    :type schema: Dict
    :return: Polars Dataframe
    :rtype: pl.DataFrame
    """
    mds_logger.info("Converting to dataframe")
    df = pl.DataFrame(data=data, schema=schema)
    return df


def pl_df_cols_to_standard(df: pl.DataFrame):
    """Convert polars dataframe columns to standard used"""
    mds_logger.info("Converting dataframe cols to standard")
    for col in df.columns:
        new_col = cols_text_to_standard(col)
        df = df.rename({col: new_col})

    return df


def pl_concat_dfs(list_of_dfs: List[pl.DataFrame], **kwargs) -> pl.DataFrame:
    """
    Helpful function to take in a list of dataframes and concatenate them

    :param list_of_dfs: List of dataframes
    :type list_of_dfs: List[pl.DataFrame]
    :return: One dataframe
    :rtype: pl.DataFrame
    """

    result_df = pl.concat(items=list_of_dfs, **kwargs)

    return result_df


def pl_aggregate_column(
    df: pl.DataFrame, column_name: str, agg_type: str
) -> Union[int, str, datetime, None]:
    """
    Aggregate a single column and get back one record as a native python type

    :param df: Dataframe to aggregate
    :type df: pl.DataFrame
    :param column_name: Column to aggregate
    :type column_name: str
    :param agg_type: type of aggregation to use
    :type agg_type: str
    :return: Result from dataframe in native python type
    :rtype: Union[int, str, datetime, None]
    """
    result = None

    if agg_type == "max":
        result = df.select(pl.col(column_name)).max()[column_name][0]
    elif agg_type == "min":
        result = df.select(pl.col(column_name)).min()[column_name][0]

    return result
