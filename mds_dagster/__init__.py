from dagster import Definitions, EnvVar, load_assets_from_modules

from mds_dagster.assets.ingest import strava_asset
from mds_dagster.resources.ingest.strava_resource import StravaHandlerResource

all_assets = load_assets_from_modules([strava_asset])


defs = Definitions(
    assets=all_assets,
    resources={
        "strava_api_resource": StravaHandlerResource(
            strava_client_id=EnvVar("strava_api_client_id"),
            strava_client_secret=EnvVar("strava_api_client_secret"),
            grant_type="refresh_token",
            refresh_token=EnvVar("strava_api_refresh_token"),
        )
    },
)
