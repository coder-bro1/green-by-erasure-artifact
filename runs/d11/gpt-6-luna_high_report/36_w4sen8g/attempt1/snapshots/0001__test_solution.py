import pytest

from solution import derivative


@pytest.mark.parametrize(
    ("coefficients", "expected"),
    [
        ([3, 1, 2, 4, 5], [1, 4, 12, 20]),
        ([1, 2, 3], [2, 6]),
        ([7], []),
        ([], []),
        ([0, 0, 0], [0, 0]),
        ([5, -3, 0, 2], [-3, 0, 6]),
        ([1.5, 2.5, -1.25], [2.5, -2.5]),
    ],
)
def test_derivative_returns_coefficients_of_polynomial_derivative(coefficients, expected):
    assert derivative(coefficients) == expected
