"""Tests for kth's documented equivalence to sorted(arr)[k]."""

import pytest

from solution import kth


@pytest.mark.parametrize(
    "arr, k, expected",
    [
        pytest.param([0], 0, 0, id="single-zero"),
        pytest.param([-17], 0, -17, id="single-negative"),
        pytest.param([10**100], 0, 10**100, id="single-large-integer"),
        pytest.param([2, 1], 0, 1, id="two-elements-minimum"),
        pytest.param([2, 1], 1, 2, id="two-elements-maximum"),
        pytest.param([3, 1, 2], 0, 1, id="unsorted-minimum"),
        pytest.param([3, 1, 2], 2, 3, id="unsorted-maximum"),
        pytest.param([2, 3, 1], 1, 2, id="pivot-middle-rank"),
        pytest.param([3, 1, 2, 4, 5], 2, 3, id="pivot-with-both-partitions"),
        pytest.param([2, 2, 1, 3], 1, 2, id="duplicate-pivot-first-rank"),
        pytest.param([2, 2, 1, 3], 2, 2, id="duplicate-pivot-last-rank"),
        pytest.param([0, -3, 2, -1, 0], 2, 0, id="mixed-signs-first-zero"),
        pytest.param([0, -3, 2, -1, 0], 3, 0, id="mixed-signs-second-zero"),
    ],
)
def test_kth_documented_examples(arr, k, expected):
    assert kth(arr, k) == expected


@pytest.mark.parametrize(
    "arr",
    [
        pytest.param([5, 4, 3, 2, 1], id="descending"),
        pytest.param([9, 9, 4, 4, 4, 0, -2, -2], id="descending-duplicates"),
        pytest.param([-1, -4, -9, -20], id="negative-integers"),
        pytest.param([10**100, 1, 0, -(10**100)], id="large-integers"),
        pytest.param([5, 5, 5, 5], id="all-equal"),
        pytest.param([0, 0, 0], id="all-zero"),
    ],
)
def test_kth_every_valid_rank(arr):
    for k, expected in enumerate(sorted(arr)):
        assert kth(arr, k) == expected, f"Incorrect result for rank {k}"


@pytest.mark.xfail(
    strict=True,
    reason=(
        "kth recurses into the upper partition without subtracting the number "
        "of elements <= the pivot from k; this violates sorted(arr)[k]."
    ),
)
@pytest.mark.parametrize(
    "arr, k, expected",
    [
        pytest.param([1, 2], 1, 2, id="upper-partition-index-error"),
        pytest.param([1, 2, 3, 4], 2, 3, id="ascending-middle-rank"),
        pytest.param([2, 3, 1], 2, 3, id="unsorted-maximum"),
        pytest.param([3, 1, 2], 1, 2, id="upper-partition-in-nested-call"),
        pytest.param([4, 1, 3, 2], 1, 2, id="returns-wrong-value"),
        pytest.param([4, 1, 3, 2], 2, 3, id="nested-index-error"),
        pytest.param([2, 2, 1, 3], 3, 3, id="duplicate-pivot-offset"),
        pytest.param([0, -3, 2, -1, 0], 1, -1, id="negative-upper-partition"),
        pytest.param([0, -3, 2, -1, 0], 4, 2, id="mixed-signs-maximum"),
    ],
)
def test_kth_upper_partition_matches_documented_rank(arr, k, expected):
    assert kth(arr, k) == expected
