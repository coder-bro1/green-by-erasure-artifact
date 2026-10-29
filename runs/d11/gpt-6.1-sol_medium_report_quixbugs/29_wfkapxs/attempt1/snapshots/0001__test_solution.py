"""Tests for the documented coin-change counting behavior."""

import pytest

from solution import possible_change


@pytest.mark.parametrize("coins", [[], [1], [2, 5], [1, 5, 10, 25]])
def test_zero_total_has_one_empty_combination(coins):
    assert possible_change(coins, 0) == 1


@pytest.mark.parametrize("coins", [[], [1], [2, 5]])
@pytest.mark.parametrize("total", [-1, -5])
def test_negative_total_has_no_combinations(coins, total):
    assert possible_change(coins, total) == 0


@pytest.mark.parametrize(
    "coins, total, expected",
    [
        pytest.param([1, 5, 10, 25], 11, 4, id="docstring-example"),
        pytest.param([], 3, 0, id="no-denominations"),
        pytest.param([1], 4, 1, id="repeat-unit-coin"),
        pytest.param([2], 6, 1, id="repeat-single-denomination"),
        pytest.param([2], 3, 0, id="single-denomination-impossible"),
        pytest.param([2, 4], 3, 0, id="multiple-denominations-impossible"),
        pytest.param([5, 10], 3, 0, id="all-coins-exceed-total"),
        pytest.param([2, 3], 3, 1, id="later-denomination-exact-match"),
        pytest.param([1, 2], 4, 3, id="combinations-not-permutations"),
        pytest.param([1, 2, 3], 4, 4, id="three-denominations"),
        pytest.param([3, 1, 2], 4, 4, id="unsorted-denominations"),
        pytest.param([2, 3, 7], 7, 2, id="without-unit-coin"),
    ],
)
def test_positive_total_counts_distinct_combinations(coins, total, expected):
    assert possible_change(coins, total) == expected
