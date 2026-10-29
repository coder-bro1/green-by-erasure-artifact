import pytest

from solution import count_nums


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([], 0),
        ([0], 0),
        ([1, 1, 2], 3),
        ([-1, 11, -11], 1),
        ([-123, -99, -10, -1], 0),
        ([12, 20, 101, 1000], 4),
        ([-123, -101, -100, -99, -20, -11, -10, -2], 0),
        ([-120, -111, -1000, -1001], 1),
        ([123, -123, 999, -999], 2),
    ],
)
def test_count_nums(numbers, expected):
    assert count_nums(numbers) == expected


def test_count_nums_counts_each_element_independently():
    # Repeated values should each contribute to the count.
    assert count_nums([7, 7, -7, -7]) == 2


def test_count_nums_handles_large_integers():
    assert count_nums([int("9" * 100), -int("9" * 100)]) == 1
