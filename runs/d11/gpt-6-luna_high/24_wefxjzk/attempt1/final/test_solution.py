import pytest

from solution import double_the_difference


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], 0),
        ([0], 0),
        ([1, 3, 2, 0], 10),
        ([-1, -2, 0], 0),
        ([9, -2], 81),
        ([1, 2, 3, 4, 5], 35),
        ([7, 7, 7], 147),
    ],
)
def test_sums_squares_of_positive_odd_integers(values, expected):
    assert double_the_difference(values) == expected


def test_ignores_negative_even_and_non_integer_values():
    assert double_the_difference([-3, -2, 2, 4, 1.5, 3.5]) == 0


def test_ignores_non_integer_values_among_valid_odds():
    assert double_the_difference([3, 2.5, 5, -7.5]) == 34
