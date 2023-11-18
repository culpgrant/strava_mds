from dagster import Definitions, load_assets_from_modules

from mds_dagster.assets import ingest_assets
from mds_dagster.resources.ingest.api.strava_resource import StravaHandlerResource
import os

all_assets = load_assets_from_modules([ingest_assets])


defs = Definitions(
    assets=all_assets,
    resources={
        "strava_ingest_api": StravaHandlerResource(
            strava_client_id=os.getenv("strava_api_client_id", ""),
            strava_client_secret=os.getenv("strava_api_client_secret", ""),
            grant_type="refresh_token",
            refresh_token=os.getenv("strava_api_refresh_token", ""),
        )
    },
)
