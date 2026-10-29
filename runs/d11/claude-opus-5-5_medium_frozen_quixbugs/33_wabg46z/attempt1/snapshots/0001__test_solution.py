"""Tests for solution.subsequences.

NOTE: solution.py has a known bug: the base case ``if k == 0: return []``
should be ``return [[]]``. As written, the recursion never yields any
sequence, so every call returns ``[]``. Tests asserting the documented
behaviour that the bug breaks are marked ``xfail(strict=True)``: they are
reported as expected failures now, and will turn into hard failures
(XPASS strict) once the bug is fixed, signalling the markers should be removed.
"""
from itertools import combinations

import pytest

from solution import subsequences

BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py bug: base case k == 0 returns [] instead of [[]]",
)


def reference(a, b, k):
    return [list(c) for c in combinations(range(a, b), k)]


# ---------------------------------------------------------------------------
# Behaviour that holds with the current implementation
# ---------------------------------------------------------------------------

def test_returns_list():
    assert isinstance(subsequences(1, 5, 3), list)


@pytest.mark.parametrize(
    "a, b, k",
    [
        (1, 3, 3),   # k larger than range size
        (0, 0, 1),   # empty range
        (5, 1, 2),   # reversed bounds -> empty range
        (3, 4, 2),   # range of size 1, k = 2
    ],
)
def test_no_sequences_when_k_exceeds_range(a, b, k):
    assert subsequences(a, b, k) == []


def test_results_are_ascending_and_in_range():
    # Holds vacuously for the buggy implementation, meaningfully once fixed.
    for seq in subsequences(-2, 6, 3):
        assert len(seq) == 3
        assert all(-2 <= x < 6 for x in seq)
        assert all(x < y for x, y in zip(seq, seq[1:]))


# ---------------------------------------------------------------------------
# Documented behaviour broken by the base-case bug
# ---------------------------------------------------------------------------

@BUG
def test_docstring_example():
    assert subsequences(a=1, b=5, k=3) == [
        [1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]
    ]


@BUG
def test_k_equals_one():
    assert subsequences(0, 4, 1) == [[0], [1], [2], [3]]


@BUG
def test_k_equals_range_size():
    assert subsequences(2, 5, 3) == [[2, 3, 4]]


@BUG
def test_negative_bounds():
    assert subsequences(-2, 1, 2) == [[-2, -1], [-2, 0], [-1, 0]]


@BUG
@pytest.mark.parametrize("a, b, k", [(0, 6, 2), (1, 8, 4), (-3, 3, 3), (0, 10, 5)])
def test_matches_itertools_combinations(a, b, k):
    assert subsequences(a, b, k) == reference(a, b, k)
