"""Tests for the zero-based QuickSelect function's documented input domain."""

from itertools import product
import random

import pytest

from solution import kth


@pytest.mark.parametrize(
    "arr",
    [
        [42],
        [1, 2],
        [2, 1],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [3, 1, 5, 2, 4],
        [7, 7, 7, 7],
        [3, 1, 3, 5, 3, 1, 5],
        [-10, -3, -20, -1, -3],
        [0, -5, 5, 0, -1, 1],
        [10**100, -(10**100), 0, 10**100],
    ],
    ids=[
        "singleton", "ascending-pair", "descending-pair", "ascending",
        "descending", "unsorted", "all-equal", "duplicates", "negative",
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
        ([2, 1, 4, 3, 5], 4, 5),  # Recurse above the pivot.
        ([3, 1, 3, 5, 3, 2, 4], 2, 3),  # First pivot rank.
        ([3, 1, 3, 5, 3, 2, 4], 4, 3),  # Last pivot rank.
        ([3, 1, 3, 5, 3, 2, 4], 5, 4),  # First rank above duplicates.
    ],
)
def test_partition_boundaries(arr, k, expected):
    assert kth(arr, k) == expected


def test_all_small_lists_and_valid_ranks():
    for length in range(1, 7):
        for values in product((-1, 0, 1), repeat=length):
            arr = list(values)
            for k, expected in enumerate(sorted(arr)):
                assert kth(arr, k) == expected, (arr, k)


def test_seeded_random_lists():
    rng = random.Random(2026)
    for length in (10, 25, 50, 100):
        for _ in range(10):
            arr = [rng.randint(-100, 100) for _ in range(length)]
            for k, expected in enumerate(sorted(arr)):
                assert kth(arr, k) == expected, (arr, k)


def test_input_list_is_preserved():
    arr = [3, -1, 5, 3, 0, 2]
    original = arr.copy()
    for k in range(len(arr)):
        kth(arr, k)
        assert arr == original
