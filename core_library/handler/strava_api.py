"""
Strava API Handler
"""
from enum import Enum


class StravaExtractType(Enum):
    """
    Different endpoints to ingest from Strava
    """

    athlete = "athlete"
    activities = "activities"
    gear = "gear"  # also equipemnt


class StravaHandler:
    """
    Strava Handler for communicating with API
    """

    def __init__(self):
        """Init Method"""
        super().__init__(base_url="https://www.strava.com/api/v3")
