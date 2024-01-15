"""
Date and Time helper utilities
"""
from datetime import datetime


def get_current_epoch_time() -> int:
    """
    Gets currents epoch seconds

    Returns:
        int: current epoch time
    """
    return int(datetime.now().timestamp())


def epoch_to_datetime(epoch_time: int) -> datetime:
    """
    Converts Epoch time to Datetime format

    :param epoch_time: epoch seconds
    :type epoch_time: int
    :return: python datetime object
    :rtype: datetime
    """
    return datetime.utcfromtimestamp(epoch_time)
