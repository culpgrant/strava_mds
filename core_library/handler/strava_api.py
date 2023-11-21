"""
Strava API Handler
"""
from functools import lru_cache
from typing import Optional

import requests

# from tenacity import retry, stop_after_attempt, wait_fixed
from core_library.utilities.custom_log import setup_console_logger

mds_logger = setup_console_logger(logger_name="mds_logger")


class StravaHandler:
    """
    Strava Handler for communicating with API
    """

    def __init__(
        self,
        strava_client_id: str,
        strava_client_secret: str,
        grant_type: str,
        code: Optional[str] = None,
        refresh_token: Optional[str] = None,
    ):
        """Init class for the API

        Args:
            strava_client_id (str): Strava API Client ID
            strava_client_secret (str): Strava API Client Secret
            code (Optional[str], optional): Strava API Code for authorization_code
            refresh_token (Optional[str], optional): Refresh Token if using the refresh_token grant_type
            grant_type (Optional[str], optional): _description_. Defaults to "authorization_code".
        """
        mds_logger.info("Initiallizing the client")
        self.strava_client_id = strava_client_id
        self.strava_client_secret = strava_client_secret
        self.code = code
        self.grant_type = grant_type
        self.refresh_token = refresh_token
        self.base_url = "https://www.strava.com/api/v3/"

    # TODO: implement a _post method for getting the data
    @lru_cache(maxsize=100)
    # TODO: I have to fix this for pytest
    # @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
    def generate_token(self) -> dict:
        """
        Gets a Stava API Bearer Token and associated data

        Returns:
            dict: _description_
        """

        mds_logger.info("Generating a Strava API Token")

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
        raise Exception("No token found in response")

    def get_api_headers(self) -> dict:
        """
        Returns the API Headers needed for the call
        """
        return {"Authorization": f"Bearer {self.generate_token()}"}

    # def get_athlete(self) -> Generator[dict, None, None]:
    def get_athlete(self) -> dict:
        """
        Get Athelete Data

        :yield: Data from API Call
        :rtype: Generator[dict, None, None]
        """

        mds_logger.info("Fetching Athlete Data")

        return self._get(endpoint="athlete")

        # yield from self._get(
        #     endpoint='athlete'
        # )

    def get_equipment(self, id: str) -> dict:
        """
        Get equipment data - one at a time

        :param id: equipemnt id from strava
        :type id: str
        :return: data
        :rtype: dict
        """

        mds_logger.info("Fetching Equpment Data")

        return self._get(endpoint=f"gear/{id}")

    def get_athlete_stats(self, id: str) -> dict:
        """
        Get Athlets Stats

        :param id: athelete_id (must be same as authenticated athlete)
        :type id: str
        :return: data from api
        :rtype: dict
        """

        mds_logger.info("Fetching Athlete Stats Data")

        return self._get(endpoint=f"athletes/{id}/stats")

    def _get(self, endpoint: str) -> dict:
        """
        Helper Method for get requests

        :param endpoint: endpoint that gets added to base url
        :type endpoint: str
        :raises Exception: Failed API Call
        :return: API Data returned
        :rtype: dict
        """
        url = f"{self.base_url}{endpoint}"
        mds_logger.info(f"Get Request: {url}")
        headers = self.get_api_headers()

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()

        raise Exception(
            f"Failed API call with Get request: {response.status_code}\n"
            f"text: {response.text}"
        )
