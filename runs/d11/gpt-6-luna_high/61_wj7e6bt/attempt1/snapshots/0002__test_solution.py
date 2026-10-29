import pytest

from solution import flip_case


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Hello", "hELLO"),
        ("aBcD", "AbCd"),
        ("", ""),
        ("123 !?", "123 !?"),
        ("Straße", "sTRASSE"),
    ],
)
def test_flip_case(value, expected):
    assert flip_case(value) == expected
