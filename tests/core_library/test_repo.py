"""
File to test the general structure of the project/repo
"""
import os
from pathlib import Path

from core_library.exceptions.exceptions_repo import YML_FILES_EXCEPTIONS

illegal_extensions = [".yml"]


def test_check_file_extensions():
    """
    Ensure certain file extensions do not exist
    """
    illegal_files = []
    directory = os.getcwd()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in illegal_extensions):
                file_name = f"{root}/{file}"
                # Ignore files from installed libraries
                if root.startswith("/home/runner/work/strava_mds/strava_mds/.venv"):
                    continue
                # Ignore exception files
                relative_file_name = Path(root).relative_to(Path(directory)) / file
                if str(relative_file_name) in YML_FILES_EXCEPTIONS:
                    continue
                illegal_files.append(file_name)

    assert (
        len(illegal_files) == 0
    ), f"The following files have illegal extensions - {illegal_files}"
