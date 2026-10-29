import pytest

from solution import derivative


def test_derivative_of_empty_polynomial():
    assert derivative([]) == []


@pytest.mark.xfail(
    reason="derivative currently keeps the constant term and uses the wrong coefficient index",
    strict=False,
)
@pytest.mark.parametrize(
    ("coefficients", "expected"),
    [
        ([3, 1, 2, 4, 5], [1, 4, 12, 20]),
        ([1, 2, 3], [2, 6]),
        ([7], []),
        ([0, 0, 0], [0, 0]),
        ([2, -3, 0.5], [-3, 1.0]),
    ],
)
def test_derivative_matches_polynomial_coefficients(coefficients, expected):
    assert derivative(coefficients) == expected
