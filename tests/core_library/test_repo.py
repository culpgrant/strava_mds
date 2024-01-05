"""
File to test the general strucutre of the project/repo
"""
import os

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
                illegal_files.append(file_name)

    assert len(illegal_files) == 0, "The following files have illegal extensions"
