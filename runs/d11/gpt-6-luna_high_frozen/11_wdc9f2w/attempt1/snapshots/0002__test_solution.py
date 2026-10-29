import pytest

from solution import count_nums


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], 0),
        ([0], 0),
        ([1], 0),
        ([12], 1),
        ([11], 0),
        ([-1], 1),
        ([-11], 1),
        ([-12], 1),
        ([1, 12, -1, -12, 0], 3),
    ],
)
def test_count_nums(values, expected):
    assert count_nums(values) == expected


def test_count_nums_counts_each_qualifying_element():
    # Repeated values are separate elements and should each be counted.
    assert count_nums([12, 12, -11, -11]) == 4


def test_count_nums_accepts_values_with_multiple_digits():
    assert count_nums([123, -123, 101, -101]) == 3
