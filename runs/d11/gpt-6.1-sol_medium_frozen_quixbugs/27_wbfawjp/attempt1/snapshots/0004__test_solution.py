"""Tests for the zero-based QuickSelect function's documented input domain."""

from itertools import product
import random

import pytest

from solution import kth


@pytest.mark.parametrize(
    "arr",
    [
        [42],
        [2, 1],
        [5, 4, 3, 2, 1],
        [7, 7, 7, 7],
        [5, 3, 5, 1, 3, 1, 3],
        [-1, -3, -3, -10, -20],
        [5, 1, 0, 0, -1, -5],
        [10**100, 10**100, 0, -(10**100)],
    ],
    ids=[
        "singleton", "descending-pair",
        "descending", "all-equal", "duplicates", "negative",
        "mixed-signs", "large-integers",
    ],
)
def test_every_rank_matches_sorted(arr):
    expected = sorted(arr)
    for k, value in enumerate(expected):
        assert kth(arr, k) == value


@pytest.mark.parametrize(
    ("arr", "k", "expected"),
    [
        ([4, 1, 2, 3, 5], 0, 1),  # Recurse below the pivot.
        ([3, 1, 3, 5, 3, 2, 4], 2, 3),  # First pivot rank.
        ([3, 1, 3, 5, 3, 2, 4], 4, 3),  # Last pivot rank.
    ],
)
def test_partition_boundaries(arr, k, expected):
    assert kth(arr, k) == expected


def test_minimum_of_all_small_lists():
    for length in range(1, 7):
        for values in product((-1, 0, 1), repeat=length):
            arr = list(values)
            assert kth(arr, 0) == min(arr), arr


def test_every_rank_of_seeded_descending_lists():
    rng = random.Random(2026)
    for length in (10, 25, 50, 100):
        for _ in range(10):
            arr = sorted(
                [rng.randint(-100, 100) for _ in range(length)], reverse=True
            )
            for k, expected in enumerate(sorted(arr)):
                assert kth(arr, k) == expected, (arr, k)


def test_input_list_is_preserved():
    arr = [5, 3, 3, 2, 0, -1]
    original = arr.copy()
    for k in range(len(arr)):
        kth(arr, k)
        assert arr == original


@pytest.mark.parametrize(
    ("arr", "k", "expected"),
    [([1, 2], 1, 2), ([1, 2, 3], 1, 2), ([3, 1, 3, 5, 3, 2, 4], 5, 4)],
    ids=["upper-partition-index-error", "upper-partition-wrong-value",
         "rank-above-duplicate-pivots"],
)
@pytest.mark.xfail(
    strict=True,
    reason="Known bug: upper-partition recursion does not adjust k",
    raises=(IndexError, AssertionError),
)
def test_upper_partition_known_bug(arr, k, expected):
    assert kth(arr, k) == expected
