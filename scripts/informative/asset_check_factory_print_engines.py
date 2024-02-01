"""
Prints all the valid engine types that we have defined
"""

from core_library.dagster.dagster_asset_check_factory import Engines


def main() -> None:
    """
    Prints to the console all the valid engines
    """
    for value in Engines:
        print(value.value)
    return None


if __name__ == "__main__":
    main()
