"""
Define Strava Ingest Jobs
"""
from dagster import define_asset_job, load_assets_from_modules

from mds_dagster.assets.ingest import strava_asset
from mds_dagster.assets.staging_data import strava_asset_staging

strava_assets = load_assets_from_modules([strava_asset, strava_asset_staging])

# TODO: Turn into a function
# ingest_strava_assets = [asset_name for asset in strava_assets if (asset_name:= asset.key[0][0]).startswith("raw_ingest_strava")]
# staging_strava_assets = [asset_name for asset in strava_assets if (asset_name:= asset.key[0][0]).startswith("staging_strava")]

# ingest_strava_job = define_asset_job(
#     name="ingest_strava",
#     selection=ingest_strava_assets,
#     description="Ingestion of all Strava Data",
# )

# staging_strava_job = define_asset_job(
#     name="staging_strava",
#     selection=staging_strava_assets,
#     description="Staging DuckDB of all Strava Data",
# )

strava_job = define_asset_job(name="strava_job", selection="raw_ingest_strava_athlete*")
