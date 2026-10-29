"""Tests for the maximum contiguous sublist sum, including empty sublists."""

from itertools import product

import pytest

from solution import max_sublist_sum


@pytest.mark.parametrize(
    ("arr", "expected"),
    [
        pytest.param([], 0, id="empty-list"),
        pytest.param([7], 7, id="positive-singleton"),
        pytest.param([-7], 0, id="negative-singleton"),
        pytest.param([0], 0, id="zero-singleton"),
        pytest.param([-8, -1, -4], 0, id="all-negative-empty-sublist-wins"),
        pytest.param([0, 0, 0], 0, id="all-zero"),
        pytest.param([1, 2, 3, 4], 10, id="whole-list"),
        pytest.param([4, -5, 2, 1, -1, 3], 5, id="docstring-example"),
        pytest.param([5, 3, -20, 1], 8, id="best-prefix"),
        pytest.param([-20, 2, -1, 4], 5, id="best-suffix"),
        pytest.param([-10, 3, 4, -20], 7, id="best-interior"),
        pytest.param([5, -2, 4], 7, id="bridge-negative-value"),
        pytest.param([5, -10, 6], 6, id="restart-after-negative-total"),
        pytest.param([5, -100, 6], 6, id="must-be-contiguous"),
        pytest.param([3, -3, 3], 3, id="tied-maxima"),
        pytest.param([0, 3, 0, -1, 0, 2, 0], 4, id="mixed-with-zeros"),
        pytest.param([10**100, -1, 10**100], 2 * 10**100 - 1,
                     id="arbitrary-precision-integers"),
    ],
)
def test_max_sublist_sum_examples(arr, expected):
    assert max_sublist_sum(arr) == expected


def test_max_sublist_sum_matches_documented_definition_exhaustively():
    """Compare every short list against direct enumeration of its sublists."""
    for length in range(6):
        for values in product(range(-2, 3), repeat=length):
            arr = list(values)
            expected = max(
                sum(arr[start:end])
                for start in range(length + 1)
                for end in range(start, length + 1)
            )
            assert max_sublist_sum(arr) == expected, f"arr={arr!r}"


def test_max_sublist_sum_preserves_input():
    arr = [4, -5, 2, 1, -1, 3]
    original = arr.copy()

    assert max_sublist_sum(arr) == 5
    assert arr == original
