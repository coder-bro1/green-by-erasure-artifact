import random

import pytest

from solution import find_in_sorted


# --- Found cases -----------------------------------------------------------

def test_docstring_example():
    assert find_in_sorted([3, 4, 5, 5, 5, 5, 6], 5) == 3


@pytest.mark.parametrize(
    "arr, x",
    [
        ([1], 1),
        ([1, 2], 1),
        ([1, 2], 2),
        ([1, 2, 3], 1),
        ([1, 2, 3], 3),
        ([-10, -5, 0, 5, 10], -10),
        ([-10, -5, 0, 5, 10], 0),
        ([-10, -5, 0, 5, 10], 10),
        (list(range(100)), 0),
        (list(range(100)), 99),
        (list(range(100)), 57),
    ],
)
def test_finds_present_element(arr, x):
    i = find_in_sorted(arr, x)
    assert 0 <= i < len(arr)
    assert arr[i] == x


def test_duplicates_returns_some_matching_index():
    arr = [2, 2, 2, 2, 2]
    i = find_in_sorted(arr, 2)
    assert arr[i] == 2


def test_every_element_of_random_sorted_lists_is_found():
    rng = random.Random(0)
    for _ in range(200):
        arr = sorted(rng.randint(-50, 50) for _ in range(rng.randint(1, 40)))
        for x in arr:
            i = find_in_sorted(arr, x)
            assert arr[i] == x


def test_does_not_mutate_input():
    arr = [1, 3, 5, 7]
    find_in_sorted(arr, 5)
    assert arr == [1, 3, 5, 7]


# --- Not-found cases that currently work ------------------------------------

def test_empty_list():
    assert find_in_sorted([], 5) == -1


@pytest.mark.parametrize(
    "arr, x",
    [
        ([1], 0),
        ([1, 2, 3], 0),
        ([5, 6, 7, 8], -100),
    ],
)
def test_smaller_than_all_elements_returns_minus_one(arr, x):
    assert find_in_sorted(arr, x) == -1


# --- Known bug --------------------------------------------------------------
# In solution.py the `x > arr[mid]` branch recurses with binsearch(mid, end)
# instead of binsearch(mid + 1, end). When x is absent and the search moves
# right, the range never shrinks and recursion never ends (RecursionError).
# These tests specify the correct behaviour and are strict xfails: if the
# bug is fixed they will XPASS and fail the run, prompting removal of the mark.

KNOWN_BUG = pytest.mark.xfail(
    raises=RecursionError,
    strict=True,
    reason="solution.py bug: binsearch(mid, end) should be binsearch(mid + 1, end)",
)


@KNOWN_BUG
@pytest.mark.parametrize(
    "arr, x",
    [
        ([1], 2),
        ([1, 2, 3], 4),
        ([1, 3], 2),
        ([1, 3, 5, 7], 6),
    ],
)
def test_missing_element_to_the_right_returns_minus_one(arr, x):
    assert find_in_sorted(arr, x) == -1
