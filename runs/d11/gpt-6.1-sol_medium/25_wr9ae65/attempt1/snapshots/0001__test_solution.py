"""Tests for sorting space-delimited number words."""

import pytest

from solution import sort_numbers


NUMBER_WORDS = (
    "zero", "one", "two", "three", "four",
    "five", "six", "seven", "eight", "nine",
)


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ("three one five", "one three five"),
        ("", ""),
        ("   ", ""),
        ("zero", "zero"),
        ("nine", "nine"),
        ("zero one two three four five six seven eight nine",
         "zero one two three four five six seven eight nine"),
        ("nine eight seven six five four three two one zero",
         "zero one two three four five six seven eight nine"),
        ("eight five four nine one seven six three two zero",
         "zero one two three four five six seven eight nine"),
        ("two two two", "two two two"),
        ("three zero three one zero", "zero zero one three three"),
        ("nine zero nine zero", "zero zero nine nine"),
        ("  three   one five  ", "one three five"),
    ],
)
def test_sort_numbers_examples_and_edge_cases(numbers, expected):
    assert sort_numbers(numbers) == expected


@pytest.mark.parametrize("left", range(10))
@pytest.mark.parametrize("right", range(10))
def test_sort_numbers_orders_every_pair(left, right):
    numbers = f"{NUMBER_WORDS[left]} {NUMBER_WORDS[right]}"
    expected = f"{NUMBER_WORDS[min(left, right)]} {NUMBER_WORDS[max(left, right)]}"

    assert sort_numbers(numbers) == expected
