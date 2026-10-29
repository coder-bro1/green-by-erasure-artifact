import pytest

from solution import specialFilter


def test_special_filter_matches_first_docstring_example():
    assert specialFilter([15, -73, 14, -15]) == 1


def test_special_filter_matches_second_docstring_example():
    assert specialFilter([33, -2, -3, 45, 21, 109]) == 2


@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        ([], 0),
        ([10, 11, 13, 19, 20], 3),
        ([31, 33, 35, 37, 39], 5),
        ([12, 23, 32, 44, 51, 59], 2),
        ([-11, -33, -99, 13], 1),
        ([15, 15, 15], 3),
    ],
)
def test_special_filter_counts_values_with_odd_outer_digits(nums, expected):
    assert specialFilter(nums) == expected
