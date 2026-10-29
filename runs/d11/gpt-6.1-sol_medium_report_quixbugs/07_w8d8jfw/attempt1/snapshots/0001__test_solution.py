"""Tests for kth's documented sorted(arr)[k] behavior on valid inputs."""

from itertools import product

import pytest

from solution import kth


@pytest.mark.parametrize(
    "arr, k, expected",
    [
        pytest.param([42], 0, 42, id="singleton"),
        pytest.param([2, 1], 0, 1, id="two-elements-minimum"),
        pytest.param([2, 1], 1, 2, id="two-elements-maximum"),
        pytest.param([4, 2, 5, 1, 3], 0, 1, id="recurse-below-pivot"),
        pytest.param([2, 4, 5, 1, 3], 4, 5, id="recurse-above-pivot"),
        pytest.param([3, 5, 1, 4, 2], 2, 3, id="return-pivot"),
        pytest.param([3, 1, 3, 2, 3, 4], 1, 2, id="before-duplicate-pivots"),
        pytest.param([3, 1, 3, 2, 3, 4], 2, 3, id="first-duplicate-pivot"),
        pytest.param([3, 1, 3, 2, 3, 4], 4, 3, id="last-duplicate-pivot"),
        pytest.param([3, 1, 3, 2, 3, 4], 5, 4, id="after-duplicate-pivots"),
        pytest.param([-3, -1, -5, -2], 1, -3, id="negative-integers"),
        pytest.param([0, -4, 8, -1, 0], 2, 0, id="mixed-signs-and-zero"),
        pytest.param([10**100, 0, -(10**100)], 0, -(10**100), id="large-negative"),
        pytest.param([10**100, 0, -(10**100)], 2, 10**100, id="large-positive"),
    ],
)
def test_kth_examples(arr, k, expected):
    assert kth(arr, k) == expected


@pytest.mark.parametrize(
    "arr",
    [
        pytest.param(list(range(30)), id="ascending"),
        pytest.param(list(range(29, -1, -1)), id="descending"),
        pytest.param([7] * 30, id="all-equal"),
        pytest.param([9, 1, 8, 2, 7, 3, 6, 4, 5, 0], id="alternating"),
        pytest.param([5, 2, 5, 1, 2, 5, 3, 1, 3, 5], id="duplicate-groups"),
    ],
)
def test_kth_matches_sorted_for_every_valid_rank(arr):
    expected = sorted(arr)
    for k, value in enumerate(expected):
        assert kth(arr, k) == value, f"arr={arr!r}, k={k}"


@pytest.mark.parametrize("length", range(1, 6))
def test_kth_exhaustive_small_lists(length):
    """Exercise every ordering and duplicate pattern over a small integer set."""
    for values in product((-1, 0, 1), repeat=length):
        arr = list(values)
        for k, expected in enumerate(sorted(arr)):
            assert kth(arr, k) == expected, f"arr={arr!r}, k={k}"
