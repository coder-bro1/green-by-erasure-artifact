"""Tests for knapsack, including its current strict capacity boundary."""

from itertools import combinations
from random import Random

import pytest

from solution import knapsack


@pytest.mark.parametrize(
    "capacity, items, expected",
    [
        pytest.param(100, [(60, 10), (50, 8), (20, 4), (20, 4), (8, 3), (3, 2)], 19, id="documented-example"),
        pytest.param(10, [], 0, id="empty-items"),
        pytest.param(0, [(1, 5), (2, 10)], 0, id="zero-capacity"),
        pytest.param(3, [(4, 10), (5, 20)], 0, id="all-items-too-heavy"),
        pytest.param(6, [(5, 12)], 12, id="single-item-fits"),
        pytest.param(10, [(2, 3), (3, 4), (4, 5)], 12, id="all-items-fit"),
        pytest.param(11, [(9, 10), (5, 7), (5, 7)], 14, id="combination-beats-largest-value"),
        pytest.param(11, [(6, 12), (5, 9), (5, 9)], 18, id="ratio-greedy-is-suboptimal"),
        pytest.param(7, [(2, 5)], 5, id="item-cannot-be-reused"),
        pytest.param(7, [(2, 5), (2, 5), (2, 5)], 15, id="duplicate-items-are-distinct"),
        pytest.param(8, [(2, 0), (3, -5), (4, 7)], 7, id="nonpositive-values-are-optional"),
        pytest.param(8, [(2, -3), (3, -1)], 0, id="taking-no-items-is-allowed"),
    ],
)
def test_knapsack_examples(capacity, items, expected):
    assert knapsack(capacity, items) == expected


@pytest.mark.parametrize(
    "capacity, items, expected",
    [
        (5, [(5, 12)], 0),
        (5, [(2, 4), (3, 6)], 6),
        (1, [(1, 8)], 0),
    ],
)
def test_current_behavior_excludes_exact_capacity(capacity, items, expected):
    # Characterize the existing boundary behavior; the docstring permits equality.
    assert knapsack(capacity, items) == expected


def brute_force_strict_capacity(capacity, items):
    """Independent subset enumeration matching the current positive-weight boundary."""
    best = 0
    for count in range(1, len(items) + 1):
        for subset in combinations(items, count):
            if sum(weight for weight, _ in subset) < capacity:
                best = max(best, sum(value for _, value in subset))
    return best


def test_matches_exhaustive_subset_search():
    rng = Random(2026)
    for _ in range(100):
        items = [(rng.randint(1, 10), rng.randint(-5, 20)) for _ in range(rng.randint(0, 8))]
        capacity = rng.randint(0, 25)
        assert knapsack(capacity, items) == brute_force_strict_capacity(capacity, items), (capacity, items)


def test_item_order_does_not_change_result():
    items = [(6, 10), (4, 9), (3, 6), (2, 5)]
    expected = knapsack(10, items)
    assert knapsack(10, list(reversed(items))) == expected
    assert knapsack(10, sorted(items)) == expected


def test_does_not_modify_items():
    items = [(3, 7), (2, 4), (5, 12)]
    original = items.copy()
    knapsack(9, items)
    assert items == original
