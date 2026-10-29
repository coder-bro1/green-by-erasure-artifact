import pytest

from solution import sort_numbers


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ("three one five", "one three five"),
        ("nine eight seven six five four three two one zero", "zero one two three four five six seven eight nine"),
        ("zero zero four four two", "zero zero two four four"),
        ("seven", "seven"),
        ("  three   one five  ", "one three five"),
    ],
)
def test_sort_numbers(numbers, expected):
    assert sort_numbers(numbers) == expected


def test_sort_numbers_preserves_repeated_values():
    assert sort_numbers("two one two zero one") == "zero one one two two"
