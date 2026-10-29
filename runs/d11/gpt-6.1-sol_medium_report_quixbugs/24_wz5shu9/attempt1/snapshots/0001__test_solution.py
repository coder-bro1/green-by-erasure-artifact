from itertools import combinations, permutations

import pytest

from solution import lis


@pytest.mark.parametrize(
    ("arr", "expected"),
    [
        pytest.param([], 0, id="empty"),
        pytest.param([42], 1, id="single-element"),
        pytest.param([1, 2, 3, 4, 5], 5, id="increasing"),
        pytest.param([5, 4, 3, 2, 1], 1, id="decreasing"),
        pytest.param([4, 1, 5, 3, 7, 6, 2], 3, id="docstring-example"),
        pytest.param([3, 1, 2], 2, id="replace-initial-tail"),
        pytest.param([1, 5, 2, 3, 4], 4, id="skip-large-interior-value"),
        pytest.param([2, 3, 4, 1], 3, id="best-subsequence-ends-early"),
        pytest.param([1, 3, 5, 2, 4, 6], 4, id="subsequence-not-contiguous"),
        pytest.param([-5, -1, -4, -3, -2], 4, id="negative-values"),
        pytest.param([-2, 0, -1, 1], 3, id="mixed-signs"),
        pytest.param([10**100, -(10**100), 0, 10**99], 3, id="large-integers"),
        pytest.param((), 0, id="empty-tuple"),
        pytest.param((4, 1, 5, 3, 7, 6, 2), 3, id="tuple-sequence"),
        pytest.param(range(-3, 4), 7, id="range-sequence"),
    ],
)
def test_lis_documented_behavior(arr, expected):
    assert lis(arr) == expected


def test_lis_preserves_input():
    arr = [4, 1, 5, 3, 7, 6, 2]
    original = arr.copy()

    lis(arr)

    assert arr == original


def brute_force_lis(arr):
    """Find the answer independently by enumerating every subsequence."""
    for length in range(len(arr), 0, -1):
        for subsequence in combinations(arr, length):
            if all(a < b for a, b in zip(subsequence, subsequence[1:])):
                return length
    return 0


@pytest.mark.parametrize("size", range(7))
def test_lis_matches_brute_force_for_every_small_permutation(size):
    # All inputs meet the documented precondition that integers are unique.
    for arr in permutations(range(size)):
        assert lis(arr) == brute_force_lis(arr), f"Incorrect LIS for {arr!r}"
