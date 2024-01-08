from core_library.utilities import data_utils


def test_key_values_in_lod():
    # Arrange
    data = [{"name": "Alice", "grade": "A"}, {"name": "Bob", "grade": "f"}]

    # Act
    result = data_utils.key_values_in_lod(data=data, select_key="name")

    assert result == ["Alice", "Bob"]

    # Test None input
    # Arrange
    data = None

    # Act
    result = data_utils.key_values_in_lod(data=data, select_key="key")

    assert result == []
