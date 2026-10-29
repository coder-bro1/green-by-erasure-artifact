"""Tests for solution.mergesort.

KNOWN BUG in solution.py: the recursion's base case is ``len(arr) == 0`` only.
For a one-element list, ``middle == 0`` so ``arr[middle:]`` is the same
one-element list, and mergesort recurses forever (RecursionError). Since every
non-empty input eventually reaches a one-element sublist, *all* non-empty
inputs fail. The fix is ``if len(arr) <= 1: return arr``.

solution.py must not be modified, so the specification tests for non-empty
inputs are marked ``xfail(strict=True, raises=RecursionError)``. They document
the intended behaviour; once the bug is fixed they will XPASS, and strict mode
turns that into a failure, prompting removal of the marker.
"""
import random

import pytest

from solution import mergesort

known_bug = pytest.mark.xfail(
    strict=True,
    raises=RecursionError,
    reason="base case is len(arr)==0; single-element lists recurse forever",
)


# --- Behaviour that works today -------------------------------------------

def test_empty_list_returns_empty():
    assert mergesort([]) == []


def test_empty_list_returns_list_type():
    assert isinstance(mergesort([]), list)


@pytest.mark.parametrize("arr", [[1], [2, 1], [3, 1, 2]])
def test_nonempty_input_currently_raises_recursion_error(arr):
    """Pins the current (buggy) behaviour so a change is noticed."""
    with pytest.raises(RecursionError):
        mergesort(arr)


# --- Specification tests (blocked by the known bug) -----------------------

@known_bug
def test_single_element():
    assert mergesort([5]) == [5]


@known_bug
@pytest.mark.parametrize(
    "arr, expected",
    [
        ([2, 1], [1, 2]),
        ([1, 2], [1, 2]),
        ([3, 1, 2], [1, 2, 3]),
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        ([4, 1, 3, 1, 2, 4], [1, 1, 2, 3, 4, 4]),
        ([7, 7, 7], [7, 7, 7]),
        ([0, -1, 5, -10, 3], [-10, -1, 0, 3, 5]),
        ([10**18, -(10**18), 0], [-(10**18), 0, 10**18]),
    ],
)
def test_sorts_correctly(arr, expected):
    assert mergesort(arr) == expected


@known_bug
def test_does_not_mutate_input():
    arr = [3, 1, 2]
    original = list(arr)
    mergesort(arr)
    assert arr == original


@known_bug
@pytest.mark.parametrize("seed", range(5))
def test_matches_sorted_on_random_input(seed):
    rng = random.Random(seed)
    arr = [rng.randint(-100, 100) for _ in range(rng.randint(1, 200))]
    assert mergesort(arr) == sorted(arr)


@known_bug
def test_is_stable():
    """Equal keys keep their original relative order (merge uses <=)."""

    class Item:
        def __init__(self, key, tag):
            self.key, self.tag = key, tag

        def __le__(self, other):
            return self.key <= other.key

    items = [Item(2, "a"), Item(1, "b"), Item(2, "c"), Item(1, "d")]
    result = mergesort(items)
    assert [(i.key, i.tag) for i in result] == [
        (1, "b"), (1, "d"), (2, "a"), (2, "c"),
    ]
