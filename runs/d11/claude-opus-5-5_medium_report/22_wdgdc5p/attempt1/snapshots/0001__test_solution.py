import pytest

from solution import count_nums


# Docstring examples
def test_empty():
    assert count_nums([]) == 0


def test_docstring_mixed():
    assert count_nums([-1, 11, -11]) == 1


def test_docstring_positive():
    assert count_nums([1, 1, 2]) == 3


@pytest.mark.parametrize(
    "arr, expected",
    [
        ([0], 0),                 # digit sum 0 is not > 0
        ([-1], 0),                # -1
        ([-10], 0),               # -1 + 0 = -1
        ([-11], 0),               # -1 + 1 = 0
        ([-12], 1),               # -1 + 2 = 1
        ([-123], 1),              # -1 + 2 + 3 = 4
        ([-91], 0),               # -9 + 1 = -8
        ([-19], 1),               # -1 + 9 = 8
        ([10], 1),
        ([100], 1),
        ([987654321], 1),
        ([-987654321], 1),        # -9 + 36 = 27
        ([12, 23, 34, -45, -56, 0], 5),
        ([-0, 1], 1),
        ([1, 6, 9, -6, 0, 1, 5], 5),
        ([1, 100, 98, -7, 1, -1], 4),
        ([-1, -2, -3, -9], 0),
    ],
)
def test_various(arr, expected):
    assert count_nums(arr) == expected


def test_large_negative():
    # -1 + 0*20 + 1 = 0 -> not counted; -1 followed by twenty 0s then 2 -> 1
    assert count_nums([-(10**21 + 1)]) == 0
    assert count_nums([-(10**21 + 2)]) == 1


def test_does_not_mutate_input():
    arr = [-12, 0, 5]
    copy = list(arr)
    count_nums(arr)
    assert arr == copy


def test_accepts_tuple():
    assert count_nums((1, -11, -12)) == 2
