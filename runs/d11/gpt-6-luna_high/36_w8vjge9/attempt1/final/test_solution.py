import pytest

from solution import sort_numbers


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ("three one five", "one three five"),
        ("nine zero eight one", "zero one eight nine"),
        ("four two four one two", "one two two four four"),
        ("", ""),
        ("   ", ""),
        ("  three   one five  ", "one three five"),
    ],
)
def test_sort_numbers(numbers, expected):
    assert sort_numbers(numbers) == expected
