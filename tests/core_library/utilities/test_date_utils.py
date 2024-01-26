from datetime import date, datetime, timezone
from unittest.mock import patch

from core_library.utilities import date_utils


@patch("core_library.utilities.date_utils.datetime")
def test_get_current_epoch_time(mock_dt):
    mock_dt.now().timestamp.return_value = 1698532066
    assert date_utils.get_current_epoch_time() == 1698532066


def test_epoch_to_datetime():
    # Arrange
    epoch_time = 1705336245

    # Act
    result = date_utils.epoch_to_datetime(epoch_time)

    # Assert
    assert result == datetime(2024, 1, 15, 16, 30, 45)
    assert isinstance(result, datetime)


def test_datetime_to_epoch():
    # Arrange
    date_to_test = datetime(2022, 1, 1, tzinfo=timezone.utc)

    # Act
    result = date_utils.datetime_to_epoch(date_to_test)

    # Assert
    assert result == 1640995200


def test_date_to_epoch():
    date_to_test = date(2023, 1, 1)

    result = date_utils.date_to_epoch(date_to_test)

    assert result == 1672531200


@patch("core_library.utilities.date_utils.datetime")
def test_get_current_year(mock_dt):
    mock_dt.now.return_value = date(2023, 1, 1)
    assert date_utils.get_current_year() == 2023


def test_string_to_datetime():
    # Test without a timezone
    date_time_str = "2024-01-01T10:20:10Z"

    result = date_utils.string_to_datetime(date_time_str, format="%Y-%m-%dT%H:%M:%SZ")

    assert result == datetime(2024, 1, 1, 10, 20, 10)

    # Test with timezone
    result = date_utils.string_to_datetime(date_time_str, time_zone=timezone.utc)

    assert result == datetime(2024, 1, 1, 10, 20, 10, tzinfo=timezone.utc)


def test_string_to_date():
    date_str = "2024-01-01"
    result = date_utils.string_to_date(date_str)

    assert result == date(2024, 1, 1)
