import pytest

from solution import count_nums


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([], 0),
        ([-1, 11, -11], 1),
        ([1, 1, 2], 3),
        ([0], 0),
        ([-123], 1),  # -1 + 2 + 3 is positive.
        ([-321], 0),  # -3 + 2 + 1 is zero.
        ([-999], 0),
        ([10, 100, 1000], 3),
        ([12, -12, 20, -20], 2),
    ],
)
def test_count_nums(numbers, expected):
    assert count_nums(numbers) == expected


def test_count_nums_counts_each_element_independently():
    assert count_nums([123, 123, -123]) == 3
