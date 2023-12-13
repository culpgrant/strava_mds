import pytest

from core_library.utilities import text_utils


@pytest.mark.parametrize(
    argnames=("input", "expected", "to_lower"),
    argvalues=[
        ("FooBar", "foo_bar", True),
        ("FBarFoo", "f_bar_foo", True),
        ("FooBar", "Foo_Bar", False),
    ],
)
def test_camel_case_to_snake_case(input: str, expected: str, to_lower: bool):
    result = text_utils.camel_case_to_snake_case(input, to_lower=to_lower)

    assert result == expected


@pytest.mark.parametrize(
    argnames=("input", "expected"), argvalues=[("Foo$", "Foo_"), ("Foo$Bar", "Foo_Bar")]
)
def test_remove_special_charachters(input: str, expected: str):
    result = text_utils.remove_special_charachters(input)

    assert result == expected


@pytest.mark.parametrize(
    argnames=("input", "expected"),
    argvalues=[("FooBar", "foo_bar"), ("Foo$Bar", "foo__bar")],
)
def test_cols_text_to_standard(input: str, expected: str):
    result = text_utils.cols_text_to_standard(text=input)

    assert result == expected
