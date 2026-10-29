"""Regression tests for the current implementation.

The return values in solution.py are inverted relative to its docstring.
These tests preserve the implemented behavior without changing solution.py.
"""

import pytest

from solution import is_one_direction


@pytest.mark.parametrize(
    "seq",
    [
        [],
        [7],
        [2, 2, 2],
        [1, 2, 3],
        [3, 2, 1],
        [1, 1, 3],
        [5, 2, 2, 0],
        [-5, -3, -1, 0],
        [0, -1, -3, -5],
        [0.5, 0.5, 1.25],
        ["a", "b", "c"],
    ],
)
def test_returns_false_for_monotonic_sequences(seq):
    assert is_one_direction(seq) is False


@pytest.mark.parametrize(
    "seq",
    [
        [2, 9, 4],
        [3, 1, 2],
        [1, 2, 1, 2],
        [1, 1, 3, 3, 2, 2],
        [-3, 0, -1],
        [0.5, 1.25, 0.75],
        ["a", "c", "b"],
    ],
)
def test_returns_true_when_direction_changes(seq):
    assert is_one_direction(seq) is True


@pytest.mark.parametrize("seq", [[1, 1, 3], [5, 2, 2, 0], [2, 9, 4]])
def test_does_not_modify_input(seq):
    original = seq.copy()

    is_one_direction(seq)

    assert seq == original
