from datetime import datetime
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
