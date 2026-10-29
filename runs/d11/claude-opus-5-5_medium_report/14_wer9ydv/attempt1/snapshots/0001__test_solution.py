import pytest

from solution import specialFilter

BUG_REASON = (
    "solution.py's odd_digits tuple contains 2, so numbers whose first or "
    "last digit is 2 are wrongly counted"
)


def test_docstring_example_1():
    assert specialFilter([15, -73, 14, -15]) == 1


@pytest.mark.xfail(strict=True, reason=BUG_REASON)
def test_docstring_example_2():
    # 33 and 109 qualify; 21 starts with 2 (even) and must not count.
    assert specialFilter([33, -2, -3, 45, 21, 109]) == 2


def test_empty_list():
    assert specialFilter([]) == 0


def test_ten_and_below_excluded():
    # 11 is the only element > 10; 9, 7, 1 are odd but not > 10.
    assert specialFilter([1, 3, 5, 7, 9, 10, 11]) == 1


def test_exactly_ten_not_counted():
    assert specialFilter([10]) == 0


def test_negative_numbers_never_counted():
    assert specialFilter([-11, -33, -99, -135]) == 0


@pytest.mark.parametrize("n", [11, 13, 35, 57, 79, 99, 101, 135, 9999, 70001])
def test_qualifying_numbers(n):
    assert specialFilter([n]) == 1


@pytest.mark.parametrize("n", [14, 16, 18, 40, 41, 63, 85, 100, 456, 891 * 10])
def test_non_qualifying_numbers_with_non2_even_digit(n):
    assert specialFilter([n]) == 0


@pytest.mark.xfail(strict=True, reason=BUG_REASON)
@pytest.mark.parametrize("n", [12, 21, 23, 32, 52, 29, 201, 1002])
def test_first_or_last_digit_two_not_counted(n):
    assert specialFilter([n]) == 0


def test_middle_digits_ignored():
    # middle digits may be even
    assert specialFilter([1241, 3005, 7867]) == 3


def test_mixed_list():
    assert specialFilter([11, 15, 14, 100, -77, 77, 8, 919]) == 4


def test_duplicates_counted_each_time():
    assert specialFilter([33, 33, 33]) == 3
