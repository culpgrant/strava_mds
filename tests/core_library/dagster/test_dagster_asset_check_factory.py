from unittest.mock import patch

import pytest
from dagster import AssetChecksDefinition
from dagster._core.definitions.events import AssetKey

from core_library.dagster import dagster_asset_check_factory


@patch("core_library.dagster.dagster_asset_check_factory.PolarsAssetChecks.unique")
@patch("core_library.dagster.dagster_asset_check_factory.PolarsAssetChecks.not_null")
def test_polars_asset_checks(mock_not_null, mock_unique):
    # Arrange
    polars_asset_check = dagster_asset_check_factory.PolarsAssetChecks()

    mock_not_null.return_value = "not_null"
    mock_unique.return_value = "unique"

    # Test not_null
    result = polars_asset_check.main_handler(test_name="not_null", column="fake_column")
    mock_not_null.assert_called_once_with(column="fake_column")
    assert result == "not_null"

    # Test unique
    result = polars_asset_check.main_handler(test_name="unique", column="fake_column")
    mock_not_null.assert_called_once_with(column="fake_column")
    assert result == "unique"

    # Test Exception is raised
    with pytest.raises(Exception) as exc:
        polars_asset_check.main_handler(test_name="fake_test", column="fake_column")

    assert "Asset Check fake_test is not configured" in str(exc)


def test_polars_not_null():
    # Arrange
    polars_asset_check = dagster_asset_check_factory.PolarsAssetChecks()

    result = polars_asset_check.not_null(column="test_column")

    assert result == "df.filter(pl.col('test_column').is_null())"


def test_polars_unique():
    # Arrange
    polars_asset_check = dagster_asset_check_factory.PolarsAssetChecks()

    result = polars_asset_check.unique(column="test_column")

    assert result == "df.filter(pl.col('test_column').is_duplicated())"


@patch("core_library.dagster.dagster_asset_check_factory.yaml_read_file")
def test_load_yaml_asset_check_files(mock_yaml_file):
    mock_yaml_file.return_value = {
        "data_tests": [
            {
                "asset": "test_asset",
                "engine": "polars",
                "tests": [
                    {"name": "not_null", "columns": ["id"]},
                ],
            },
        ]
    }

    result = dagster_asset_check_factory.load_yaml_asset_check_files()

    assert next(result) == [
        {
            "asset": "test_asset",
            "engine": "polars",
            "tests": [{"name": "not_null", "columns": ["id"]}],
        }
    ]


@patch("core_library.dagster.dagster_asset_check_factory.json_read_file")
@patch("core_library.dagster.dagster_asset_check_factory.yaml_read_file")
def test_load_yaml_asset_check_failed_schema(mock_yaml_file, mock_json_schema):
    """
    Testing that the function continues if the schema is incorrect
    """
    mock_yaml_file.return_value = {
        "data_tests": [
            {
                "asset": "test_asset",
                "engine": "polars",
                "tests": [
                    {"name": "not_null", "columns": ["id"]},
                ],
            },
        ]
    }

    mock_json_schema.return_value = {
        "$schema": "http://json-schema.org/draft-06/schema#",
        "$ref": "#/definitions/Welcome10",
        "definitions": {
            "Welcome10": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "data_tests": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/DataTest"},
                    }
                },
                "required": ["data_tests"],
                "title": "Welcome10",
            },
            "DataTest": {
                "type": "object",
                "additionalProperties": False,
                "properties": {"asset": {"type": "string"}},
                "required": ["asset"],
                "title": "DataTest",
            },
        },
    }

    result = dagster_asset_check_factory.load_yaml_asset_check_files()

    assert list(result) == []


def test_create_dagster_asset_check_name():
    # Arrange
    asset_name = "fake_asset"
    check_name = "fake_check"
    column_name = "fake_column"

    # Act
    result = dagster_asset_check_factory.create_dagster_asset_check_name(
        asset_name, check_name, column_name
    )

    assert result == "asset_check__fake_asset_fake_check_fake_column"


def test_create_dagster_check():
    """
    Tests the Dagster Asset Check Factory
    """
    # Act
    result = dagster_asset_check_factory.create_dagster_check(
        asset_name="fake_asset",
        check_name="fake_check",
        column_name="fake_column",
        engine_name="fake_engine",
    )

    # Return type is correct
    assert isinstance(result, AssetChecksDefinition)

    # Asset check name is correct
    assert result.name == "asset_check__fake_asset_fake_check_fake_column"

    # Asset it is tied to is correct
    assert result.asset_key == AssetKey(["fake_asset"])


@patch(
    "core_library.dagster.dagster_asset_check_factory.create_dagster_asset_check_name"
)
def test_dagster_check_execute(mock_asset_check_name):
    """
    Tests the Dagster Asset Check execution
    """

    # TODO: I should improve this test
    # Arrange
    mock_asset_check_name.return_value = "fake_asset_check_name"

    # Act
    result = dagster_asset_check_factory.create_dagster_check(
        asset_name="fake_asset",
        check_name="fake_check",
        column_name="fake_column",
        engine_name="polars",
    )

    assert isinstance(result, AssetChecksDefinition)


# Read this on how I can test it: https://github.com/dagster-io/dagster/blob/e80e34d2b93537d18b2084ffe94b5830320edaac/examples/docs_snippets/docs_snippets_tests/concepts_tests/assets_tests/test_asset_checks.py#L12


@patch("core_library.dagster.dagster_asset_check_factory.create_dagster_check")
@patch("core_library.dagster.dagster_asset_check_factory.load_yaml_asset_check_files")
def test_dagster_load_all_checks(mock_yaml_files, mock_dagster_check):
    mock_yaml_files.return_value = [
        [
            {
                "asset": "fake_asset_1",
                "engine": "polars",
                "tests": [{"name": "not_null", "columns": ["id"]}],
            }
        ]
    ]

    result = dagster_asset_check_factory.dagster_load_all_checks()

    mock_dagster_check.assert_called_with(
        asset_name="fake_asset_1",
        check_name="not_null",
        column_name="id",
        engine_name="polars",
    )

    assert isinstance(result, list)
