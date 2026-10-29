import pytest

from solution import double_the_difference


def test_docstring_mixed_example():
    assert double_the_difference([1, 3, 2, 0]) == 10


def test_negative_values_and_zero_are_ignored():
    assert double_the_difference([-1, -2, 0]) == 0


def test_positive_odd_integer_is_squared():
    assert double_the_difference([9, -2]) == 81


def test_zero_alone_returns_zero():
    assert double_the_difference([0]) == 0


def test_empty_list_returns_zero():
    assert double_the_difference([]) == 0


def test_non_integer_numbers_are_ignored():
    assert double_the_difference([1.5, 3.0, 5.25, -7.5]) == 0


@pytest.mark.xfail(
    strict=True,
    reason="The implementation includes positive even integers, despite the docstring requiring odd integers only.",
)
def test_positive_even_integers_are_ignored():
    assert double_the_difference([2, 4, 6]) == 0


@pytest.mark.xfail(
    strict=True,
    reason="The implementation adds the square of 2 in the docstring's mixed example.",
)
def test_mixed_list_only_squares_odd_integers():
    assert double_the_difference([1, 2, 3, 4, 5]) == 35
