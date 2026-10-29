"""Tests for solution.kheapsort.

NOTE: solution.py has a known bug. The main loop is `for x in arr:` but should be
`for x in arr[k:]:`, so the first k elements are pushed onto the heap twice.
When k > 0 the output then has duplicates and may come out of order.
Tests for the documented (correct) behaviour that hit this bug are marked
`xfail(strict=True)`: they are expected to fail now, and they turn into hard
failures (XPASS) once the bug is fixed, which tells you to remove the marker.
"""
import inspect
import random

import pytest

from solution import kheapsort

BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py iterates over arr instead of arr[k:], duplicating the first k elements",
)


def make_k_sorted(n, k, seed):
    """Build a list of unique ints where each element is at most k from its sorted position."""
    rng = random.Random(seed)
    arr = list(range(n))
    # Shuffle inside disjoint windows of size k+1, so no element moves more than k.
    for start in range(0, n, k + 1):
        window = arr[start:start + k + 1]
        rng.shuffle(window)
        arr[start:start + k + 1] = window
    return arr


# ---- Behaviour that works with the current implementation ----

def test_returns_generator():
    assert inspect.isgenerator(kheapsort([1, 2, 3], 0))


def test_k_zero_sorted_input_docstring_example():
    assert list(kheapsort([1, 2, 3, 4, 5], 0)) == [1, 2, 3, 4, 5]


def test_empty_list():
    assert list(kheapsort([], 0)) == []


def test_empty_list_with_positive_k():
    assert list(kheapsort([], 3)) == []


def test_single_element():
    assert list(kheapsort([42], 0)) == [42]


def test_negative_numbers_k_zero():
    assert list(kheapsort([-5, -2, 0, 7], 0)) == [-5, -2, 0, 7]


def test_input_not_mutated():
    arr = [3, 2, 1, 5, 4]
    list(kheapsort(arr, 2))
    assert arr == [3, 2, 1, 5, 4]


def test_lazy_evaluation():
    gen = kheapsort([1, 2, 3], 0)
    assert next(gen) == 1
    assert next(gen) == 2


def test_output_contains_all_input_elements():
    # Holds even with the bug: every element shows up at least once.
    arr = [3, 2, 1, 5, 4]
    assert set(kheapsort(arr, 2)) == set(arr)


# ---- Documented behaviour that the current bug breaks ----

@BUG
def test_docstring_example_k2():
    assert list(kheapsort([3, 2, 1, 5, 4], 2)) == [1, 2, 3, 4, 5]


@BUG
def test_docstring_example_reversed_k4():
    assert list(kheapsort([5, 4, 3, 2, 1], 4)) == [1, 2, 3, 4, 5]


@BUG
def test_single_element_positive_k():
    assert list(kheapsort([42], 1)) == [42]


@BUG
def test_adjacent_swaps_k1():
    assert list(kheapsort([2, 1, 4, 3, 6, 5], 1)) == [1, 2, 3, 4, 5, 6]


@BUG
def test_sorted_input_positive_k():
    assert list(kheapsort([1, 2, 3, 4, 5], 2)) == [1, 2, 3, 4, 5]


@BUG
def test_output_length_matches_input():
    arr = [3, 2, 1, 5, 4]
    assert len(list(kheapsort(arr, 2))) == len(arr)


@BUG
@pytest.mark.parametrize("n,k,seed", [(10, 1, 0), (50, 3, 1), (100, 7, 2), (20, 19, 3)])
def test_random_k_sorted_arrays(n, k, seed):
    arr = make_k_sorted(n, k, seed)
    assert list(kheapsort(arr, k)) == sorted(arr)
