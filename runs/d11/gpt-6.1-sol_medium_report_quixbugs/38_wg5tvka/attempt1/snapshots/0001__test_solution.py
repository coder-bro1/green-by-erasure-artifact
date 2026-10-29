"""Tests for the documented distinct coin-change combinations."""

from itertools import permutations

import pytest

from solution import possible_change


@pytest.mark.parametrize(
    "coins,total,expected",
    [
        ([1, 5, 10, 25], 11, 4),  # The docstring's example.
        ([1, 2, 5], 5, 4),
        ([2, 3, 5], 10, 4),
        ([1, 2, 3], 4, 4),  # Order of individual coins is irrelevant.
        ([2, 4], 7, 0),
        ([4, 6], 2, 0),
        ([5], 5, 1),
        ([5], 15, 1),  # Each denomination can be used repeatedly.
        ([5], 16, 0),
        ([1], 12, 1),
        ([], 7, 0),
        ([], 0, 1),  # The empty combination makes zero.
        ([2, 5], 0, 1),
        ([1, 2], -1, 0),
        ([], -3, 0),
        ([1, 5, 100], 6, 2),
    ],
)
def test_change_counts(coins, total, expected):
    assert possible_change(coins, total) == expected


@pytest.mark.parametrize("coins", list(permutations([1, 2, 5])))
def test_denomination_order_does_not_change_count(coins):
    assert possible_change(list(coins), 5) == 4


def test_input_list_is_not_modified():
    coins = [5, 1, 2]
    original = coins.copy()

    assert possible_change(coins, 5) == 4
    assert coins == original


@pytest.mark.parametrize(
    "coins,total,expected",
    [([1, 1], 2, 1), ([1, 2, 2], 4, 3), ([2, 2], 3, 0)],
)
def test_repeated_values_represent_the_same_denomination(coins, total, expected):
    assert possible_change(coins, total) == expected
