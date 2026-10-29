import pytest

from solution import count_nums


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([], 0),
        ([-1, 11, -11], 1),
        ([1, 1, 2], 3),
        ([0, 0], 0),
        ([1, 9, 10, 100, 1000], 5),
        ([-1, -9, -10, -100], 0),
        ([-11, -22, -123, -99, -101, -909], 2),
        ([-21, -120, -912, -1001], 1),
        ([0, 7, -7, 11, -11, -123, -321], 3),
        ([10**100, -(10**100), -(10**100 + 99)], 2),
    ],
)
def test_count_nums(numbers, expected):
    assert count_nums(numbers) == expected


def test_count_nums_preserves_input():
    numbers = [-123, 0, 10, -11, 10]
    original = numbers.copy()

    assert count_nums(numbers) == 3
    assert numbers == original
