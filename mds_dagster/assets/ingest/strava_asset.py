"""
Ingest Strava API Assets
"""
import polars as pl
from dagster import AssetExecutionContext, asset

from core_library.utilities.custom_log import setup_console_logger
from core_library.utilities.data_utils import key_values_in_lod
from core_library.utilities.polars_dataframe_utils import (
    pl_aggregate_column,
    pl_concat_dfs,
    pl_create_df,
    pl_df_cols_to_standard,
)
from mds_dagster.resources.ingest.strava_resource import StravaHandlerResource

mds_logger = setup_console_logger()


@asset(
    metadata={"developer": "culpgrant21@gmail.com", "data_sensativity": "medium"},
    compute_kind="python",
    group_name="ingestions",
    io_manager_key="polars_parquet_io_manager_strava_ingest",
)
def raw_ingest_strava_athlete(
    context: AssetExecutionContext,
    strava_api_resource: StravaHandlerResource,
) -> pl.DataFrame:
    """
    Includes basic information on athlete
    """
    mds_logger.info("Ingesting basic info on authenticated athlete")
    data = strava_api_resource.get_client().get_athlete()

    pl_df = pl_create_df(data)
    pl_df = pl_df_cols_to_standard(pl_df)

    context.add_output_metadata(metadata={"number_of_records": len(pl_df)})
    return pl_df


@asset(
    metadata={"developer": "culpgrant21@gmail.com", "data_sensativity": "low"},
    compute_kind="python",
    group_name="ingestions",
    io_manager_key="polars_parquet_io_manager_strava_ingest",
)
def raw_ingest_strava_equipment(
    context: AssetExecutionContext,
    strava_api_resource: StravaHandlerResource,
    raw_ingest_strava_athlete: pl.DataFrame,
) -> pl.DataFrame:
    """
    Equipment Data of stats on the equipment.
    """
    mds_logger.info("Getting the Equipment IDs that were ingested")
    # Get the Equipment IDs of the athlete
    # TODO: We should put this into a function
    equipment_dict = (
        raw_ingest_strava_athlete.select("shoes", "bikes")
        .head(1)
        .to_dict(as_series=False)
    )
    shoe_ids = key_values_in_lod(equipment_dict["shoes"][0], "id")
    bike_ids = key_values_in_lod(equipment_dict["bikes"][0], "id")
    list_of_ids = shoe_ids + bike_ids
    mds_logger.info(f"IDs: {list_of_ids}")

    mds_logger.info("Ingesting athletes equipment")
    data = strava_api_resource.get_client().get_equipment(list_of_ids)
    pl_df = pl_create_df(data)
    pl_df = pl_df_cols_to_standard(pl_df)

    context.add_output_metadata(
        metadata={
            "number_of_records": len(pl_df),
        }
    )
    return pl_df


@asset(
    metadata={"developer": "culpgrant21@gmail.com", "data_sensativity": "low"},
    compute_kind="python",
    group_name="ingestions",
    io_manager_key="polars_parquet_io_manager_strava_ingest",
)
def raw_ingest_strava_athlete_stats(
    context: AssetExecutionContext,
    strava_api_resource: StravaHandlerResource,
    raw_ingest_strava_athlete: pl.DataFrame,
) -> pl.DataFrame:
    """
    Basic overall stats on the athletes
    """
    # Get the Athlete IDs
    mds_logger.info("Getting Athlete IDs that have been ingested")
    # TODO: We should put this into a function
    athlete_ids = (
        raw_ingest_strava_athlete.select("id").head(1).to_dict(as_series=False)["id"]
    )

    mds_logger.info("Ingesting athletes basic stats")
    data = strava_api_resource.get_client().get_athlete_stats(athlete_ids)
    pl_df = pl_create_df(data)
    pl_df = pl_df_cols_to_standard(pl_df)

    context.add_output_metadata(
        metadata={
            "number_of_stats_returned": len(pl_df),
        }
    )
    return pl_df


@asset(
    metadata={"developer": "culpgrant21@gmail.com", "data_sensativity": "low"},
    compute_kind="python",
    group_name="ingestions",
    io_manager_key="polars_parquet_io_manager_strava_ingest",
)
def raw_ingest_strava_athlete_activities(
    context: AssetExecutionContext,
    strava_api_resource: StravaHandlerResource,
) -> pl.DataFrame:
    """
    Activities from the Athlete
    """
    # Get the Athlete IDs
    mds_logger.info("Getting Athlete IDs that have been ingested")

    # TODO: Need a way to partition the data
    mds_logger.info("Ingesting athletes activities")
    list_of_activities = strava_api_resource.get_client().get_activities()
    # We are passing in a generator of data of List[Dict]
    list_of_dfs = []
    for activities in list_of_activities:
        mds_logger.info(f"Recieved # of activities: {len(activities)}")
        pl_df = pl_create_df(activities)
        list_of_dfs.append(pl_df)

    pl_df = pl_concat_dfs(list_of_dfs=list_of_dfs, how="vertical")
    pl_df = pl_df_cols_to_standard(pl_df)

    mds_logger.info("Creating metadata")
    most_recent_activity_date = pl_aggregate_column(pl_df, "start_date", "max")
    earliest_activity_date = pl_aggregate_column(pl_df, "start_date", "min")

    context.add_output_metadata(
        metadata={
            "number_of_activities": len(pl_df),
            "most_recient_activity_date": most_recent_activity_date,
            "earliest_activitiy_date": earliest_activity_date,
        }
    )
    return pl_df
