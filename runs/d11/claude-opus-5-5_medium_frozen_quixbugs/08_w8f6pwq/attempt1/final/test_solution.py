"""Tests for solution.possible_change.

KNOWN BUG in solution.py: the recursion never handles an exhausted coin list
while total > 0, so `first, *rest = coins` raises ValueError for practically
every positive total (including the docstring example). solution.py must not
be modified, so tests asserting the documented behavior for those inputs are
marked xfail(strict=True, raises=ValueError). Once the bug is fixed they will
XPASS, and strict mode turns that into a failure so the markers get removed.
"""
import pytest

from solution import possible_change

empty_coins_bug = pytest.mark.xfail(
    strict=True,
    raises=ValueError,
    reason="solution.py does not handle empty coins with total > 0",
)


# ---- Behavior that currently works -------------------------------------

@pytest.mark.parametrize("coins", [[], [1], [5], [1, 5, 10, 25], [3, 7]])
def test_zero_total_has_exactly_one_way(coins):
    assert possible_change(coins, 0) == 1


@pytest.mark.parametrize("coins", [[1], [1, 5, 10, 25], [2, 3]])
@pytest.mark.parametrize("total", [-1, -5, -100])
def test_negative_total_has_no_ways(coins, total):
    assert possible_change(coins, total) == 0


def test_negative_total_with_empty_coins():
    assert possible_change([], -3) == 0


def test_does_not_mutate_coins():
    coins = [1, 5, 10, 25]
    possible_change(coins, 0)
    possible_change(coins, -1)
    assert coins == [1, 5, 10, 25]


# ---- Documented behavior that currently crashes (bug) ------------------

@empty_coins_bug
def test_docstring_example():
    assert possible_change([1, 5, 10, 25], 11) == 4


@empty_coins_bug
def test_empty_coins_positive_total_has_no_ways():
    assert possible_change([], 3) == 0


@empty_coins_bug
@pytest.mark.parametrize(
    "coins, total, expected",
    [
        ([1], 3, 1),
        ([2], 3, 0),
        ([2], 4, 1),
        ([1, 2], 4, 3),          # 1111, 112, 22
        ([2, 5, 3, 6], 10, 5),
        ([1, 2, 5], 5, 4),
        ([1, 5, 10, 25], 100, 242),
        ([25, 10, 5, 1], 11, 4),  # order of coins must not matter
        ([7], 5, 0),
    ],
)
def test_known_counts(coins, total, expected):
    assert possible_change(coins, total) == expected
