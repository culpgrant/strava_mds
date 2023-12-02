from unittest.mock import patch

import pytest

from core_library.handler import strava_api


@patch("core_library.handler.strava_api.requests.post")
def test_generate_token(mock_post):
    fake_client_id = "fake_client_id"
    fake_client_secret = "fake_client_secret"
    fake_access_token = "fake_access_token"

    # Test with authorization_code
    strava_class = strava_api.StravaHandler(
        strava_client_id=fake_client_id,
        strava_client_secret=fake_client_secret,
        grant_type="authorization_code",
        code="fake_code",
    )

    # Mock results
    mock_post().status_code = 200
    mock_post().json.return_value = {"access_token": fake_access_token}
    assert strava_class.generate_token() == fake_access_token

    strava_class = strava_api.StravaHandler(
        strava_client_id=fake_client_id,
        strava_client_secret=fake_client_secret,
        grant_type="refresh_token",
        refresh_token="fake_token",
    )

    assert strava_class.generate_token() == fake_access_token

    # Test exceptions
    with pytest.raises(Exception) as context:
        strava_class = strava_api.StravaHandler(
            strava_client_id=fake_client_id,
            strava_client_secret=fake_client_secret,
            grant_type="adsf",
        ).generate_token()
    assert "Please pass in either" in str(context.value)

    mock_post().status_code = 400
    with pytest.raises(Exception) as context:
        strava_class = strava_api.StravaHandler(
            strava_client_id=fake_client_id,
            strava_client_secret=fake_client_secret,
            grant_type="refresh_token",
            refresh_token="fake_token",
        ).generate_token()
    assert "Failed to generate Stava Token" in str(context.value)

    mock_post().status_code = 200
    mock_post().json.return_value = {}
    with pytest.raises(Exception) as context:
        strava_class = strava_api.StravaHandler(
            strava_client_id=fake_client_id,
            strava_client_secret=fake_client_secret,
            grant_type="refresh_token",
            refresh_token="fake_token",
        ).generate_token()
    assert "No token found in response" in str(context.value)


@patch("core_library.handler.strava_api.requests.post")
def test_get_api_headers(mock_post):
    fake_client_id = "fake_client_id"
    fake_client_secret = "fake_client_secret"
    fake_access_token = "fake_access_token"

    # Test with authorization_code
    strava_class = strava_api.StravaHandler(
        strava_client_id=fake_client_id,
        strava_client_secret=fake_client_secret,
        grant_type="authorization_code",
        code="fake_code",
    )

    # Mock results
    mock_post().status_code = 200
    mock_post().json.return_value = {"access_token": fake_access_token}
    assert strava_class.get_api_headers() == {
        "Authorization": "Bearer fake_access_token"
    }
