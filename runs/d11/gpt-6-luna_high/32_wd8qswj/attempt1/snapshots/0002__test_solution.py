import pytest

from solution import specialFilter


@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        ([], 0),
        ([1, 9, 10], 0),  # Values must be greater than 10.
        ([11], 1),
        ([12, 13, 15, 17, 19], 4),  # Both endpoint digits must be odd.
        ([31, 33, 35, 37, 39], 5),
        ([15, -73, 14, -15], 1),
        ([33, -2, -3, 45, 21, 109], 2),
        ([111, 203, 909, 1001, 1002], 3),
        ([0, 1, 2, 8, 9, 10, 20, 22, 28, 29], 0),
    ],
)
def test_special_filter(nums, expected):
    assert specialFilter(nums) == expected


def test_special_filter_does_not_mutate_input():
    nums = [15, 24, 39]
    original = nums.copy()

    specialFilter(nums)

    assert nums == original
