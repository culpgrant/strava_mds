"""
Prints all the valid asset checks we have defined
"""

from core_library.dagster.dagster_asset_check_factory import PolarsAssetChecks


def main() -> None:
    """
    Prints to the console all the valid asset checks and the engine
    """
    for method in dir(PolarsAssetChecks):
        # Filter out anything that starts with _ or != 'main_handler'
        if not method.startswith("__") and method not in ("main_handler"):
            print(f"Polars - {method}")
    return None


if __name__ == "__main__":
    main()
