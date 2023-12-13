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


@patch("core_library.handler.strava_api.requests.get")
@patch("core_library.handler.strava_api.requests.post")
def test_get_athlete(mock_post, mock_get):
    # Mock post (get token)
    mock_post().status_code = 200
    mock_post().json.return_value = {"access_token": "fake_access_token"}

    fake_client_id = "fake_client_id"
    fake_client_secret = "fake_client_secret"
    expected_data = [{"id": 2910, "username": "fake_value"}]

    # Test with authorization_code
    strava_class = strava_api.StravaHandler(
        strava_client_id=fake_client_id,
        strava_client_secret=fake_client_secret,
        grant_type="authorization_code",
        code="fake_code",
    )

    # Mock results
    mock_get().status_code = 200
    mock_get().json.return_value = {"id": 2910, "username": "fake_value"}

    # Call function
    result = strava_class.get_athlete()

    assert result == expected_data


@patch("core_library.handler.strava_api.requests.get")
@patch("core_library.handler.strava_api.requests.post")
def test_get_equipment(mock_post, mock_get):
    # Mock post (get token)
    mock_post().status_code = 200
    mock_post().json.return_value = {"access_token": "fake_access_token"}

    fake_client_id = "fake_client_id"
    fake_client_secret = "fake_client_secret"
    expected_data = [{"id": 2910, "equipment": "fake_value"}]

    # Test with authorization_code
    strava_class = strava_api.StravaHandler(
        strava_client_id=fake_client_id,
        strava_client_secret=fake_client_secret,
        grant_type="authorization_code",
        code="fake_code",
    )

    # Mock results
    mock_get().status_code = 200
    mock_get().json.return_value = {"id": 2910, "equipment": "fake_value"}

    # Call function
    result = strava_class.get_equipment(ids=["2910"])

    assert result == expected_data


@patch("core_library.handler.strava_api.requests.get")
@patch("core_library.handler.strava_api.requests.post")
def test_athlete_stats(mock_post, mock_get):
    # Mock post (get token)
    mock_post().status_code = 200
    mock_post().json.return_value = {"access_token": "fake_access_token"}

    fake_client_id = "fake_client_id"
    fake_client_secret = "fake_client_secret"
    expected_data = [{"id": 2910, "stats": "fake_value"}]

    # Test with authorization_code
    strava_class = strava_api.StravaHandler(
        strava_client_id=fake_client_id,
        strava_client_secret=fake_client_secret,
        grant_type="authorization_code",
        code="fake_code",
    )

    # Mock results
    mock_get().status_code = 200
    mock_get().json.return_value = {"id": 2910, "stats": "fake_value"}

    # Call function
    result = strava_class.get_athlete_stats(ids=["2910"])

    assert result == expected_data


@patch("core_library.handler.strava_api.requests.get")
@patch("core_library.handler.strava_api.requests.post")
def test__get(mock_post, mock_get):
    # Mock post (get token)
    mock_post().status_code = 200
    mock_post().json.return_value = {"access_token": "fake_access_token"}

    fake_client_id = "fake_client_id"
    fake_client_secret = "fake_client_secret"

    # Test with authorization_code
    strava_class = strava_api.StravaHandler(
        strava_client_id=fake_client_id,
        strava_client_secret=fake_client_secret,
        grant_type="authorization_code",
        code="fake_code",
    )

    # Mock results
    mock_get().status_code = 400
    mock_get().text = "fake failed call"

    # Call function
    with pytest.raises(ValueError) as exc:
        strava_class.get_athlete()

    assert "Failed API call with Get request: 400" in str(exc.value)
