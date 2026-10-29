"""Tests for the documented monotonic-list predicate."""

from itertools import product

import pytest

from solution import monotonic


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([1, 2, 4, 20], True, id="docstring-increasing"),
        pytest.param([1, 20, 4, 10], False, id="docstring-mixed"),
        pytest.param([4, 1, 0, -10], True, id="docstring-decreasing"),
        pytest.param([], True, id="empty"),
        pytest.param([7], True, id="singleton"),
        pytest.param([1, 2], True, id="pair-increasing"),
        pytest.param([2, 1], True, id="pair-decreasing"),
        pytest.param([2, 2], True, id="pair-equal"),
        pytest.param([3, 3, 3, 3], True, id="constant"),
        pytest.param([1, 1, 2, 2, 3, 3], True, id="nondecreasing"),
        pytest.param([3, 3, 2, 2, 1, 1], True, id="nonincreasing"),
        pytest.param([-9, -5, -1], True, id="negative-increasing"),
        pytest.param([-1, -5, -9], True, id="negative-decreasing"),
        pytest.param([-3, 0, 4], True, id="crosses-zero"),
        pytest.param([0.25, 0.5, 1.75], True, id="float-increasing"),
        pytest.param([1.75, 0.5, 0.25], True, id="float-decreasing"),
        pytest.param([1, 3, 2], False, id="peak"),
        pytest.param([3, 1, 2], False, id="valley"),
        pytest.param([1, 2, 1, 2], False, id="alternating"),
        pytest.param([1, 1, 2, 1], False, id="plateau-then-reversal"),
        pytest.param([1, 2, 3, 2], False, id="last-element-reversal"),
        pytest.param([2, 1, 2, 3], False, id="first-element-reversal"),
    ],
)
def test_monotonic_examples_and_edge_cases(values, expected):
    assert monotonic(values) is expected


def test_monotonic_exhaustive_short_integer_lists():
    """Check both monotonic directions using adjacent comparisons."""
    for length in range(7):
        for sequence in product((-1, 0, 1), repeat=length):
            values = list(sequence)
            pairs = list(zip(values, values[1:]))
            expected = all(a <= b for a, b in pairs) or all(
                a >= b for a, b in pairs
            )
            assert monotonic(values) is expected, f"Unexpected result for {values!r}"
