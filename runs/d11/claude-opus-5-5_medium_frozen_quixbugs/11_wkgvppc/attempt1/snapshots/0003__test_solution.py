"""Tests for solution.bucketsort.

NOTE: solution.py currently contains a bug -- its output loop iterates
``enumerate(arr)`` instead of ``enumerate(counts)``. Tests that check the
documented contract (output == sorted(arr)) for non-empty input therefore
fail today. They are marked ``xfail(strict=True)`` so the suite passes while
the defect stays visible; once the bug is fixed they will XPASS and strict
mode will flag them so the marker can be removed.
"""
import random

import pytest

from solution import bucketsort

KNOWN_BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py iterates enumerate(arr) instead of enumerate(counts)",
)


# ---------------------------------------------------------------------------
# Behaviour that is correct today
# ---------------------------------------------------------------------------

def test_empty_list_returns_empty():
    assert bucketsort([], 5) == []


def test_empty_list_with_k_zero():
    assert bucketsort([], 0) == []


def test_returns_new_list_and_does_not_mutate_input():
    arr = []
    result = bucketsort(arr, 3)
    assert result is not arr
    assert arr == []


def test_does_not_mutate_nonempty_input():
    arr = [3, 1, 2]
    bucketsort(arr, 4)
    assert arr == [3, 1, 2]


def test_value_equal_to_k_violates_precondition_and_raises():
    with pytest.raises(IndexError):
        bucketsort([5], 5)


def test_value_greater_than_k_raises():
    with pytest.raises(IndexError):
        bucketsort([1, 10], 3)


def test_returns_list_type():
    assert isinstance(bucketsort([2, 0, 1], 3), list)


# ---------------------------------------------------------------------------
# Documented contract: output is arr in sorted order (fails due to bug)
# ---------------------------------------------------------------------------

@KNOWN_BUG
def test_single_element():
    assert bucketsort([0], 1) == [0]


@KNOWN_BUG
def test_single_nonzero_element():
    assert bucketsort([3], 5) == [3]


@KNOWN_BUG
def test_already_sorted():
    assert bucketsort([0, 1, 2, 3, 4], 5) == [0, 1, 2, 3, 4]


@KNOWN_BUG
def test_reverse_sorted():
    assert bucketsort([4, 3, 2, 1, 0], 5) == [0, 1, 2, 3, 4]


@KNOWN_BUG
def test_duplicates():
    assert bucketsort([3, 1, 3, 0, 1, 3], 4) == [0, 1, 1, 3, 3, 3]


@KNOWN_BUG
def test_all_same_value():
    assert bucketsort([2, 2, 2, 2], 3) == [2, 2, 2, 2]


@KNOWN_BUG
def test_k_larger_than_needed():
    assert bucketsort([5, 1, 9], 100) == [1, 5, 9]


@KNOWN_BUG
def test_output_length_matches_input():
    arr = [0, 0]
    assert len(bucketsort(arr, 2)) == len(arr)


@KNOWN_BUG
@pytest.mark.parametrize("seed", range(5))
def test_random_matches_sorted(seed):
    rng = random.Random(seed)
    k = rng.randint(1, 50)
    arr = [rng.randrange(k) for _ in range(rng.randint(1, 200))]
    assert bucketsort(arr, k) == sorted(arr)
