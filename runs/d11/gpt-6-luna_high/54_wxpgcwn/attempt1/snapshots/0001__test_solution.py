import pytest

from solution import derivative


@pytest.mark.parametrize(
    ("coefficients", "expected"),
    [
        ([3, 1, 2, 4, 5], [1, 4, 12, 20]),
        ([1, 2, 3], [2, 6]),
        ([7, -3], [-3]),
        ([2, 0, -4, 0], [0, -8, 0]),
        ([1.5, 2.5, -0.5], [2.5, -1.0]),
        ([9], []),
        ([], []),
    ],
)
def test_derivative(coefficients, expected):
    original = coefficients.copy()

    assert derivative(coefficients) == expected
    assert coefficients == original
