"""Tests for solution.kth (QuickSelect).

Known defect in solution.py: when k lands in the `above` partition the code
recurses with `kth(above, k)` instead of `kth(above, k - num_lessoreq)`.
Cases that exercise that branch are marked xfail(strict=True), so they
document the bug and will start failing (XPASS) once it is fixed, prompting
removal of the marker.
"""
import random

import pytest

from solution import kth

KNOWN_BUG = pytest.mark.xfail(
    strict=True,
    reason="kth recurses into `above` without offsetting k by num_lessoreq",
)


# --- Cases that never take the buggy `above` branch -------------------------

def test_single_element():
    assert kth([42], 0) == 42


def test_k_zero_sorted_ascending():
    assert kth([1, 2, 3, 4, 5], 0) == 1


def test_pivot_is_answer():
    # arr[0] is the median, so the pivot is returned directly.
    assert kth([3, 1, 5, 2, 4], 2) == 3


def test_max_when_first_element_is_max():
    assert kth([3, 1, 2], 2) == 3


def test_descending_input_every_k():
    arr = [5, 4, 3, 2, 1]
    for k in range(len(arr)):
        assert kth(arr, k) == sorted(arr)[k]


def test_all_duplicates():
    arr = [7, 7, 7, 7]
    for k in range(len(arr)):
        assert kth(arr, k) == 7


def test_duplicates_of_pivot_in_middle():
    arr = [2, 1, 2, 2, 0]
    for k in range(len(arr)):
        assert kth(arr, k) == sorted(arr)[k]


def test_negative_numbers():
    assert kth([0, -5, -1, -3], 1) == -3


def test_does_not_mutate_input():
    arr = [4, 2, 3, 1]
    original = list(arr)
    kth(arr, 1)
    assert arr == original


def test_random_descending_or_below_only_paths():
    # A strictly descending list always recurses via `below` or returns the
    # pivot, so it is safe from the bug for every k.
    rng = random.Random(0)
    for _ in range(50):
        arr = sorted(rng.sample(range(-100, 100), rng.randint(1, 20)), reverse=True)
        for k in range(len(arr)):
            assert kth(arr, k) == sorted(arr)[k]


# --- Cases that hit the buggy `above` branch --------------------------------

@KNOWN_BUG
def test_max_of_ascending_list():
    assert kth([1, 2, 3], 2) == 3  # currently raises IndexError


@KNOWN_BUG
def test_middle_of_ascending_list():
    assert kth([1, 2, 3, 4, 5], 2) == 3


@KNOWN_BUG
def test_wrong_value_returned():
    # Currently returns 3 instead of 2 (no exception, silently wrong).
    assert kth([1, 5, 6, 7, 2, 3, 4], 1) == 2


@KNOWN_BUG
def test_two_elements_ascending():
    assert kth([1, 2], 1) == 2


@KNOWN_BUG
def test_matches_sorted_on_random_inputs():
    rng = random.Random(1234)
    for _ in range(200):
        arr = [rng.randint(-50, 50) for _ in range(rng.randint(1, 30))]
        for k in range(len(arr)):
            assert kth(arr, k) == sorted(arr)[k]
