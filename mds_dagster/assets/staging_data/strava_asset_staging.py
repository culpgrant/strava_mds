"""
Generate the Strava assets within duckdb (staging tables)
"""
from dagster import AssetExecutionContext, asset

from core_library.utilities.custom_log import setup_console_logger
from mds_dagster.resources.duck_db_resource import MDSDuckDBResource

mds_logger = setup_console_logger()


@asset(
    compute_kind="duckdb",
    group_name="staging",
    deps=["raw_strava_ingest_athlete"],
)
def staging_strava_athlete(
    context: AssetExecutionContext, duckdb: MDSDuckDBResource
) -> None:
    """
    Create the DuckDB table for us to build DBT Models off of

    :param context: Dagster Context
    :type context: AssetExecutionContext
    :param duckdb: Dagster DuckDB Resource
    :type duckdb: DuckDBResource
    """
    mds_logger.info("Creating Duck DB Tables")
    schema_name = "staging"
    table_name = context.asset_key[0][0]

    # Ensure schema exists
    duckdb.create_schema(schema_name)

    # Create Table
    duckdb.execute_query(
        f"CREATE OR REPLACE TABLE {schema_name}.{table_name} AS FROM read_parquet('data/ingest/strava/raw_strava_ingest_athlete.parquet')"
    )

    table_metadata = duckdb.generate_dagster_metadata(
        table_name=table_name, schema_name=schema_name
    )

    # Getting this metadata should be implemented into a function
    context.add_output_metadata(metadata=table_metadata)
