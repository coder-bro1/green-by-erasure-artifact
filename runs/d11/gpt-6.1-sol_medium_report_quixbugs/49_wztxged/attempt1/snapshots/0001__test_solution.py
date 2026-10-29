"""Tests for the documented lexicographic successor of unique integers.

All inputs satisfy the precondition: none is sorted in reverse order.
"""

import pytest

from solution import next_permutation


@pytest.mark.parametrize(
    ("perm", "expected"),
    [
        pytest.param([1, 2], [2, 1], id="two-elements"),
        pytest.param([1, 2, 3], [1, 3, 2], id="ascending"),
        pytest.param([2, 1, 3], [2, 3, 1], id="final-pair"),
        pytest.param([1, 3, 2], [2, 1, 3], id="descending-suffix"),
        pytest.param([1, 4, 3, 2], [2, 1, 3, 4], id="long-suffix"),
        pytest.param([4, 1, 3, 2], [4, 2, 1, 3], id="preserve-prefix"),
        pytest.param([-3, -1, -2], [-2, -3, -1], id="negative-integers"),
        pytest.param([0, 20, 10], [10, 0, 20], id="nonconsecutive-integers"),
    ],
)
def test_next_permutation_returns_successor(perm, expected):
    assert next_permutation(perm) == expected


@pytest.mark.parametrize(
    ("perm", "expected"),
    [
        pytest.param([3, 2, 4, 1], [3, 4, 1, 2], id="docstring-example"),
        pytest.param([2, 3, 1], [3, 1, 2], id="leftmost-pivot"),
        pytest.param([1, 3, 4, 2], [1, 4, 2, 3], id="interior-pivot"),
        pytest.param([0, -1, 2, -3], [0, 2, -3, -1], id="mixed-signs"),
    ],
)
def test_next_permutation_increases_lexicographic_order(perm, expected):
    assert next_permutation(perm) == expected
