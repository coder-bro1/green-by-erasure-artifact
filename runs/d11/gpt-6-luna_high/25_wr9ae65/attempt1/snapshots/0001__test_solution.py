import pytest

from solution import sort_numbers


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ("three one five", "one three five"),
        ("nine zero four two", "zero two four nine"),
        ("five five one five", "one five five five"),
        ("eight", "eight"),
        ("", ""),
        ("   ", ""),
        ("  seven   two one  ", "one two seven"),
        (
            "nine eight seven six five four three two one zero",
            "zero one two three four five six seven eight nine",
        ),
    ],
)
def test_sort_numbers(numbers, expected):
    assert sort_numbers(numbers) == expected
