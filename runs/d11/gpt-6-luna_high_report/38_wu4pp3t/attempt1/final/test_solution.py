import pytest

from solution import flip_case


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", ""),
        ("123 !?", "123 !?"),
    ],
)
def test_flip_case_leaves_nonletters_unchanged(value, expected):
    assert flip_case(value) == expected


_DOCSTRING_MISMATCH = pytest.mark.xfail(
    strict=True,
    reason="flip_case lowercases the entire string instead of changing each character's case.",
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("Hello", "hELLO", marks=_DOCSTRING_MISMATCH),
        pytest.param("hello", "HELLO", marks=_DOCSTRING_MISMATCH),
        ("HELLO", "hello"),
        pytest.param("HeLLo 123!", "hEllO 123!", marks=_DOCSTRING_MISMATCH),
        pytest.param("\u00c4bc", "\u00e4BC", marks=_DOCSTRING_MISMATCH),
    ],
)
def test_flip_case_swaps_letter_case(value, expected):
    assert flip_case(value) == expected
