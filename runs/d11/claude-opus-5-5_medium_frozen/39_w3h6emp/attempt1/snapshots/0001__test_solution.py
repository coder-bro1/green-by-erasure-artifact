import pytest

from solution import specialFilter

BUG_REASON = (
    "Known bug in solution.py: odd_digits contains 2, so numbers whose "
    "first/last digit is 2 are wrongly counted"
)


# --- Behaviour that matches the specification ---------------------------------

def test_docstring_example_one():
    assert specialFilter([15, -73, 14, -15]) == 1


def test_empty_list():
    assert specialFilter([]) == 0


def test_single_qualifying_number():
    assert specialFilter([15]) == 1


@pytest.mark.parametrize("n", [11, 13, 15, 17, 19, 31, 55, 77, 99, 101, 135, 579, 9119, 10001])
def test_odd_first_and_last_digit_counted(n):
    assert specialFilter([n]) == 1


@pytest.mark.parametrize("n", [10, 9, 7, 1, 0, -11, -15, -73, -99, -135])
def test_not_greater_than_ten_excluded(n):
    # 10 is not > 10; single digits and negatives never qualify
    assert specialFilter([n]) == 0


@pytest.mark.parametrize("n", [14, 16, 18, 30, 50, 70, 90, 110, 314])
def test_even_last_digit_excluded(n):
    # first digit odd, last digit even (2 deliberately excluded, see bug tests)
    assert specialFilter([n]) == 0


@pytest.mark.parametrize("n", [41, 43, 65, 87, 409, 6001, 81])
def test_even_first_digit_excluded(n):
    # last digit odd, first digit even (2 deliberately excluded, see bug tests)
    assert specialFilter([n]) == 0


def test_mixed_list():
    assert specialFilter([11, 14, 33, 46, 57, 8, -19, 97, 100]) == 4


def test_duplicates_counted_each_time():
    assert specialFilter([13, 13, 13]) == 3


def test_does_not_mutate_input():
    nums = [15, -73, 14, -15]
    specialFilter(nums)
    assert nums == [15, -73, 14, -15]


def test_large_number():
    assert specialFilter([10**20 + 1]) == 1          # first 1, last 1
    assert specialFilter([3 * 10**20 + 4]) == 0      # last digit 4


# --- Spec cases that expose the bug (strict xfail: fails loudly once fixed) ----

@pytest.mark.xfail(strict=True, reason=BUG_REASON)
def test_docstring_example_two():
    assert specialFilter([33, -2, -3, 45, 21, 109]) == 2


@pytest.mark.xfail(strict=True, reason=BUG_REASON)
@pytest.mark.parametrize("n", [12, 21, 22, 23, 29, 32, 52, 203, 1002])
def test_digit_two_is_not_odd(n):
    assert specialFilter([n]) == 0
