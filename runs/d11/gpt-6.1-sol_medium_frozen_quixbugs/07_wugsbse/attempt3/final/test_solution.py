"""Tests for the current behavior of solution.max_sublist_sum.

The implementation computes a maximum prefix sum, allowing an empty prefix.
It does not reset the running sum to find sublists starting after index zero.
"""

from itertools import product

import pytest

from solution import max_sublist_sum


@pytest.mark.parametrize(
    ("arr", "expected"),
    [
        pytest.param([], 0, id="empty"),
        pytest.param([0], 0, id="single-zero"),
        pytest.param([7], 7, id="single-positive"),
        pytest.param([-7], 0, id="single-negative"),
        pytest.param([0, 0, 0], 0, id="all-zeros"),
        pytest.param([-4, -1, -9], 0, id="all-negative"),
        pytest.param([1, 2, 3, 4], 10, id="all-positive"),
        pytest.param([4, -5, 2, 1, -1, 3], 4, id="docstring-input-current-result"),
        pytest.param([8, -3, -9], 8, id="best-prefix-before-end"),
        pytest.param([3, -1, 4], 6, id="best-prefix-at-end"),
        pytest.param([2, -2, 2, -2], 2, id="tied-prefixes"),
        pytest.param([-5, 2, 1], 0, id="negative-prefix-never-recovers"),
        pytest.param([-5, 10], 5, id="negative-prefix-recovers"),
        pytest.param([4, -10, 8], 4, id="running-sum-is-not-reset"),
        pytest.param([10**100, -1, 2], 10**100 + 1, id="large-integers"),
    ],
)
def test_max_sublist_sum_current_behavior(arr, expected):
    assert max_sublist_sum(arr) == expected


def test_does_not_modify_input():
    arr = [4, -5, 2, 1, -1, 3]
    original = arr.copy()

    max_sublist_sum(arr)

    assert arr == original


@pytest.mark.xfail(
    strict=True,
    reason="The documented maximum sublist sum is 5, but the implementation returns 4.",
)
def test_documented_example():
    assert max_sublist_sum([4, -5, 2, 1, -1, 3]) == 5


def test_matches_independent_prefix_sum_reference_for_small_lists():
    for length in range(6):
        for values in product((-2, 0, 3), repeat=length):
            arr = list(values)
            expected = max(sum(arr[:end]) for end in range(length + 1))

            assert max_sublist_sum(arr) == expected, f"Input: {arr!r}"
