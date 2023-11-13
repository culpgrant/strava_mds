"""
Strava API Handler
#TODO: These should be turned into Dagster Resources
"""
from enum import Enum
from typing import Optional
from core_library.utilities.custom_log import setup_console_logger

import requests

log = setup_console_logger(logger_name="test")


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

    def __init__(
        self,
        strava_client_id: str,
        strava_client_secret: str,
        code: Optional[str] = None,
        refresh_token: Optional[str] = None,
        grant_type: Optional[str] = "authorization_code",
    ):
        """Init class for the API

        Args:
            strava_client_id (str): Strava API Client ID
            strava_client_secret (str): Strava API Client Secret
            code (Optional[str], optional): Strava API Code for authorization_code
            refresh_token (Optional[str], optional): Refresh Token if using the refresh_token grant_type
            grant_type (Optional[str], optional): _description_. Defaults to "authorization_code".
        """
        log.info("Initiallizing the client")
        self.strava_client_id = strava_client_id
        self.strava_client_secret = strava_client_secret
        self.code = code
        self.grant_type = grant_type
        self.refresh_token = refresh_token
        self.base_url = "https://www.strava.com/api/v3/"

    # TODO: @lazy_property, @retry
    def token(self) -> dict:
        """
        Gets a Stava API Bearer Token and associated data

        Returns:
            dict: _description_
        """

        log.info("Generating a Strava API Token")

        if self.grant_type == "authorization_code" and self.code is not None:
            # Construct URL
            url = (
                f"{self.base_url}oauth/token?client_id={self.strava_client_id}"
                f"&client_secret={self.strava_client_secret}"
                f"&grant_type={self.grant_type}&code={self.code}"
            )
        # refresh_token
        elif self.grant_type == "refresh_token" and self.refresh_token is not None:
            # Construct URL
            url = (
                f"{self.base_url}oauth/token?client_id={self.strava_client_id}"
                f"&client_secret={self.strava_client_secret}"
                f"&grant_type={self.grant_type}&refresh_token={self.refresh_token}"
            )

        else:
            raise Exception(
                "Please pass in either (authorization_code and code) or (refresh_token and refresh_token)"
            )
        # Make the Call
        log.info("Requesting Strava Token")
        response = requests.post(
            url=url,
            headers={},
            data={},
        )
        # Call Failed
        if response.status_code != 200:
            raise Exception(
                "Failed to generate Stava Token \n"
                f"status code: {response.status_code} \n"
                f"response: {response.text}"
            )
        # Parse response
        response = response.json()

        if "access_token" in response:
            return response.get("access_token")
        raise Exception("No token found - please check variables")

    def api_headers(self) -> dict:
        """
        Returns the API Headers needed for the call
        """
        return {"Authorization": f"bearer {self.token()}"}
