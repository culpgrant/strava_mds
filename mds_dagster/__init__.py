import warnings

from dagster import (
    Definitions,
    EnvVar,
    load_assets_from_modules,
)

from core_library.dagster import dagster_asset_check_factory
from mds_dagster.assets.ingest import strava_asset
from mds_dagster.assets.staging_data import strava_asset_staging
from mds_dagster.jobs.assets.ingest.strava_jobs import strava_job
from mds_dagster.resources.duck_db_resource import MDSDuckDBResource
from mds_dagster.resources.ingest.strava_resource import StravaHandlerResource
from mds_dagster.resources.polars_parquet_io_manager import (
    polars_parquet_io_manager_resource,
)
from mds_dagster.schedules import strava_schedule

warnings.simplefilter("ignore")

all_assets = load_assets_from_modules([strava_asset, strava_asset_staging])
all_asset_checks = dagster_asset_check_factory.dagster_load_all_checks()


defs = Definitions(
    assets=all_assets,
    resources={
        "strava_api_resource": StravaHandlerResource(
            strava_client_id=EnvVar("strava_api_client_id"),
            strava_client_secret=EnvVar("strava_api_client_secret"),
            grant_type="refresh_token",
            refresh_token=EnvVar("strava_api_refresh_token"),
        ),
        # TODO: There has to be a better way to do this. I would like to define this dynamically
        # TODO: This Resource in Dagster web ui is not showing as being used
        "polars_parquet_io_manager_strava_ingest": polars_parquet_io_manager_resource,
        "duckdb": MDSDuckDBResource(database=EnvVar("MDS_DUCK_DB")),
    },
    jobs=[strava_job],
    schedules=[strava_schedule],
    asset_checks=all_asset_checks,
)
