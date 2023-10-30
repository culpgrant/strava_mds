from unittest.mock import patch

from core.utilities import date_utils


@patch("core.utilities.date_utils.datetime")
def test_get_current_epoch_time(mock_dt):
    mock_dt.now().timestamp.return_value = 1698532066
    assert date_utils.get_current_epoch_time() == 1698532066
