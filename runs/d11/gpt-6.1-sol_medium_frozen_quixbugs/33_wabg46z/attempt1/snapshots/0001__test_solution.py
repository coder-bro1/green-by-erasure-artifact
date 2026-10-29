"""Tests for the documented subsequences contract.

Nonempty results currently fail because the recursion has no successful base
case. Strict xfail records that defect without changing solution.py; fixing it
will produce XPASS failures until the marks are removed.
"""

from itertools import combinations

import pytest

from solution import subsequences


NONEMPTY_RESULT_BUG = pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="The k=0 base case returns [] instead of [[]], discarding every sequence",
)


@NONEMPTY_RESULT_BUG
def test_documented_example():
    assert subsequences(a=1, b=5, k=3) == [
        [1, 2, 3],
        [1, 2, 4],
        [1, 3, 4],
        [2, 3, 4],
    ]


@NONEMPTY_RESULT_BUG
@pytest.mark.parametrize(
    "a,b,k",
    [
        pytest.param(1, 5, 1, id="singletons-and-exclusive-upper-bound"),
        pytest.param(1, 5, 2, id="pairs-in-lexicographic-order"),
        pytest.param(1, 5, 4, id="entire-range"),
        pytest.param(7, 8, 1, id="one-element-range"),
        pytest.param(-5, -1, 2, id="negative-integers"),
        pytest.param(-2, 3, 3, id="range-crossing-zero"),
        pytest.param(0, 6, 3, id="multiple-recursion-levels"),
    ],
)
def test_nonempty_results_match_combinations(a, b, k):
    expected = [list(sequence) for sequence in combinations(range(a, b), k)]
    assert subsequences(a, b, k) == expected


@pytest.mark.parametrize(
    "a,b,k",
    [
        pytest.param(0, 0, 1, id="empty-range"),
        pytest.param(-3, -3, 2, id="empty-negative-range"),
        pytest.param(5, 1, 1, id="reversed-range"),
        pytest.param(2, -2, 3, id="reversed-range-crossing-zero"),
        pytest.param(1, 5, 5, id="length-one-too-large"),
        pytest.param(7, 8, 2, id="singleton-range-length-too-large"),
        pytest.param(-2, 2, 10, id="length-much-too-large"),
    ],
)
def test_no_possible_subsequences(a, b, k):
    assert subsequences(a, b, k) == []


@pytest.mark.parametrize("a,b", [(1, 5), (0, 0), (5, 1), (-3, 3)])
def test_zero_length_returns_empty_list(a, b):
    # k=0 is outside the documented positive-k input domain, but the function
    # explicitly defines this behavior.
    assert subsequences(a, b, 0) == []
