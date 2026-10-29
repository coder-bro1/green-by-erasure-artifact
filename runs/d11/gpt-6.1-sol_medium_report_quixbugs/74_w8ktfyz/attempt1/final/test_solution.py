"""Tests for the square-root contract documented in solution.py."""

import math

import pytest

from solution import sqrt


@pytest.mark.parametrize(
    ("x", "epsilon"),
    [
        (1.0, 1e-12),
        (1.000001, 1e-12),
        (1.5, 1e-12),
        (2.0, 0.01),
        (2.0, 1e-12),
        (3.0, 1e-12),
        (4.0, 1e-12),
        (9.0, 1e-12),
        (100.0, 1e-10),
        (1e6, 1e-9),
        (1e12, 0.001),
        (1.0, 1.0),
        (2.0, 10.0),
        (100.0, 1e4),
    ],
)
def test_sqrt_returns_float_within_documented_interval(x, epsilon):
    result = sqrt(x, epsilon)
    expected = math.sqrt(x)

    assert isinstance(result, float)
    assert expected - epsilon <= result <= expected + epsilon


def test_sqrt_documented_example():
    assert sqrt(2, 0.01) == 1.4166666666666665


@pytest.mark.xfail(
    strict=True,
    raises=OverflowError,
    reason=(
        "Large finite inputs meet the documented preconditions, but squaring "
        "the initial x / 2 approximation overflows instead of returning "
        "a float within epsilon of the square root."
    ),
)
@pytest.mark.parametrize(
    ("x", "epsilon"),
    [(1e155, 1e65), (1e200, 1e88), (1e308, 1e142)],
)
def test_sqrt_large_finite_inputs(x, epsilon):
    expected = math.sqrt(x)
    result = sqrt(x, epsilon)

    assert isinstance(result, float)
    assert expected - epsilon <= result <= expected + epsilon
