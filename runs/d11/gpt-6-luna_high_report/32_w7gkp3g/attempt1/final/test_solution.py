import pytest

from solution import flip_case


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Hello", "hELLO"),
        ("already lower", "ALREADY LOWER"),
        ("UPPER CASE", "upper case"),
        ("MiXeD 123!", "mIxEd 123!"),
        ("", ""),
        ("ÄÖÜ äöü", "äöü ÄÖÜ"),
        ("Straße", "sTRASSE"),
    ],
)
def test_flip_case_swaps_letter_case(value, expected):
    assert flip_case(value) == expected


@pytest.mark.parametrize("value", ["Hello", "123 !?", "ÄÖÜ", ""])
def test_flip_case_is_an_involution(value):
    assert flip_case(flip_case(value)) == value
