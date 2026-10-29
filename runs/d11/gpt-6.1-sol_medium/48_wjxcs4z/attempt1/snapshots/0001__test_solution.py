import pytest

from solution import derivative


@pytest.mark.parametrize(
    ("coefficients", "expected"),
    [
        pytest.param([3, 1, 2, 4, 5], [1, 4, 12, 20], id="docstring-quartic"),
        pytest.param([1, 2, 3], [2, 6], id="docstring-quadratic"),
        pytest.param([], [], id="empty-polynomial"),
        pytest.param([7], [], id="constant"),
        pytest.param([0], [], id="zero-constant"),
        pytest.param([5, 3], [3], id="linear"),
        pytest.param([0, 0, 0], [0, 0], id="zero-coefficients"),
        pytest.param([4, 0, 0, 2], [0, 0, 6], id="sparse-polynomial"),
        pytest.param([-5, -2, -3, -4], [-2, -6, -12], id="negative-coefficients"),
        pytest.param([1, 2, 0, 0], [2, 0, 0], id="trailing-zeros"),
        pytest.param([0.5, 1.5, -2.25, 0.25], [1.5, -4.5, 0.75], id="fractional-coefficients"),
    ],
)
def test_derivative(coefficients, expected):
    assert derivative(coefficients) == expected


def test_derivative_does_not_mutate_input():
    coefficients = [3, 1, 2, 4, 5]
    original = coefficients.copy()

    result = derivative(coefficients)

    assert coefficients == original
    assert result is not coefficients
