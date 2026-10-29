"""Tests for the current behavior of solution.py, including its known limitation."""

import pytest

from solution import possible_change


@pytest.mark.parametrize("coins", [[], [1], [2, 5], [1, 5, 10, 25]])
def test_zero_total_has_one_way(coins):
    assert possible_change(coins, 0) == 1


@pytest.mark.parametrize("coins", [[], [1], [2, 5]])
@pytest.mark.parametrize("total", [-1, -10])
def test_negative_total_has_no_ways(coins, total):
    assert possible_change(coins, total) == 0


@pytest.mark.parametrize("total", [1, 5, 11])
def test_empty_coins_with_positive_total_raises(total):
    # The implementation has no base case for an exhausted coin list.
    with pytest.raises(ValueError, match="not enough values to unpack"):
        possible_change([], total)


@pytest.mark.parametrize(
    ("coins", "total"),
    [
        ([1], 1),
        ([2], 3),
        ([1, 2], 4),
        ([5, 2, 1], 5),
        ([1, 5, 10, 25], 11),
    ],
)
def test_positive_total_currently_raises_without_mutating_coins(coins, total):
    # Even solvable totals (including the docstring example) eventually reach
    # the missing empty-list base case. Record that behavior explicitly.
    original_coins = coins.copy()

    with pytest.raises(ValueError, match="not enough values to unpack"):
        possible_change(coins, total)

    assert coins == original_coins
