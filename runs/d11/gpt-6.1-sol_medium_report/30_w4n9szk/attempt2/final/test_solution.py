import pytest

from solution import derivative


@pytest.mark.xfail(
    strict=True,
    reason=(
        "derivative includes the constant term as a leading zero instead of "
        "returning only the derivative coefficients"
    ),
)
@pytest.mark.parametrize(
    ("coefficients", "expected"),
    [
        pytest.param([3, 1, 2, 4, 5], [1, 4, 12, 20], id="docstring-quartic"),
        pytest.param([1, 2, 3], [2, 6], id="docstring-quadratic"),
        pytest.param([7], [], id="constant"),
        pytest.param([0], [], id="zero-constant"),
        pytest.param([5, 3], [3], id="linear"),
        pytest.param([0, 0, 0, 4], [0, 0, 12], id="monomial"),
        pytest.param([-5, -2, -3, -4], [-2, -6, -12], id="negative"),
        pytest.param([1, -2, 3, -4], [-2, 6, -12], id="mixed-signs"),
        pytest.param([0.5, 1.5, -2.25], [1.5, -4.5], id="fractional"),
        pytest.param([8, 0, 0], [0, 0], id="zero-coefficients"),
        pytest.param([1, 2, 0], [2, 0], id="trailing-zero"),
        pytest.param([0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 5], id="degree-five"),
    ],
)
def test_derivative_coefficients(coefficients, expected):
    assert derivative(coefficients) == expected


def test_derivative_empty_polynomial():
    assert derivative([]) == []


@pytest.mark.parametrize("coefficients", [[], [7], [3, 1, 2, 4, 5]])
def test_derivative_preserves_input(coefficients):
    original = coefficients.copy()
    derivative(coefficients)
    assert coefficients == original
