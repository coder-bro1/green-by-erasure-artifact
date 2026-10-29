"""Tests for LIS with unique integer inputs, as required by its contract."""

from itertools import combinations

import pytest

from solution import lis


def brute_force_lis(values):
    """Independent oracle: enumerate subsequences from longest to shortest."""
    for length in range(len(values), 0, -1):
        for subsequence in combinations(values, length):
            if all(a < b for a, b in zip(subsequence, subsequence[1:])):
                return length
    return 0


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([], 0, id="empty"),
        pytest.param([7], 1, id="singleton"),
        pytest.param([1, 2], 2, id="increasing-pair"),
        pytest.param([2, 1], 1, id="decreasing-pair"),
        pytest.param([1, 2, 3, 4, 5], 5, id="increasing"),
        pytest.param([5, 4, 3, 2, 1], 1, id="decreasing"),
        pytest.param([3, 1, 2], 2, id="skip-leading-maximum"),
        pytest.param([1, 3, 2, 4], 3, id="noncontiguous-subsequence"),
        pytest.param([-4, -2, -3, -1], 3, id="negative-values"),
        pytest.param([-2, 0, -1, 3], 3, id="mixed-signs"),
        pytest.param([10, 9, 2, 5, 3, 7, 101, 18], 4, id="mixed-order"),
        pytest.param([-(10**100), 0, 10**100], 3, id="large-integers"),
    ],
)
def test_lis_length(values, expected):
    assert lis(values) == expected


@pytest.mark.parametrize("length", [0, 1, 2, 10, 100])
def test_monotonic_sequences(length):
    values = list(range(length))
    assert lis(values) == length
    assert lis(values[::-1]) == min(length, 1)


@pytest.mark.parametrize("values", [[], [7], [3, 1, 2], [-4, -2, -3, -1]])
def test_accepts_tuple_sequences(values):
    assert lis(tuple(values)) == brute_force_lis(values)


def test_does_not_modify_input_and_is_repeatable():
    values = [10, 9, 2, 5, 3, 7, 101, 18]
    original = values.copy()
    expected = brute_force_lis(values)
    assert lis(values) == expected
    assert values == original
    assert lis([3, 2, 1]) == 1
    assert lis(values) == expected
    assert values == original


@pytest.mark.xfail(
    strict=True,
    reason="lis overwrites longest when replacing a shorter subsequence tail",
)
@pytest.mark.parametrize(
    "values",
    [
        pytest.param([4, 1, 5, 3, 7, 6, 2], id="docstring-example"),
        pytest.param([1, 2, 0], id="minimal-regression"),
        pytest.param([1, 2, 3, 0], id="trailing-minimum"),
        pytest.param([1, 2, 0, 3], id="extension-after-reset"),
        pytest.param([2, 3, 1, 4], id="replacement-before-extension"),
    ],
)
def test_preserves_earlier_longest_subsequence(values):
    assert lis(values) == brute_force_lis(values)
