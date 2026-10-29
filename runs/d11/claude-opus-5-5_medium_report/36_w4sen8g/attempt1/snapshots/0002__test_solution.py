import pytest

from solution import derivative


@pytest.mark.parametrize(
    "xs, expected",
    [
        ([3, 1, 2, 4, 5], [1, 4, 12, 20]),  # docstring example
        ([1, 2, 3], [2, 6]),  # docstring example
        ([5, 7], [7]),  # linear
        ([0, 0, 1], [0, 2]),  # x^2 -> 2x
        ([1, 0, 0, 0, 1], [0, 0, 0, 4]),  # x^4 + 1 -> 4x^3
        ([-1, -2, -3], [-2, -6]),  # negative coefficients
        ([0.5, 1.5, 2.5], [1.5, 5.0]),  # float coefficients
    ],
)
def test_derivative_values(xs, expected):
    assert derivative(xs) == expected


def test_constant_polynomial_has_empty_derivative():
    assert derivative([42]) == []


def test_empty_polynomial():
    assert derivative([]) == []


def test_result_length_is_one_shorter():
    xs = list(range(1, 11))
    assert len(derivative(xs)) == len(xs) - 1


def test_input_not_mutated():
    xs = [3, 1, 2, 4, 5]
    derivative(xs)
    assert xs == [3, 1, 2, 4, 5]


def test_returns_list():
    assert isinstance(derivative([1, 2, 3]), list)
