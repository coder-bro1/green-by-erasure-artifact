"""Tests for the documented 0/1 knapsack behavior."""

from itertools import combinations, product

import pytest

from solution import knapsack


@pytest.mark.parametrize(
    "capacity, items, expected",
    [
        (100, [(60, 10), (50, 8), (20, 4), (20, 4), (8, 3), (3, 2)], 19),
        (0, [], 0),
        (10, [], 0),
        (0, [(1, 10)], 0),
        (3, [(4, 10), (5, 20)], 0),
        (5, [(5, 12)], 12),
        (10, [(2, 3), (3, 5)], 8),
        (6, [(3, 8)], 8),  # Each item may be taken only once.
        (6, [(3, 8), (3, 8)], 16),  # Identical entries are distinct items.
        (4, [(3, 5), (2, 3), (2, 3)], 6),
        (5, [(5, 10), (2, 7), (3, 8)], 15),
        (5, [(1, -5), (2, -1)], 0),
        (5, [(1, -5), (2, 4), (3, 0)], 4),
        (4, [(1, 0), (2, 0)], 0),
        (3, [(2, 5), (0, 7)], 12),
    ],
)
def test_documented_knapsack_cases(capacity, items, expected):
    assert knapsack(capacity, items) == expected


def brute_force_knapsack(capacity, items):
    """Find the optimum by enumerating subsets independently of the DP."""
    return max(
        sum(value for _, value in subset)
        for size in range(len(items) + 1)
        for subset in combinations(items, size)
        if sum(weight for weight, _ in subset) <= capacity
    )


@pytest.mark.parametrize("capacity", range(7))
def test_small_inputs_match_exhaustive_subset_search(capacity):
    choices = [(1, -1), (1, 0), (1, 3), (2, 2), (3, 5)]
    for count in range(4):
        for items in product(choices, repeat=count):
            items = list(items)
            assert knapsack(capacity, items) == brute_force_knapsack(capacity, items), (
                capacity,
                items,
            )


def test_result_is_independent_of_item_order():
    items = [(4, 7), (2, 5), (3, 6), (1, 1)]
    assert knapsack(5, items) == knapsack(5, list(reversed(items))) == 11


def test_does_not_modify_items():
    items = [(3, 5), (2, 4), (1, 2)]
    original = items.copy()
    assert knapsack(4, items) == 7
    assert items == original


@pytest.mark.xfail(
    strict=True,
    reason="The DP never computes capacity 0, so it discards positive-value zero-weight items at capacity 0.",
)
@pytest.mark.parametrize(
    "items, expected",
    [([(0, 5)], 5), ([(0, 3), (0, 4)], 7), ([(0, 5), (1, 100)], 5)],
)
def test_zero_weight_items_fit_zero_capacity(items, expected):
    assert knapsack(0, items) == expected


@pytest.mark.xfail(
    strict=True,
    reason="The uncomputed capacity-0 DP state loses earlier zero-weight items when a later item fills the knapsack exactly.",
)
def test_zero_weight_item_combines_with_exact_fit():
    assert knapsack(2, [(0, 7), (2, 5)]) == 12
