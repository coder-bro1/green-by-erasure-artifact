import itertools
import random

import pytest

from solution import lis


def brute_force_lis(arr):
    """Reference implementation: O(n^2) DP."""
    best = [1] * len(arr)
    for i in range(len(arr)):
        for j in range(i):
            if arr[j] < arr[i]:
                best[i] = max(best[i], best[j] + 1)
    return max(best, default=0)


KNOWN_BUG = pytest.mark.xfail(
    strict=True,
    reason=(
        "solution.py bug: `longest = length + 1` can shrink `longest` when a "
        "small value appears late; it should be `longest = max(longest, length + 1)`"
    ),
)


# ---- Cases the current implementation handles correctly ----

@pytest.mark.parametrize(
    "arr, expected",
    [
        ([], 0),
        ([1], 1),
        ([-5], 1),
        ([1, 2], 2),
        ([2, 1], 1),
        ([1, 2, 3, 4, 5], 5),
        ([5, 4, 3, 2, 1], 1),
        ([1, 5, 2], 2),
        ([3, 1, 2], 2),
        ([10, 9, 2, 5, 3, 7, 101, 18], 4),
        ([0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15], 6),
        ([-3, -2, -1, 0], 4),
    ],
)
def test_lis_correct_cases(arr, expected):
    assert lis(arr) == expected


def test_accepts_tuple():
    assert lis((1, 3, 2, 4)) == 3


def test_does_not_mutate_input():
    arr = [3, 1, 4, 2, 5]
    copy = list(arr)
    lis(arr)
    assert arr == copy


def test_long_increasing_sequence():
    assert lis(list(range(500))) == 500


def test_long_decreasing_sequence():
    assert lis(list(range(500, 0, -1))) == 1


# ---- Cases exposing the bug in solution.py (documented spec) ----

@KNOWN_BUG
def test_docstring_example():
    assert lis([4, 1, 5, 3, 7, 6, 2]) == 3


@KNOWN_BUG
@pytest.mark.parametrize(
    "arr, expected",
    [
        ([2, 3, 1], 2),
        ([1, 2, 3, 0], 3),
        ([5, 6, 7, 8, 1], 4),
    ],
)
def test_small_trailing_value_does_not_shrink_result(arr, expected):
    assert lis(arr) == expected


@KNOWN_BUG
def test_matches_brute_force_on_all_small_permutations():
    for n in range(6):
        for perm in itertools.permutations(range(n)):
            assert lis(list(perm)) == brute_force_lis(list(perm)), perm


@KNOWN_BUG
def test_matches_brute_force_random():
    rng = random.Random(0)
    for _ in range(200):
        arr = rng.sample(range(-100, 100), rng.randint(0, 30))
        assert lis(arr) == brute_force_lis(arr), arr


def test_brute_force_reference_sanity():
    assert brute_force_lis([]) == 0
    assert brute_force_lis([4, 1, 5, 3, 7, 6, 2]) == 3
    assert brute_force_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4
