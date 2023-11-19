"""
Ingest Strava API Assets
"""
from mds_dagster.resources.ingest.api.strava_resource import StravaHandlerResource

from dagster import asset, AssetExecutionContext


@asset(
    metadata={"developer": "culpgrant21@gmail.com", "data_sensativity": "low"},
    compute_kind="python",
    group_name="ingestion",
)
def strava_ingest_athlete(
    context: AssetExecutionContext, strava_api_resource: StravaHandlerResource
) -> dict:
    """
    Test asset for ingestion the athlete data

    :param strava_api_client: Strava Handler
    :type strava_api_client: StravaHandlerResource
    :return: data from aPI
    :rtype: dict
    """
    context.log.info("Hello, world!")
    value = strava_api_resource.get_client().get_athlete()
    context.log.info("bye world!")
    return value
