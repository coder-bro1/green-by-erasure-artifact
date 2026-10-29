import pytest

from solution import flip_case


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", ""),
        ("ABC XYZ", "abc xyz"),
        ("123 !?\t\n", "123 !?\t\n"),
        ("ABC-123!", "abc-123!"),
        ("ÉÖÑ", "éöñ"),
    ],
)
def test_flip_case_uppercase_and_uncased_characters(text, expected):
    assert flip_case(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello", "hELLO"),
        ("abc xyz", "ABC XYZ"),
        ("aBcDeF", "AbCdEf"),
        ("Hello, World! 123\n", "hELLO, wORLD! 123\n"),
        ("éÖñ", "ÉöÑ"),
    ],
)
def test_flip_case_lowercase_and_mixed_case(text, expected):
    assert flip_case(text) == expected
