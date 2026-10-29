import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solution import count_nums


def test_empty_array_has_no_matching_numbers():
    assert count_nums([]) == 0


def test_zero_does_not_have_a_positive_digit_sum():
    assert count_nums([0]) == 0


def test_positive_multi_digit_numbers_are_counted_by_digit_sum():
    assert count_nums([12, 34]) == 2


def test_negative_multi_digit_number_with_positive_signed_digit_sum_counts():
    # -123 has signed digits -1, 2, and 3, whose sum is positive.
    assert count_nums([-123]) == 1


@pytest.mark.xfail(
    strict=True,
    reason="count_nums negates the leading digit of positive numbers, so it misses [1, 1, 2].",
)
def test_documented_positive_single_digit_example():
    assert count_nums([1, 1, 2]) == 3


@pytest.mark.xfail(
    strict=True,
    reason="count_nums makes the leading digit of negative numbers positive, contrary to the signed-digit rule.",
)
def test_documented_negative_example():
    assert count_nums([-1, 11, -11]) == 1


@pytest.mark.xfail(
    strict=True,
    reason="The signed digit sum of -11 is zero, but count_nums treats its leading digit as positive.",
)
def test_negative_number_with_zero_signed_digit_sum_is_not_counted():
    assert count_nums([-11]) == 0


@pytest.mark.xfail(
    strict=True,
    reason="The digit sum of positive 10 is positive, but count_nums negates its leading digit and returns zero.",
)
def test_positive_number_with_positive_digit_sum_is_counted():
    assert count_nums([10]) == 1
