"""Tests for the binary-search contract documented in solution.py."""

from itertools import combinations_with_replacement

import pytest

from solution import find_in_sorted


def test_docstring_example():
    assert find_in_sorted([3, 4, 5, 5, 5, 5, 6], 5) == 3


@pytest.mark.parametrize(
    "arr, target, expected",
    [
        ([7], 7, 0),
        ([2, 9], 2, 0),
        ([2, 9], 9, 1),
        ([1, 3, 5, 7, 9], 1, 0),
        ([1, 3, 5, 7, 9], 5, 2),
        ([1, 3, 5, 7, 9], 9, 4),
        ([0, 2, 4, 6, 8, 10], 0, 0),
        ([0, 2, 4, 6, 8, 10], 4, 2),
        ([0, 2, 4, 6, 8, 10], 10, 5),
        ([-12, -5, -1, 0, 4], -5, 1),
        ([-12, -5, -1, 0, 4], 0, 3),
        ([-10**100, 0, 10**100], -10**100, 0),
        ([-10**100, 0, 10**100], 10**100, 2),
    ],
)
def test_present_value_has_expected_index(arr, target, expected):
    assert find_in_sorted(arr, target) == expected


@pytest.mark.parametrize(
    "arr, target",
    [
        ([], 0),
        ([], -1),
        ([7], 6),
        ([7], 8),
        ([2, 9], 1),
        ([2, 9], 5),
        ([2, 9], 10),
        ([1, 3, 5, 7, 9], 0),
        ([1, 3, 5, 7, 9], 4),
        ([1, 3, 5, 7, 9], 10),
        ([0, 2, 4, 6, 8, 10], 7),
        ([-12, -5, -1, 0, 4], -6),
        ([5, 5, 5, 5], 4),
        ([5, 5, 5, 5], 6),
    ],
)
def test_absent_value_returns_minus_one(arr, target):
    assert find_in_sorted(arr, target) == -1


@pytest.mark.parametrize(
    "arr, target",
    [
        ([5, 5], 5),
        ([5, 5, 5, 5], 5),
        ([1, 1, 2, 3, 4], 1),
        ([1, 2, 3, 4, 4], 4),
        ([-3, -3, -3, 0, 2, 2], -3),
        ([-3, -3, -3, 0, 2, 2], 2),
    ],
)
def test_duplicate_value_returns_a_matching_index(arr, target):
    # The contract allows any matching index, not necessarily the first one.
    index = find_in_sorted(arr, target)
    assert 0 <= index < len(arr)
    assert arr[index] == target


@pytest.mark.parametrize("length", range(8))
def test_all_small_sorted_lists(length):
    """Compare every small sorted input with a simple membership oracle."""
    for values in combinations_with_replacement([-2, -1, 0, 1, 2], length):
        arr = list(values)
        for target in range(-3, 4):
            index = find_in_sorted(arr, target)
            context = f"{arr=}, {target=}, {index=}"
            if target in arr:
                assert 0 <= index < len(arr), context
                assert arr[index] == target, context
            else:
                assert index == -1, context
