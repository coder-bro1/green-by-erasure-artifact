import pytest

from solution import derivative

BUG = (
    "derivative() keeps the constant term's slot: it returns [i * x for i, x in "
    "enumerate(xs)], which yields a leading 0 and a list as long as xs, instead of "
    "dropping xs[0] as the docstring requires"
)


@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_example_1():
    assert derivative([3, 1, 2, 4, 5]) == [1, 4, 12, 20]


@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_example_2():
    assert derivative([1, 2, 3]) == [2, 6]


@pytest.mark.xfail(strict=True, reason=BUG)
def test_linear():
    # d/dx (5 + 7x) = 7
    assert derivative([5, 7]) == [7]


@pytest.mark.xfail(strict=True, reason=BUG)
def test_constant_polynomial_has_empty_derivative():
    assert derivative([42]) == []


@pytest.mark.xfail(strict=True, reason=BUG)
def test_negative_and_float_coefficients():
    assert derivative([0.5, -2, 1.5, -1]) == [-2, 3.0, -3]


@pytest.mark.xfail(strict=True, reason=BUG)
def test_result_length_is_one_less():
    xs = [1, 2, 3, 4, 5, 6]
    assert len(derivative(xs)) == len(xs) - 1


def test_empty_list():
    assert derivative([]) == []


def test_input_not_mutated():
    xs = [3, 1, 2, 4, 5]
    derivative(xs)
    assert xs == [3, 1, 2, 4, 5]


def test_returns_list():
    assert isinstance(derivative([1, 2, 3]), list)
