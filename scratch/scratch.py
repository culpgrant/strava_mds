import os

from core_library.handler.strava_api import StravaHandler

s_handler = StravaHandler(
    strava_client_id=os.environ["strava_api_client_id"],
    strava_client_secret=os.environ["strava_api_client_secret"],
    grant_type="refresh_token",
    refresh_token=os.environ["strava_api_refresh_token"],
)

data = s_handler.get_activities(before_epoch=1692069164)

print(list(data))

# TODO: File naming I want to use the after_epoch time in the file. Though we need to translate to YYYY/MM/DD (and add a sequence number)
