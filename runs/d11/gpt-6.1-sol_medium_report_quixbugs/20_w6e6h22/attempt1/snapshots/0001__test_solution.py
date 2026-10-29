"""Tests for the integer-list sorting contract in solution.py."""

import random
from itertools import product

import pytest

from solution import mergesort


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([], [], id="empty"),
        pytest.param([7], [7], id="singleton"),
        pytest.param([2, 1], [1, 2], id="reversed-pair"),
        pytest.param([1, 2], [1, 2], id="sorted-pair"),
        pytest.param([3, 1, 2], [1, 2, 3], id="odd-length"),
        pytest.param([4, 2, 3, 1], [1, 2, 3, 4], id="even-length"),
        pytest.param([-1, -5, -2], [-5, -2, -1], id="negative"),
        pytest.param([0, -2, 4, -1, 0], [-2, -1, 0, 0, 4], id="mixed-signs"),
        pytest.param([3, 1, 3, 2, 1], [1, 1, 2, 3, 3], id="duplicates"),
        pytest.param([5] * 9, [5] * 9, id="all-equal"),
        pytest.param(list(range(12)), list(range(12)), id="already-sorted"),
        pytest.param(list(range(12, 0, -1)), list(range(1, 13)), id="reverse-sorted"),
        pytest.param([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], id="left-exhausted"),
        pytest.param([4, 5, 6, 1, 2, 3], [1, 2, 3, 4, 5, 6], id="right-exhausted"),
        pytest.param([10**100, 0, -(10**100)], [-(10**100), 0, 10**100], id="large-integers"),
    ],
)
def test_mergesort_examples(values, expected):
    assert mergesort(values) == expected


def test_mergesort_exhaustive_short_lists():
    """Check every ordering of small lists, including repeated values."""
    for length in range(7):
        for values in product((-1, 0, 1), repeat=length):
            values = list(values)
            assert mergesort(values) == sorted(values), f"input={values!r}"


@pytest.mark.parametrize("length", [7, 16, 31, 64, 127, 256, 1000])
def test_mergesort_seeded_random_lists(length):
    rng = random.Random(length)
    values = [rng.randint(-100, 100) for _ in range(length)]
    assert mergesort(values) == sorted(values)
