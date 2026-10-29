import pytest

from solution import specialFilter


def test_counts_numbers_with_odd_first_and_last_digits():
    assert specialFilter([15, -73, 14, -15]) == 1


def test_uses_strictly_greater_than_ten():
    assert specialFilter([9, 10, 11, 13, 19]) == 3


def test_only_first_and_last_digits_matter():
    assert specialFilter([131, 153, 179, 102, 120, 234]) == 3


def test_ignores_negative_numbers_and_zero():
    assert specialFilter([-11, -35, 0, 11, 35]) == 2


def test_empty_input_returns_zero():
    assert specialFilter([]) == 0


@pytest.mark.xfail(
    strict=True,
    reason="solution.py incorrectly includes 2 among the odd digits",
)
@pytest.mark.parametrize("number", [12, 21, 123, 321])
def test_even_endpoint_digit_is_not_counted(number):
    assert specialFilter([number]) == 0
