"""Regression tests for count_nums as implemented.

The implementation negates the leading digit of positive numbers as well.
These tests preserve that behavior; they do not assert the conflicting
examples in the function's docstring.
"""

import pytest

from solution import count_nums


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([], 0),
        ([0], 0),
        ([0, 0, 0], 0),
        ([-1, 11, -11], 2),
        ([1, 1, 2], 0),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9], 0),
        ([-1, -2, -3, -4, -5, -6, -7, -8, -9], 9),
        ([10, 100, 1000, 10000], 0),
        ([-10, -100, -1000, -10000], 4),
        ([11, 22, 99, 101, 202, 909], 0),
        ([12, 19, 123, 199, 9099], 5),
        ([21, 91, 310, 9001], 0),
        ([-11, -12, -21, -99, -123, -9001], 6),
        ([12, 12, 12, 21, 21], 3),
        ([0, 1, -1, 11, -11, 12, 21, -21], 4),
    ],
    ids=[
        "empty", "zero", "repeated-zero", "mixed-docstring-discrepancy",
        "positive-single-digit-docstring-discrepancy",
        "positive-single-digits", "negative-single-digits",
        "positive-powers-of-ten", "negative-powers-of-ten",
        "zero-transformed-sum-is-excluded", "positive-transformed-sums",
        "negative-transformed-sums", "negative-multiple-digits",
        "duplicates-count-separately", "mixed-signs",
    ],
)
def test_count_nums_current_behavior(numbers, expected):
    assert count_nums(numbers) == expected


@pytest.mark.parametrize("leading_digit", range(1, 10))
def test_positive_two_digit_threshold_is_strict(leading_digit):
    below = leading_digit * 10 + leading_digit - 1
    equal = leading_digit * 10 + leading_digit
    assert count_nums([below, equal]) == 0
    if leading_digit < 9:
        above = leading_digit * 10 + leading_digit + 1
        assert count_nums([above]) == 1


def test_arbitrarily_large_integers():
    power_of_ten = 10**100
    repeated_nines = int("9" * 101)
    assert count_nums(
        [power_of_ten, -power_of_ten, repeated_nines, -repeated_nines]
    ) == 3


def test_input_list_is_not_modified():
    numbers = [12, -21, 0, 11, 12, 1]
    original = numbers.copy()
    assert count_nums(numbers) == 3
    assert numbers == original


def test_repeated_calls_are_independent():
    assert count_nums([12, -1]) == 2
    assert count_nums([]) == 0
    assert count_nums([12, -1]) == 2
