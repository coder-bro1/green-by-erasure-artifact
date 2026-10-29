import math
from fractions import Fraction

import pytest

from solution import double_the_difference


# Docstring examples
@pytest.mark.parametrize(
    "lst, expected",
    [
        ([1, 3, 2, 0], 10),
        ([-1, -2, 0], 0),
        ([9, -2], 81),
        ([0], 0),
        ([], 0),
    ],
)
def test_docstring_examples(lst, expected):
    assert double_the_difference(lst) == expected


def test_only_even_numbers():
    assert double_the_difference([2, 4, 6, 100]) == 0


def test_only_odd_numbers():
    assert double_the_difference([1, 3, 5, 7]) == 1 + 9 + 25 + 49


def test_negative_odd_numbers_ignored():
    assert double_the_difference([-3, -5, 3]) == 9


def test_non_integer_floats_ignored():
    assert double_the_difference([1.5, 2.5, 3]) == 9


def test_negative_float_ignored():
    assert double_the_difference([-1.5, 5]) == 25


def test_single_odd():
    assert double_the_difference([7]) == 49


def test_large_odd_integer():
    n = 10**9 + 7
    assert double_the_difference([n]) == n * n


def test_duplicates_counted():
    assert double_the_difference([3, 3, 3]) == 27


def test_mixed_list():
    lst = [5, 0.1, -5, 4, 11, 0.3, -7.0, 2]
    assert double_the_difference(lst) == 25 + 121


def test_result_is_int_for_int_input():
    result = double_the_difference([1, 3])
    assert result == 10
    assert isinstance(result, int)


def test_input_not_mutated():
    lst = [1, 2, 3, -1, 2.5]
    copy = list(lst)
    double_the_difference(lst)
    assert lst == copy


def test_accepts_tuple():
    assert double_the_difference((1, 2, 3)) == 10


def test_integer_valued_fraction_counted():
    # Fraction(3, 1) is an integer value; it is odd and positive.
    assert double_the_difference([Fraction(3, 1)]) == 9


@pytest.mark.xfail(
    strict=True,
    reason="Non-integer check relies on '.' in str(i); str(Fraction(1, 3)) is "
    "'1/3', so the non-integer is wrongly included.",
)
def test_non_integer_fraction_ignored():
    assert double_the_difference([Fraction(1, 3), 3]) == 9


@pytest.mark.xfail(
    strict=True,
    reason="str(float('inf')) is 'inf' (no '.') and inf % 2 is nan != 0, so "
    "infinity is wrongly treated as an odd integer and the result is inf.",
)
def test_infinity_ignored():
    assert double_the_difference([math.inf, 3]) == 9
