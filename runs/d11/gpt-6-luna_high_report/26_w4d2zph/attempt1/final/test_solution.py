import pytest

from solution import double_the_difference


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([1, 3, 2, 0], 10),
        ([-1, -2, 0], 0),
        ([9, -2], 81),
        ([0], 0),
        ([], 0),
        ([1, 2, 3, 4, 5], 35),
        ([1.5, 2.5, 3.5, -3.5], 0),
        ([3.0, 5.0, 2.0], 0),
        ([1, 1, 1], 3),
        ([10**20 + 1, 10**20], (10**20 + 1) ** 2),
    ],
)
def test_double_the_difference(numbers, expected):
    assert double_the_difference(numbers) == expected


def test_only_positive_odd_integers_contribute():
    assert double_the_difference([-7, -3, 2, 4, 6, 8]) == 0
    assert double_the_difference([-2, 3, 4, 7]) == 58

