import pytest

from solution import specialFilter


def test_docstring_example_1():
    assert specialFilter([15, -73, 14, -15]) == 1


def test_docstring_example_2():
    assert specialFilter([33, -2, -3, 45, 21, 109]) == 2


def test_empty_list():
    assert specialFilter([]) == 0


@pytest.mark.parametrize("n", [11, 13, 15, 17, 19, 31, 57, 99, 101, 135, 979, 12345])
def test_counts_odd_first_and_last_digit(n):
    assert specialFilter([n]) == 1


@pytest.mark.parametrize(
    "n",
    [
        12,   # last digit even
        21,   # first digit even
        20,   # both even
        110,  # last digit zero
        201,  # first digit even
        44,
    ],
)
def test_rejects_even_first_or_last_digit(n):
    assert specialFilter([n]) == 0


@pytest.mark.parametrize("n", [10, 9, 7, 5, 3, 1, 0])
def test_not_greater_than_ten_is_excluded(n):
    # 10 is not strictly greater than 10; single odd digits are too small
    assert specialFilter([n]) == 0


@pytest.mark.parametrize("n", [-11, -13, -99, -135, -1])
def test_negative_numbers_are_excluded(n):
    assert specialFilter([n]) == 0


def test_mixed_list():
    assert specialFilter([71, -2, -33, 75, 21, 19]) == 3
    assert specialFilter([43, -12, 93, 125, 121, 109]) == 4


def test_duplicates_counted_each_time():
    assert specialFilter([11, 11, 11]) == 3


def test_large_number():
    assert specialFilter([10**20 + 1]) == 1   # first 1, last 1
    assert specialFilter([2 * 10**20 + 1]) == 0  # first 2


def test_does_not_mutate_input():
    data = [15, 22, 33]
    specialFilter(data)
    assert data == [15, 22, 33]
