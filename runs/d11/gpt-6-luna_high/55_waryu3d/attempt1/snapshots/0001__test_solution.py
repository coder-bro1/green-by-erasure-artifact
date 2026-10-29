import pytest

from solution import double_the_difference


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([1, 3, 2, 0], 10),
        ([-1, -2, 0], 0),
        ([9, -2], 81),
        ([0], 0),
        ([], 0),
        ([1, 2, 3, 4, 5], 35),
    ],
)
def test_sums_squares_of_positive_odd_integers(values, expected):
    assert double_the_difference(values) == expected


def test_ignores_non_integer_numbers():
    assert double_the_difference([1.5, 3.0, 5.25, -7.5]) == 0


def test_includes_only_positive_odd_integer_values_in_mixed_input():
    assert double_the_difference([3, -3, 4, 7, 2.5, 8, 11]) == 179
