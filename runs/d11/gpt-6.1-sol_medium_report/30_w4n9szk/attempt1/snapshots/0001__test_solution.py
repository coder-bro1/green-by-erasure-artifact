import pytest

from solution import derivative


@pytest.mark.parametrize(
    ('coefficients', 'expected'),
    [
        pytest.param([3, 1, 2, 4, 5], [1, 4, 12, 20], id='docstring-quartic'),
        pytest.param([1, 2, 3], [2, 6], id='docstring-quadratic'),
        pytest.param([7], [], id='constant'),
        pytest.param([0], [], id='zero-constant'),
        pytest.param([4, 5], [5], id='linear'),
        pytest.param([0, 0, 0], [0, 0], id='zero-coefficients'),
        pytest.param([9, 0, 0, 2], [0, 0, 6], id='sparse-polynomial'),
        pytest.param([-3, -2, -4, -5], [-2, -8, -15], id='negative-coefficients'),
        pytest.param([1.5, -2.5, 0.25], [-2.5, 0.5], id='fractional-coefficients'),
        pytest.param([1, 2, 3, 4, 5, 6, 7], [2, 6, 12, 20, 30, 42], id='higher-degree'),
    ],
)
def test_derivative_coefficients(coefficients, expected):
    assert derivative(coefficients) == expected


def test_empty_polynomial():
    assert derivative([]) == []


@pytest.mark.parametrize('coefficients', [[], [7], [3, 1, 2, 4, 5]])
def test_derivative_does_not_mutate_input(coefficients):
    original = coefficients.copy()
    result = derivative(coefficients)
    assert coefficients == original
    assert result is not coefficients
