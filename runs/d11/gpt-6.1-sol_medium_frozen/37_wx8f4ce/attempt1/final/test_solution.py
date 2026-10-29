"""Tests for the current behavior of solution.add."""

import pytest

from solution import add


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([4, 2, 6, 7], 8, id="docstring-input-current-result"),
        pytest.param([2], 0, id="single-even-value-is-excluded"),
        pytest.param([3], 0, id="single-odd-value"),
        pytest.param([100, 2, 3], 2, id="first-value-is-excluded"),
        pytest.param([1, 3, 5, 7], 0, id="all-odd-values"),
        pytest.param([1, 2, 4, 6, 8], 20, id="all-later-even-values"),
        pytest.param([1, 3, 8, 5], 8, id="even-value-at-even-index-is-included"),
        pytest.param([1, 2, 3, 4], 6, id="even-values-at-odd-indices"),
        pytest.param([2, 0, 1, 0], 0, id="zero-values"),
        pytest.param([-100, -2, -4, -3], -6, id="negative-even-values"),
        pytest.param([7, -6, 2, 4, -5], 0, id="positive-negative-cancellation"),
        pytest.param([9, 2, 2, 2], 6, id="duplicate-values-counted"),
        pytest.param([0, 10**100, -(10**100) + 2, 3], 2, id="large-integers"),
    ],
)
def test_add_sums_even_values_after_first_index(values, expected):
    assert add(values) == expected


def test_add_does_not_modify_input():
    values = [10, -2, 4, 3, 0]
    original = values.copy()

    assert add(values) == 2
    assert values == original
