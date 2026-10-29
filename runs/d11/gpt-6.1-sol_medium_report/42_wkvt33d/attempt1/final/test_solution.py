"""Tests for the digit and value requirements in specialFilter's docstring."""

import pytest

from solution import specialFilter


@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        ([15, -73, 14, -15], 1),
        ([33, -2, -3, 45, 21, 109], 2),
    ],
)
def test_docstring_examples(nums, expected):
    assert specialFilter(nums) == expected


@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        ([], 0),
        (list(range(11)), 0),
        ([-11, -33, -135, -999, 0], 0),
        ([9, 10, 11, 12, 13], 2),
        ([11, 13, 15, 17, 19, 31, 55, 77, 99], 9),
        ([12, 21, 22, 34, 43, 56, 65, 78, 87, 90], 0),
        ([101, 103, 105, 107, 109, 12031, 90807], 7),
        ([1110, 2111, 2002, 100, 9998], 0),
        ([11, 11, 11, 22, 33, 33], 5),
        ([10**100 + 1, 2 * 10**100 + 1, 9 * 10**100 + 9], 2),
    ],
)
def test_counts_qualifying_elements(nums, expected):
    assert specialFilter(nums) == expected


@pytest.mark.parametrize("first_digit", range(1, 10))
@pytest.mark.parametrize("last_digit", range(10))
def test_every_pair_of_endpoint_digits(first_digit, last_digit):
    number = first_digit * 100 + last_digit
    expected = int(first_digit % 2 == 1 and last_digit % 2 == 1)
    assert specialFilter([number]) == expected


def test_does_not_modify_input():
    nums = [109, -73, 14, 33, 10, 109]
    original = nums.copy()

    assert specialFilter(nums) == 3
    assert nums == original
