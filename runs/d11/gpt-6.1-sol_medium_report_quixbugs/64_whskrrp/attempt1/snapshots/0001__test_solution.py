"""Tests for the documented 0/1 knapsack contract."""

import pytest

from solution import knapsack


@pytest.mark.parametrize(
    "capacity, items, expected",
    [
        pytest.param(100, [(60, 10), (50, 8), (20, 4), (20, 4), (8, 3), (3, 2)], 19, id="docstring-example"),
        pytest.param(10, [], 0, id="empty-items"),
        pytest.param(0, [], 0, id="empty-items-zero-capacity"),
        pytest.param(0, [(1, 10), (2, 20)], 0, id="zero-capacity-positive-weights"),
        pytest.param(3, [(4, 10), (5, 20)], 0, id="all-items-overweight"),
        pytest.param(6, [(5, 12)], 12, id="single-item-with-spare-capacity"),
        pytest.param(7, [(3, 5)], 5, id="item-cannot-be-reused"),
        pytest.param(7, [(3, 5), (3, 5)], 10, id="duplicate-items-are-distinct"),
        pytest.param(11, [(6, 30), (5, 25), (5, 25)], 50, id="combination-beats-greedy-choice"),
        pytest.param(9, [(2, 0), (3, 7), (4, 6)], 13, id="zero-value-item"),
        pytest.param(10, [(2, -5), (3, -1)], 0, id="may-leave-all-items"),
        pytest.param(6, [(2, -5), (3, 8)], 8, id="negative-value-item-can-be-skipped"),
        pytest.param(1, [(0, 4), (0, 6)], 10, id="zero-weight-items-count-once"),
        pytest.param(4, [(0, 4), (2, 6)], 10, id="mixed-zero-and-positive-weights"),
    ],
)
def test_documented_maximum_value(capacity, items, expected):
    assert knapsack(capacity, items) == expected


@pytest.mark.xfail(
    strict=True,
    reason="The docstring permits total weight equal to capacity, but weight < j excludes exact fits.",
)
@pytest.mark.parametrize(
    "capacity, items, expected",
    [
        pytest.param(5, [(5, 12)], 12, id="single-item-exact-fit"),
        pytest.param(1, [(1, 9)], 9, id="unit-capacity-exact-fit"),
        pytest.param(5, [(2, 4), (3, 7)], 11, id="combination-exact-fit"),
        pytest.param(6, [(3, 5), (3, 5)], 10, id="duplicate-items-exact-fit"),
        pytest.param(10, [(6, 30), (5, 25), (5, 25)], 50, id="optimal-exact-fit-beats-partial-fill"),
    ],
)
def test_items_may_fill_capacity_exactly(capacity, items, expected):
    assert knapsack(capacity, items) == expected


@pytest.mark.xfail(
    strict=True,
    reason="Zero-weight items fit at capacity zero, but the DP never computes the zero-capacity column.",
)
@pytest.mark.parametrize(
    "items, expected",
    [
        pytest.param([(0, 5)], 5, id="one-zero-weight-item"),
        pytest.param([(0, 4), (0, 6)], 10, id="multiple-zero-weight-items"),
        pytest.param([(1, 100), (0, 7), (0, -3)], 7, id="skip-overweight-and-negative-items"),
    ],
)
def test_zero_weight_items_fit_at_zero_capacity(items, expected):
    assert knapsack(0, items) == expected


def test_item_order_does_not_change_result():
    items = [(6, 30), (5, 25), (5, 25), (0, 3)]
    assert knapsack(11, items) == 53
    assert knapsack(11, list(reversed(items))) == 53


def test_input_items_are_not_modified():
    items = [(4, 8), (2, 5), (2, 5)]
    original = items.copy()
    assert knapsack(9, items) == 18
    assert items == original
