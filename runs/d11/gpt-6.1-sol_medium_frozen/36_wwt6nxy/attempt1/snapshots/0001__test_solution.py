"""Regression tests for the current behavior of solution.derivative.

The implementation retains a leading zero, unlike the docstring examples.
These tests explicitly capture that behavior without changing solution.py.
"""

import pytest

from solution import derivative


@pytest.mark.parametrize(
    ("coefficients", "expected"),
    [
        pytest.param([], [], id="empty-polynomial"),
        pytest.param([7], [0], id="constant"),
        pytest.param([0], [0], id="zero-constant"),
        pytest.param([3, 1], [0, 1], id="linear"),
        pytest.param([3, 1, 2, 4, 5], [0, 1, 4, 12, 20], id="first-docstring-input"),
        pytest.param([1, 2, 3], [0, 2, 6], id="second-docstring-input"),
        pytest.param([-9, -2, -3, -4], [0, -2, -6, -12], id="negative-coefficients"),
        pytest.param([5, 0, 0, 2], [0, 0, 0, 6], id="missing-middle-terms"),
        pytest.param([1, 2, 0, 0], [0, 2, 0, 0], id="trailing-zero-terms"),
        pytest.param([0.5, 1.5, -2.25], [0.0, 1.5, -4.5], id="fractional-coefficients"),
    ],
)
def test_derivative_current_coefficient_representation(coefficients, expected):
    assert derivative(coefficients) == expected


def test_derivative_does_not_mutate_input():
    coefficients = [3, 1, 2, 4, 5]
    original = coefficients.copy()

    result = derivative(coefficients)

    assert coefficients == original
    assert result is not coefficients
    result.append(99)
    assert coefficients == original


def test_derivative_returns_independent_lists_on_repeated_calls():
    coefficients = [1, 2, 3]

    first = derivative(coefficients)
    second = derivative(coefficients)
    first[1] = 99

    assert second == [0, 2, 6]


def test_derivative_handles_large_integer_coefficients_exactly():
    large = 10**100

    assert derivative([large, -large, large]) == [0, -large, 2 * large]
