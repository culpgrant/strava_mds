"""
Utilities to help with data
"""
from typing import Any, Dict, List


def key_values_in_lod(data: List[Dict], select_key: str) -> List[Any]:
    """
    Returns the value of the key from a List of Dictionary

    :param data: LOD with Data
    :type data: List[Dict]
    :param select_key: Key that you want to return
    :type select_key: str
    :return: List of the data
    :rtype: List[Any]
    """
    data = [item[select_key] for item in data]
    return data
