import polars as pl

from core_library.utilities.polars_dataframe_utils import pl_add_standard_cols

source_df = pl.DataFrame(
    {"Name": ["Alice", "Bob", "Charlie"], "Age": [24, 20, None], "ID": [1, 2, 3]}
)

print(pl_add_standard_cols(source_df, hash_cols=["ID", "Age"]))
