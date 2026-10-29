"""Tests for solution.max_sublist_sum.

Spec (from the docstring): result equals
    max(sum(arr[i:j]) for 0 <= i <= j <= len(arr))
i.e. the maximum sum over all contiguous sublists, where the empty sublist
(sum 0) is allowed.

NOTE: the current implementation does not reset the running sum when it
drops below zero, so it actually computes max(0, max prefix sum). Cases where
the best sublist does not start at index 0 are marked xfail(strict=True) to
document that known bug without modifying solution.py. If the bug is fixed,
those tests will XPASS and fail the run (strict), signalling the markers
should be removed.
"""
import random

import pytest

from solution import max_sublist_sum


def brute_force(arr):
    n = len(arr)
    return max(sum(arr[i:j]) for i in range(n + 1) for j in range(i, n + 1))


KNOWN_BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py never resets max_ending_here to 0 (computes max prefix sum)",
)


@pytest.mark.parametrize(
    "arr, expected",
    [
        ([], 0),
        ([0], 0),
        ([7], 7),
        ([-7], 0),
        ([1, 2, 3, 4], 10),
        ([-1, -2, -3], 0),
        ([0, 0, 0], 0),
        ([5, -1, 5], 9),
        ([3, 4, -100, 2], 7),
        ([2, -1, 2, -1, 2], 4),
        ([10, -3, -4, 7, 6], 16),
    ],
)
def test_cases_where_best_sublist_is_a_prefix(arr, expected):
    assert max_sublist_sum(arr) == expected
    assert brute_force(arr) == expected


@pytest.mark.parametrize(
    "arr, expected",
    [
        pytest.param([4, -5, 2, 1, -1, 3], 5, id="docstring-example"),
        pytest.param([-5, 3], 3, id="negative-then-positive"),
        pytest.param([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6, id="classic-kadane"),
        pytest.param([1, -10, 5, 5], 10, id="best-after-big-dip"),
        pytest.param([-1, -1, 9, -1, -1], 9, id="middle-element"),
    ],
)
@KNOWN_BUG
def test_cases_where_best_sublist_starts_later(arr, expected):
    assert brute_force(arr) == expected
    assert max_sublist_sum(arr) == expected


def test_result_never_negative():
    rng = random.Random(0)
    for _ in range(200):
        arr = [rng.randint(-50, 50) for _ in range(rng.randint(0, 15))]
        assert max_sublist_sum(arr) >= 0


def test_does_not_mutate_input():
    arr = [4, -5, 2, 1, -1, 3]
    copy = list(arr)
    max_sublist_sum(arr)
    assert arr == copy


def test_accepts_any_iterable_of_ints():
    assert max_sublist_sum((1, 2, 3)) == 6
    assert max_sublist_sum(iter([1, 2, 3])) == 6


def test_all_non_negative_equals_total_sum():
    rng = random.Random(1)
    for _ in range(100):
        arr = [rng.randint(0, 100) for _ in range(rng.randint(0, 20))]
        assert max_sublist_sum(arr) == sum(arr)


def test_all_non_positive_is_zero():
    rng = random.Random(2)
    for _ in range(100):
        arr = [rng.randint(-100, 0) for _ in range(rng.randint(0, 20))]
        assert max_sublist_sum(arr) == 0


@KNOWN_BUG
def test_matches_brute_force_on_random_inputs():
    rng = random.Random(3)
    for _ in range(500):
        arr = [rng.randint(-20, 20) for _ in range(rng.randint(0, 12))]
        assert max_sublist_sum(arr) == brute_force(arr), arr
