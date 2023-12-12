"""
Utilities for working with polars dataframes
"""
from typing import Dict, Optional

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
