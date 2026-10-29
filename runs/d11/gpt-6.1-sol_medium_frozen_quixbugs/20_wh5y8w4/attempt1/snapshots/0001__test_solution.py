"""Tests for terminating inputs within sqrt's documented preconditions.

The current stopping condition can loop forever for tighter tolerances,
including the docstring's sqrt(2, 0.01) example. These cases intentionally
use tolerances for which the existing implementation terminates.
"""

import math

import pytest

from solution import sqrt


@pytest.mark.parametrize("epsilon", [1e-12, 1e-6, 0.01, 0.1])
def test_lower_input_boundary_converges(epsilon):
    result = sqrt(1.0, epsilon)

    assert isinstance(result, float)
    assert abs(result - 1.0) <= epsilon


@pytest.mark.parametrize(
    ("x", "epsilon"),
    [(1.0, 0.5), (2.0, 1.0), (4.0, 2.0), (9.0, 4.5), (100.0, 50.0)],
)
def test_initial_estimate_is_returned_at_stopping_boundary(x, epsilon):
    assert sqrt(x, epsilon) == x / 2.0


@pytest.mark.parametrize(
    ("x", "epsilon", "expected"),
    [
        (1.0, 0.3, 1.25),
        (2.0, 0.6, 1.5),
        (2.0, 0.585, 1.4166666666666665),
        (9.0, 5.8, 3.25),
        (16.0, 11.0, 5.0),
        (100.0, 74.0, 26.0),
    ],
)
def test_newton_updates_produce_expected_estimate(x, epsilon, expected):
    assert sqrt(x, epsilon) == pytest.approx(expected, rel=1e-14)


@pytest.mark.parametrize(
    ("x", "epsilon"),
    [
        (1.0, 1e-10),
        (1.25, 0.2),
        (2.0, 0.585),
        (4.0, 2.0),
        (9.0, 5.8),
        (16.0, 11.0),
        (100.0, 74.0),
    ],
)
def test_result_meets_documented_error_bound(x, epsilon):
    result = sqrt(x, epsilon)

    assert math.isfinite(result)
    assert math.sqrt(x) - epsilon <= result <= math.sqrt(x) + epsilon
