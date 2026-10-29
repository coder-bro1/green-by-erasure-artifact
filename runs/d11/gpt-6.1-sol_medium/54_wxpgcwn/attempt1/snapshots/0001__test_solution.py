import pytest

from solution import derivative


@pytest.mark.parametrize(
    ("coefficients", "expected"),
    [
        pytest.param([3, 1, 2, 4, 5], [1, 4, 12, 20], id="first-docstring-example"),
        pytest.param([1, 2, 3], [2, 6], id="second-docstring-example"),
        pytest.param([], [], id="empty-polynomial"),
        pytest.param([7], [], id="constant-polynomial"),
        pytest.param([0], [], id="zero-polynomial"),
        pytest.param([9, 5], [5], id="linear-polynomial"),
        pytest.param([0, 0, 0, 2], [0, 0, 6], id="sparse-polynomial"),
        pytest.param([5, -2, -3, -4], [-2, -6, -12], id="negative-coefficients"),
        pytest.param([1, 2, 0, 0], [2, 0, 0], id="preserves-trailing-zeros"),
        pytest.param([0.5, 1.25, -2.5, 0.125], [1.25, -5.0, 0.375], id="floats"),
        pytest.param([0, 10**100, -(10**100)], [10**100, -2 * 10**100], id="large-integers"),
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
    result.append(99)
    assert coefficients == original


def test_repeated_derivatives_reduce_to_constant_then_empty():
    coefficients = [5, -2, 3, 4]

    first = derivative(coefficients)
    second = derivative(first)
    third = derivative(second)

    assert first == [-2, 6, 12]
    assert second == [6, 24]
    assert third == [24]
    assert derivative(third) == []
    assert derivative([]) == []


def test_high_degree_monomial():
    coefficients = [0] * 100 + [7]

    assert derivative(coefficients) == [0] * 99 + [700]
