import pytest

from solution import double_the_difference

ODD_BUG = "solution.py never filters for odd numbers, so even positive integers are squared and summed"


def test_empty_list_returns_zero():
    assert double_the_difference([]) == 0


def test_single_zero():
    assert double_the_difference([0]) == 0


def test_all_negative_or_zero():
    assert double_the_difference([-1, -2, 0]) == 0


def test_odd_with_negative():
    assert double_the_difference([9, -2]) == 81


def test_only_odd_positive_integers():
    assert double_the_difference([1, 3, 5]) == 1 + 9 + 25


def test_negative_odd_ignored():
    assert double_the_difference([-3, -5, 7]) == 49


def test_floats_ignored():
    assert double_the_difference([1.5, 3.0, 5]) == 25


def test_only_floats_returns_zero():
    assert double_the_difference([0.1, 0.2, 0.3]) == 0


@pytest.mark.xfail(strict=True, reason=ODD_BUG)
def test_docstring_example_mixed():
    assert double_the_difference([1, 3, 2, 0]) == 10


@pytest.mark.xfail(strict=True, reason=ODD_BUG)
def test_even_positive_ignored():
    assert double_the_difference([2]) == 0


@pytest.mark.xfail(strict=True, reason=ODD_BUG)
def test_mixed_odd_and_even():
    assert double_the_difference([2, 4, 5, 6, 7]) == 25 + 49


@pytest.mark.xfail(
    strict=True,
    reason="Non-integer check uses '.' not in str(i); float('inf') has no '.' and is not ignored",
)
def test_infinity_ignored():
    assert double_the_difference([float("inf"), 3]) == 9
