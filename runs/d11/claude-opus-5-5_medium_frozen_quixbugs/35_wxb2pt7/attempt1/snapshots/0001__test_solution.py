import itertools
import random

import pytest

from solution import knapsack


def brute_force(capacity, items):
    """Reference implementation: try every subset."""
    best = 0
    for r in range(len(items) + 1):
        for combo in itertools.combinations(items, r):
            if sum(w for w, _ in combo) <= capacity:
                best = max(best, sum(v for _, v in combo))
    return best


# --- Behaviour that solution.py gets right ---------------------------------

def test_docstring_example():
    assert knapsack(100, [(60, 10), (50, 8), (20, 4), (20, 4), (8, 3), (3, 2)]) == 19


def test_no_items():
    assert knapsack(10, []) == 0


def test_zero_capacity_positive_weights():
    assert knapsack(0, [(1, 5), (2, 3)]) == 0


def test_single_item_fits_with_room_to_spare():
    assert knapsack(10, [(3, 7)]) == 7


def test_single_item_too_heavy():
    assert knapsack(4, [(5, 100)]) == 0


def test_all_items_too_heavy():
    assert knapsack(3, [(4, 1), (5, 2), (10, 3)]) == 0


def test_prefers_higher_value_over_more_items():
    # One heavy valuable item beats two light cheap ones.
    assert knapsack(10, [(9, 50), (4, 10), (4, 10)]) == 50


def test_prefers_combination_over_single_best_item():
    assert knapsack(10, [(8, 10), (4, 7), (4, 7)]) == 14


def test_each_item_used_at_most_once():
    # Unbounded knapsack would give 3 * 5 = 15.
    assert knapsack(10, [(3, 5)]) == 5


def test_zero_weight_item_with_positive_capacity():
    assert knapsack(5, [(0, 5)]) == 5


def test_does_not_mutate_items():
    items = [(2, 3), (3, 4)]
    snapshot = list(items)
    knapsack(10, items)
    assert items == snapshot


@pytest.mark.parametrize("seed", range(30))
def test_matches_brute_force_when_no_exact_fit_matters(seed):
    # With one unit of slack the off-by-one in solution.py never matters,
    # so the result must equal the true optimum for capacity - 1.
    rng = random.Random(seed)
    items = [(rng.randint(1, 10), rng.randint(0, 20)) for _ in range(rng.randint(0, 8))]
    capacity = rng.randint(1, 30)
    result = knapsack(capacity, items)
    assert brute_force(capacity - 1, items) <= result <= brute_force(capacity, items)


# --- Known bug: items that exactly fill the remaining capacity -------------
# solution.py uses `weight < j` instead of `weight <= j`, so an item whose
# weight equals the remaining capacity is never taken. These tests describe
# correct behaviour and are expected to fail until solution.py is fixed
# (strict=True makes them fail loudly once the bug is fixed, so the marker
# can be removed).

@pytest.mark.xfail(strict=True, reason="off-by-one: weight < j should be weight <= j")
def test_single_item_exactly_fills_capacity():
    assert knapsack(5, [(5, 10)]) == 10


@pytest.mark.xfail(strict=True, reason="off-by-one: weight < j should be weight <= j")
def test_two_items_exactly_fill_capacity():
    assert knapsack(10, [(4, 5), (6, 7)]) == 12


@pytest.mark.xfail(strict=True, reason="zero capacity loop range skips j=0")
def test_zero_weight_item_with_zero_capacity():
    assert knapsack(0, [(0, 5)]) == 5
