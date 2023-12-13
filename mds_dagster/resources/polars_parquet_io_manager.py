"""
Polars Parquet IO Manager for writing and reading parquet files from polars
Creating to maintain the resource easier
"""
from dagster_polars import PolarsParquetIOManager

polars_parquet_io_manager_resource = PolarsParquetIOManager(
    base_dir="data/ingest/strava/"
)
