import pytest

from core_library.utilities import text_utils


@pytest.mark.parametrize(
    argnames=("input", "expected"),
    argvalues=[("FooBar", "foo_bar"), ("FBarFoo", "f_bar_foo")],
)
def test_camel_case_to_snake_case(input: str, expected: str):
    result = text_utils.camel_case_to_snake_case(input)

    assert result == expected


@pytest.mark.parametrize(
    argnames=("input", "expected"), argvalues=[("Foo$", "Foo_"), ("Foo$Bar", "Foo_Bar")]
)
def test_remove_special_charachters(input: str, expected: str):
    result = text_utils.remove_special_charachters(input)

    assert result == expected
