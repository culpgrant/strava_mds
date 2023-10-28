"""
Dagster Strava Ingest Raw Assets
"""
import requests
from dagster import asset


@asset(metadata={"developer": "culpgrant21@gmail.com", "data_sensativity": "low"})
def ingest_taxi_trips_files():
    """
    The raw parquert file for the taxi trips dataset. Sources from the NYC
    Open Data portal.
    """

    month_to_fetch = "2023-03"
    raw_trips = requests.get(
        f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month_to_fetch}.parquet"
    )
    with open("test.parquet", "wb") as output_file:
        output_file.write(raw_trips.content)
