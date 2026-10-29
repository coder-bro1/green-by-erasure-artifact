"""Tests for the documented numeral ordering in solution.sort_numbers."""

import pytest

from solution import sort_numbers


NUMERALS = (
    "zero", "one", "two", "three", "four",
    "five", "six", "seven", "eight", "nine",
)


@pytest.mark.parametrize("numeral", NUMERALS)
def test_single_numeral(numeral):
    assert sort_numbers(numeral) == numeral


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param("", "", id="empty-input"),
        pytest.param(" ".join(NUMERALS), " ".join(NUMERALS), id="all-already-sorted"),
        pytest.param("zero zero one one nine nine", "zero zero one one nine nine", id="sorted-duplicates"),
        pytest.param("five five five", "five five five", id="identical-values"),
    ],
)
def test_already_sorted_numbers(numbers, expected):
    assert sort_numbers(numbers) == expected


@pytest.mark.xfail(
    strict=True,
    reason="sort_numbers preserves input order instead of sorting numerals from smallest to largest as documented",
)
@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param("three one five", "one three five", id="docstring-example"),
        pytest.param("one zero", "zero one", id="two-values-reversed"),
        pytest.param(" ".join(reversed(NUMERALS)), " ".join(NUMERALS), id="all-reversed"),
        pytest.param("eight five four nine one seven six three two zero", " ".join(NUMERALS), id="numeric-not-alphabetical"),
        pytest.param("nine zero nine one zero", "zero zero one nine nine", id="unsorted-duplicates"),
    ],
)
def test_unsorted_numbers_are_sorted_numerically(numbers, expected):
    assert sort_numbers(numbers) == expected
