import pytest

from solution import specialFilter


@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        ([], 0),
        ([15, -73, 14, -15], 1),
        ([33, -2, -3, 45, 21, 109], 2),
        ([11, 13, 17, 19], 4),
        ([10, 20, 22, 24, 26, 28], 0),
        ([31, 32, 35, 37, 39, 41, 51], 5),
        ([101, 120, 201, 209, 999], 2),
    ],
)
def test_special_filter_counts_numbers_with_odd_first_and_last_digits(nums, expected):
    assert specialFilter(nums) == expected


def test_special_filter_only_counts_numbers_greater_than_ten():
    assert specialFilter([1, 3, 5, 7, 9, 10, 11]) == 1
