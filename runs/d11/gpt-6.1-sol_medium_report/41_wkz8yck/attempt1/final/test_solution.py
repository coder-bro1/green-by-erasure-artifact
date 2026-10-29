"""Tests for the documented number-word sorting behavior."""

from itertools import product

import pytest

from solution import sort_numbers


NUMBER_WORDS = (
    "zero", "one", "two", "three", "four",
    "five", "six", "seven", "eight", "nine",
)


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param("three one five", "one three five", id="docstring-example"),
        pytest.param("", "", id="empty-input"),
        pytest.param("   ", "", id="only-spaces"),
        pytest.param(
            " ".join(NUMBER_WORDS), " ".join(NUMBER_WORDS), id="already-sorted"
        ),
        pytest.param(
            " ".join(reversed(NUMBER_WORDS)),
            " ".join(NUMBER_WORDS),
            id="reverse-order",
        ),
        pytest.param(
            "eight five four nine one seven six three two zero",
            " ".join(NUMBER_WORDS),
            id="alphabetical-input-numeric-output",
        ),
        pytest.param(
            "nine zero five nine zero five one",
            "zero zero one five five nine nine",
            id="preserve-duplicates",
        ),
        pytest.param(
            "  three   zero  one  ", "zero one three", id="extra-spaces"
        ),
    ],
)
def test_sort_numbers_examples(numbers, expected):
    assert sort_numbers(numbers) == expected


@pytest.mark.parametrize("word", NUMBER_WORDS)
def test_single_number_is_unchanged(word):
    assert sort_numbers(word) == word


@pytest.mark.parametrize("word", NUMBER_WORDS)
def test_repeated_number_preserves_every_occurrence(word):
    numbers = " ".join([word] * 5)
    assert sort_numbers(numbers) == numbers


@pytest.mark.parametrize("left,right", product(range(10), repeat=2))
def test_every_pair_is_sorted_by_numeric_value(left, right):
    numbers = f"{NUMBER_WORDS[left]} {NUMBER_WORDS[right]}"
    expected = f"{NUMBER_WORDS[min(left, right)]} {NUMBER_WORDS[max(left, right)]}"
    assert sort_numbers(numbers) == expected
