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
