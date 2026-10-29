"""Tests for solution.pascal.

NOTE: solution.py contains a known off-by-one bug (the inner loop is
``range(0, r)`` instead of ``range(0, r + 1)``), so every row after the first
is one element short. Consequently:
  * pascal(1) is correct,
  * pascal(2) returns [[1], [1]] instead of [[1], [1, 1]],
  * pascal(n) for n >= 3 raises IndexError.

Tests that check the documented specification are marked
``xfail(strict=True)`` with the bug as the reason, so the suite passes against
the current code and will start failing loudly (XPASS -> failure) once the bug
is fixed, signalling that the markers should be removed. The "current
behaviour" tests pin down exactly how the bug manifests.
"""
from math import comb

import pytest

from solution import pascal

BUG = "solution.py off-by-one: inner loop uses range(0, r) instead of range(0, r + 1)"


def expected(n):
    return [[comb(r, c) for c in range(r + 1)] for r in range(n)]


# --- Behaviour that is correct today -------------------------------------

def test_single_row():
    assert pascal(1) == [[1]]


def test_returns_list_of_lists():
    result = pascal(1)
    assert isinstance(result, list)
    assert all(isinstance(row, list) for row in result)


def test_fresh_result_each_call():
    a = pascal(1)
    a[0].append(99)
    assert pascal(1) == [[1]]


# --- Documented specification (blocked by the bug) -----------------------

@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_example():
    assert pascal(5) == [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]


@pytest.mark.xfail(strict=True, reason=BUG)
def test_two_rows():
    assert pascal(2) == [[1], [1, 1]]


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize("n", [2, 3, 4, 6, 10, 15])
def test_matches_binomial_coefficients(n):
    assert pascal(n) == expected(n)


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize("n", [2, 5, 12])
def test_row_lengths(n):
    assert [len(row) for row in pascal(n)] == list(range(1, n + 1))


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize("n", [3, 8])
def test_rows_are_symmetric_and_sum_to_power_of_two(n):
    for r, row in enumerate(pascal(n)):
        assert row == row[::-1]
        assert sum(row) == 2 ** r


# --- Current (buggy) behaviour, pinned so regressions are visible --------

def test_current_two_rows_missing_trailing_one():
    assert pascal(2) == [[1], [1]]


@pytest.mark.parametrize("n", [3, 4, 5, 10])
def test_current_three_or_more_rows_raises(n):
    with pytest.raises(IndexError):
        pascal(n)
