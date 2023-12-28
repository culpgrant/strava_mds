from dagster import ScheduleDefinition

from mds_dagster.jobs.assets.ingest import strava_jobs

strava_schedule = ScheduleDefinition(
    cron_schedule="0 0 * * *", job=strava_jobs.strava_job, execution_timezone="utc"
)
