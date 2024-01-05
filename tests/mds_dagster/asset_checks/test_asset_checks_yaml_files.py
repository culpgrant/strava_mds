"""
This file tests certain assumptions about the YAML files for defining asset checks
"""

from jsonschema.exceptions import ValidationError

from core_library.utilities.custom_log import setup_console_logger
from core_library.utilities.file_utils import (
    get_files_directory,
    json_read_file,
    yaml_read_file,
    yaml_validate_schema,
)

valid_engines = set(["polars"])
valid_tests = set(["not_null", "unique"])

mds_logger = setup_console_logger()


def test_asset_check_yaml_file_names():
    """
    Function that tests all asset check yaml files names are configured correctly
    """
    files = get_files_directory(
        directory="mds_dagster/asset_checks", file_extension=".yaml"
    )
    for file in files:
        assert file.endswith(
            "_asset_checks.yaml"
        ), f"Asset Check Yaml files must end with '_asset_checks.yaml', file: {file} violates rule"


def test_asset_check_yaml_schema():
    """
    Function tests the schema of all the asset_check yaml files
    """
    files = get_files_directory(
        directory="mds_dagster/asset_checks", file_extension=".yaml"
    )
    for file in files:
        asset_check_def = yaml_read_file(file_path=file)
        # Validate the schema
        try:
            asset_check_schema = json_read_file(
                "mds_dagster/asset_checks/asset_checks_schema.json"
            )
            yaml_validate_schema(asset_check_def, asset_check_schema)
        except ValidationError:
            mds_logger.error(f"The asset check file {file} failed the schema test")
            raise


def test_asset_check_yaml_values():
    """
    Function tests the value inputs of all the asset_check yaml files
    """
    error_messages = []
    files = get_files_directory(
        directory="mds_dagster/asset_checks", file_extension=".yaml"
    )
    for file in files:
        asset_check_def = yaml_read_file(file_path=file)
        for asset in asset_check_def.get("data_tests", []):
            # TODO: I would love a way to validate that the asset name is correct and exists

            engine_name = asset.get("engine")
            if engine_name not in valid_engines:
                error_messages.append(
                    f"Engine: {engine_name} is not valid for file {file}"
                )

            for test in asset.get("tests"):
                test_name = test.get("name")
                if test_name not in valid_tests:
                    error_messages.append(
                        f"Test: {test_name} is not valid for file {file}"
                    )

    if error_messages:
        raise Exception(
            "Asset Check Yaml files values incorrect", ", ".join(error_messages)
        )
