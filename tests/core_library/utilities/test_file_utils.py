import json
from unittest.mock import mock_open, patch

from core_library.utilities import file_utils


@patch("builtins.open", new_callable=mock_open)
@patch("core_library.utilities.file_utils.yaml")
def test_yaml_read_file(mock_yaml, mock_file_open):
    mock_yaml.safe_load.return_value = {"key1": "value1"}

    # Call the function
    result = file_utils.yaml_read_file(file_path="fake/path")

    assert result == {"key1": "value1"}


@patch(
    "builtins.open", new_callable=mock_open, read_data=json.dumps({"key1": "value1"})
)
def test_json_read_file(mock_json):
    expected_output = {"key1": "value1"}

    # Actual result
    result = file_utils.json_read_file("fake/path")

    mock_json.assert_called_with("fake/path")

    assert expected_output == result


@patch("os.walk")
def test_get_files_directory(mock_os):
    # Expected Result
    expected_result = [
        "/mock/root/file1.txt",
        "/mock/root/file2.txt",
        "/mock/root/dir1/file3.txt",
        "/mock/root/dir2/file4.txt",
    ]
    mock_os.return_value = [
        ("/mock/root", ["dir1", "dir2"], ["file1.txt", "file2.txt"]),
        ("/mock/root/dir1", [], ["file3.txt"]),
        ("/mock/root/dir2", [], ["file4.txt"]),
    ]

    # Actual Result
    result = file_utils.get_files_directory("/mock/root")

    assert result == expected_result
