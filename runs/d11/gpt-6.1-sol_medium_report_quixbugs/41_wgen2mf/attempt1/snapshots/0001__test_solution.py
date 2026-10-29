"""Tests for the documented bucketsort input domain and output."""

from itertools import product

import pytest

from solution import bucketsort


@pytest.mark.parametrize(
    ("arr", "k", "expected"),
    [
        pytest.param([], 0, [], id="empty-zero-bound"),
        pytest.param([], 5, [], id="empty-positive-bound"),
        pytest.param([0], 1, [0], id="single-zero"),
        pytest.param([4], 5, [4], id="single-upper-bound-minus-one"),
        pytest.param([0, 0, 0], 1, [0, 0, 0], id="all-zeros"),
        pytest.param([3, 3, 3], 4, [3, 3, 3], id="all-equal"),
        pytest.param([0, 1, 2, 3], 4, [0, 1, 2, 3], id="already-sorted"),
        pytest.param([3, 2, 1, 0], 4, [0, 1, 2, 3], id="reverse-sorted"),
        pytest.param([2, 0, 2, 1, 0], 3, [0, 0, 1, 2, 2], id="duplicates"),
        pytest.param([9, 0, 9, 0], 10, [0, 0, 9, 9], id="both-boundaries"),
        pytest.param([7, 2, 7, 4], 20, [2, 4, 7, 7], id="unused-buckets"),
        pytest.param([99, 1, 50, 0], 100, [0, 1, 50, 99], id="larger-bound"),
    ],
)
def test_bucketsort_documented_examples(arr, k, expected):
    assert bucketsort(arr, k) == expected


@pytest.mark.parametrize("k", range(1, 6))
def test_bucketsort_exhaustive_small_inputs(k):
    """Compare every short valid input with Python's sorting oracle."""
    for length in range(5):
        for values in product(range(k), repeat=length):
            arr = list(values)
            assert bucketsort(arr, k) == sorted(arr), (arr, k)


def test_bucketsort_independent_calls():
    assert bucketsort([2, 0, 2], 3) == [0, 2, 2]
    assert bucketsort([1, 0], 2) == [0, 1]
    assert bucketsort([], 3) == []
