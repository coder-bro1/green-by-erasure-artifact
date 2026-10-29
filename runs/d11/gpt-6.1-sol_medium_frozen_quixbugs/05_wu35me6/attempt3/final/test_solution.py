"""Tests for the documented binary-search contract."""

from itertools import combinations_with_replacement

import pytest

from solution import find_in_sorted


@pytest.mark.parametrize("target", [-10, 0, 10])
def test_empty_list_returns_minus_one(target):
    assert find_in_sorted([], target) == -1


@pytest.mark.parametrize(
    ("values", "target", "expected"),
    [
        ([7], 7, 0),
        ([1, 3], 1, 0),
        ([1, 3], 3, 1),
        ([1, 3, 5, 7, 9], 1, 0),
        ([1, 3, 5, 7, 9], 5, 2),
        ([1, 3, 5, 7, 9], 9, 4),
        ([2, 4, 6, 8, 10, 12], 2, 0),
        ([2, 4, 6, 8, 10, 12], 8, 3),
        ([2, 4, 6, 8, 10, 12], 12, 5),
        ([-9, -5, -1, 0, 4], -5, 1),
        ([-9, -5, -1, 0, 4], 0, 3),
        ([-10**100, 0, 10**100], 10**100, 2),
    ],
)
def test_returns_index_of_present_value_without_mutating_input(values, target, expected):
    original = values.copy()
    assert find_in_sorted(values, target) == expected
    assert values == original


def test_documented_example():
    assert find_in_sorted([3, 4, 5, 5, 5, 5, 6], 5) == 3


@pytest.mark.parametrize("values", [[7], [1, 3], [-8, -4, 0], [2, 2, 2, 2]])
def test_target_below_minimum_returns_minus_one(values):
    assert find_in_sorted(values, values[0] - 1) == -1


def test_present_values_in_all_small_sorted_lists_including_duplicates():
    # The contract permits any matching index when a value occurs repeatedly.
    for length in range(1, 7):
        for values_tuple in combinations_with_replacement([-2, 0, 1, 5], length):
            values = list(values_tuple)
            for target in set(values):
                index = find_in_sorted(values, target)
                assert 0 <= index < len(values), (values, target, index)
                assert values[index] == target, (values, target, index)
            assert values == list(values_tuple)


@pytest.mark.xfail(
    strict=True,
    raises=RecursionError,
    reason="The right-hand recursive branch retains mid and can fail to shrink the interval.",
)
@pytest.mark.parametrize(
    ("values", "target"),
    [
        ([1], 2),
        ([1, 3, 5], 2),
        ([-5, -1, 3], 0),
        ([2, 2, 2, 2], 3),
        ([1, 3, 5, 7], 8),
    ],
    ids=["singleton-above", "interior-gap", "gap-across-zero", "duplicates-above", "above-maximum"],
)
def test_other_absent_values_return_minus_one(values, target):
    assert find_in_sorted(values, target) == -1
