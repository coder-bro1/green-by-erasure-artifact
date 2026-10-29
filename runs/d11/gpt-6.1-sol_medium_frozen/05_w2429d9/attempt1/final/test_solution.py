"""Regression tests for the current implementation of ``fibfib``.

The implementation uses seeds (0, 1, 2), whereas its docstring specifies
(0, 0, 1). These tests preserve the implemented behavior without changing
solution.py.
"""

import pytest

from solution import fibfib


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 6),
        (5, 11),
        (6, 20),
        (7, 37),
        (8, 68),
        (9, 125),
        (10, 230),
        (11, 423),
        (12, 778),
        (13, 1431),
        (14, 2632),
        (15, 4841),
    ],
)
def test_fibfib_sequence(n, expected):
    """Check each base case and known terms of the implemented sequence."""
    assert fibfib(n) == expected


def test_fibfib_repeated_calls_in_different_orders():
    """Results remain consistent across repeated, interleaved calls."""
    indices = [8, 0, 5, 2, 8, 1, 5, 0]
    assert [fibfib(n) for n in indices] == [68, 0, 11, 2, 68, 1, 11, 0]
