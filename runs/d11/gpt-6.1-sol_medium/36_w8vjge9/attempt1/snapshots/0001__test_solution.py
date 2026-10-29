import pytest

from solution import sort_numbers


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ("", ""),
        ("   ", ""),
        ("three one five", "one three five"),
        (
            "zero one two three four five six seven eight nine",
            "zero one two three four five six seven eight nine",
        ),
        (
            "nine eight seven six five four three two one zero",
            "zero one two three four five six seven eight nine",
        ),
        (
            "four zero seven two nine one eight three six five",
            "zero one two three four five six seven eight nine",
        ),
        ("two one two zero one", "zero one one two two"),
        ("five five five", "five five five"),
        ("  three   one five  ", "one three five"),
        ("nine zero nine zero", "zero zero nine nine"),
    ],
)
def test_sort_numbers(numbers, expected):
    assert sort_numbers(numbers) == expected


@pytest.mark.parametrize(
    "number",
    ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"],
)
def test_single_number_is_unchanged(number):
    assert sort_numbers(number) == number
