"""Tests for the FibFib sequence specified in solution.py's docstring."""

import doctest

import pytest

import solution
from solution import fibfib


@pytest.mark.parametrize("n, expected", [(0, 0), (1, 0), (2, 1)])
def test_initial_values(n, expected):
    assert fibfib(n) == expected


@pytest.mark.parametrize(
    "n, expected",
    [(3, 1), (4, 2), (5, 4), (6, 7), (7, 13), (8, 24),
     (9, 44), (10, 81), (11, 149), (12, 274), (15, 1705)],
)
def test_known_sequence_values(n, expected):
    assert fibfib(n) == expected


@pytest.mark.parametrize("n", range(3, 16))
def test_three_term_recurrence(n):
    assert fibfib(n) == fibfib(n - 1) + fibfib(n - 2) + fibfib(n - 3)


def test_docstring_examples():
    result = doctest.testmod(solution)
    assert result.attempted == 3
    assert result.failed == 0


def test_large_index():
    # A linear reference calculation keeps the expected value independent of
    # the implementation and exercises the promise of efficient computation.
    n = 10_000
    a, b, c = 0, 0, 1
    for _ in range(n):
        a, b, c = b, c, a + b + c
    assert fibfib(n) == a
