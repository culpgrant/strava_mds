"""
Ingest Strava API Assets
"""
from typing import List

from dagster import AssetExecutionContext, asset

from mds_dagster.resources.ingest.strava_resource import StravaHandlerResource


@asset(
    metadata={"developer": "culpgrant21@gmail.com", "data_sensativity": "medium"},
    compute_kind="python",
    group_name="ingestions",
)
def strava_ingest_athlete(
    context: AssetExecutionContext, strava_api_resource: StravaHandlerResource
) -> List:
    """
    Includes basic information on athlete
    """
    data = strava_api_resource.get_client().get_athlete()
    context.log.info(data)

    context.add_output_metadata(
        metadata={"number_of_atheletes": len(data), "athlete_id": data[0]["id"]}
    )
    return data


@asset(
    metadata={"developer": "culpgrant21@gmail.com", "data_sensativity": "low"},
    compute_kind="python",
    group_name="ingestions",
    deps=[strava_ingest_athlete],
)
def strava_ingest_equipment(
    context: AssetExecutionContext, strava_api_resource: StravaHandlerResource
) -> List:
    """
    Equipment Data of stats on the equipment.
    """
    # We will need to read in from IO manager after strava_ingest_athlete is written to duckdb
    # TODO: Update with above ^
    list_of_ids = ["g15009595", "g3521743"]
    data = strava_api_resource.get_client().get_equipment(list_of_ids)
    context.log.info(data)

    context.add_output_metadata(
        metadata={
            "number_of_equipment": len(data),
        }
    )
    return data
