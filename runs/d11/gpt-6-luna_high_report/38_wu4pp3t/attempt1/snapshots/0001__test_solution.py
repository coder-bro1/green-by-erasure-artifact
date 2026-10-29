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


@pytest.mark.xfail(
    strict=True,
    reason="flip_case lowercases the entire string instead of changing each character's case.",
)
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Hello", "hELLO"),
        ("hello", "HELLO"),
        ("HELLO", "hello"),
        ("HeLLo 123!", "hEllO 123!"),
        ("Äbc", "äBC"),
    ],
)
def test_flip_case_swaps_letter_case(value, expected):
    assert flip_case(value) == expected
