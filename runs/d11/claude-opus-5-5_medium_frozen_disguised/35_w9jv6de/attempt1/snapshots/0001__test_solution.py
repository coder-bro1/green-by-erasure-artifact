import pytest

from solution import poly_slope_coeffs


def evaluate(coeffs, t):
    return sum(c * t**k for k, c in enumerate(coeffs))


@pytest.mark.parametrize(
    "coeffs, expected",
    [
        ([5, 0, 3], [0, 6]),          # docstring example
        ([2, 4], [4]),                # docstring example
        ([1, 1, 1, 1], [1, 2, 3]),
        ([0, 0, 0, 2], [0, 0, 6]),
        ([3, -2, 0.5], [-2, 1.0]),
        ([9, 7, -4, 0, 1], [7, -8, 0, 4]),
    ],
)
def test_known_derivatives(coeffs, expected):
    assert poly_slope_coeffs(coeffs) == expected


def test_result_has_one_fewer_coefficient():
    coeffs = [4, 3, 2, 1, 5]
    assert len(poly_slope_coeffs(coeffs)) == len(coeffs) - 1


def test_constant_term_does_not_affect_result():
    assert poly_slope_coeffs([100, 2, 3]) == poly_slope_coeffs([-7, 2, 3])


def test_matches_numerical_derivative():
    coeffs = [1, -3, 2, 0.5]
    deriv = poly_slope_coeffs(coeffs)
    h = 1e-6
    for t in (-2.0, 0.0, 1.5, 3.0):
        numeric = (evaluate(coeffs, t + h) - evaluate(coeffs, t - h)) / (2 * h)
        assert evaluate(deriv, t) == pytest.approx(numeric, rel=1e-5, abs=1e-6)


def test_input_not_mutated():
    coeffs = [5, 0, 3]
    poly_slope_coeffs(coeffs)
    assert coeffs == [5, 0, 3]
