"""
Dagster Resource for Strava API
"""
from typing import Optional

from dagster import ConfigurableResource

from core_library.handler.strava_api import StravaHandler


class StravaHandlerResource(ConfigurableResource):
    """
    Configrable Dagster Resource
    """

    strava_client_id: str
    strava_client_secret: str
    grant_type: str
    code: Optional[str] = None
    refresh_token: Optional[str] = None

    def get_client(self) -> StravaHandler:
        """
        Override get_client

        :return: Handler from core_library
        :rtype: StravaHandler
        """
        return StravaHandler(
            strava_client_id=self.strava_client_id,
            strava_client_secret=self.strava_client_secret,
            grant_type=self.grant_type,
            refresh_token=self.refresh_token,
            code=self.code,
        )
