"""
Generate the Strava assets within duckdb (staging tables)
"""
from dagster import AssetExecutionContext, asset

from core_library.utilities.custom_log import setup_console_logger
from mds_dagster.resources.duck_db_resource import MDSDuckDBResource

mds_logger = setup_console_logger()

# TODO: There has to be a better way to do this
# I am just running the same query every time but they are different assets.
#
# TODO: we are building into a schema called "staging" and all the table names are prefixed with "staging_"
#   - We could strip staging_ out of the asset name. But I kind of like having it in the asset name.
#   - Might not be worth it


@asset(
    compute_kind="duckdb",
    group_name="staging",
    deps=["raw_ingest_strava_athlete"],
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
        f"CREATE OR REPLACE TABLE {schema_name}.{table_name} AS FROM read_parquet('data/ingest/strava/raw_ingest_strava_athlete.parquet')"
    )

    table_metadata = duckdb.generate_dagster_metadata(
        table_name=table_name, schema_name=schema_name
    )

    context.add_output_metadata(metadata=table_metadata)


@asset(
    compute_kind="duckdb",
    group_name="staging",
    deps=["raw_ingest_strava_equipment"],
)
def staging_strava_equipment(
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
        f"CREATE OR REPLACE TABLE {schema_name}.{table_name} AS FROM read_parquet('data/ingest/strava/raw_ingest_strava_equipment.parquet')"
    )

    table_metadata = duckdb.generate_dagster_metadata(
        table_name=table_name, schema_name=schema_name
    )

    context.add_output_metadata(metadata=table_metadata)


@asset(
    compute_kind="duckdb",
    group_name="staging",
    deps=["raw_ingest_strava_athlete_stats"],
)
def staging_strava_athlete_stats(
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
        f"CREATE OR REPLACE TABLE {schema_name}.{table_name} AS FROM read_parquet('data/ingest/strava/raw_ingest_strava_athlete_stats.parquet')"
    )

    table_metadata = duckdb.generate_dagster_metadata(
        table_name=table_name, schema_name=schema_name
    )

    context.add_output_metadata(metadata=table_metadata)
