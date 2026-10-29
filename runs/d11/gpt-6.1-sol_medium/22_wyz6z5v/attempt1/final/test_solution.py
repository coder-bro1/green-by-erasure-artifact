import pytest

from solution import specialFilter


@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        ([], 0),
        ([15, -73, 14, -15], 1),
        ([33, -2, -3, 45, 21, 109], 2),
        ([-99, -11, -1, 0, 1, 3, 5, 7, 9, 10], 0),
        ([10, 11, 12, 13], 2),
        ([21, 23, 25, 27, 29], 0),
        ([12, 32, 52, 72, 92], 0),
        ([22, 24, 46, 68, 80], 0),
        ([11, 33, 55, 77, 99], 5),
        ([101, 123, 305, 507, 709, 9001], 6),
        ([100, 302, 504, 706, 908], 0),
        ([201, 403, 605, 807], 0),
        ([11, 11, 11, 22, -11], 3),
        ([10**100 + 1, 2 * 10**100 + 1, 10**100 + 2], 1),
    ],
)
def test_special_filter_examples_and_edge_cases(nums, expected):
    assert specialFilter(nums) == expected


@pytest.mark.parametrize("first_digit", range(1, 10))
@pytest.mark.parametrize("last_digit", range(10))
def test_special_filter_all_two_digit_combinations(first_digit, last_digit):
    number = 10 * first_digit + last_digit
    expected = int(
        number > 10 and first_digit % 2 == 1 and last_digit % 2 == 1
    )

    assert specialFilter([number]) == expected


def test_special_filter_does_not_modify_input():
    nums = [15, -73, 14, -15, 109, 22]
    original = nums.copy()

    assert specialFilter(nums) == 2
    assert nums == original
