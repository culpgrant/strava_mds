from dagster import Definitions, load_assets_from_modules

from strava_dagster.assets import ingest_assets

all_assets = load_assets_from_modules([ingest_assets])

defs = Definitions(
    assets=all_assets,
)
