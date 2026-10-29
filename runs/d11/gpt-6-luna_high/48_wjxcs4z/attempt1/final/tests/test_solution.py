import pytest

from solution import derivative


@pytest.mark.parametrize(
    ("coefficients", "expected"),
    [
        ([], []),
        ([7], []),
        ([3, 1, 2, 4, 5], [1, 4, 12, 20]),
        ([1, 2, 3], [2, 6]),
        ([5, 0, 3, 0, 2], [0, 6, 0, 8]),
        ([0, -2, 1.5], [-2, 3.0]),
    ],
)
def test_derivative(coefficients, expected):
    original = coefficients.copy()

    assert derivative(coefficients) == expected
    assert coefficients == original
