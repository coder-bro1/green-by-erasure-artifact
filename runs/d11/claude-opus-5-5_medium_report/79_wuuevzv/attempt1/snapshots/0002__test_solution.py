import pytest

from solution import count_nums

SIGN_BUG = (
    "digits_sum negates the leading digit of positive numbers and makes the "
    "leading digit of negative numbers positive (n[0] * neg * -1 has the sign "
    "inverted), contrary to the docstring"
)


# ---- Cases that pass (correct behavior or bug doesn't affect the outcome) ----

def test_empty_list():
    assert count_nums([]) == 0


def test_zero_has_digit_sum_zero():
    assert count_nums([0]) == 0
    assert count_nums([0, 0, 0]) == 0


def test_positive_with_large_digit_sum():
    # 19 -> 1 + 9 = 10 > 0
    assert count_nums([19]) == 1


def test_negative_with_positive_signed_sum():
    # -19 -> -1 + 9 = 8 > 0
    assert count_nums([-19]) == 1


def test_input_not_mutated():
    arr = [-1, 11, -11]
    count_nums(arr)
    assert arr == [-1, 11, -11]


# ---- Cases from the docstring and others exposing the sign bug ----

@pytest.mark.xfail(strict=True, reason=SIGN_BUG)
def test_docstring_mixed_example():
    # -1 -> -1, 11 -> 2, -11 -> 0  => only 11 counts
    assert count_nums([-1, 11, -11]) == 1


@pytest.mark.xfail(strict=True, reason=SIGN_BUG)
def test_docstring_all_positive_example():
    assert count_nums([1, 1, 2]) == 3


@pytest.mark.xfail(strict=True, reason=SIGN_BUG)
def test_single_positive_digit():
    assert count_nums([5]) == 1


@pytest.mark.xfail(strict=True, reason=SIGN_BUG)
def test_single_negative_digit():
    assert count_nums([-5]) == 0


@pytest.mark.xfail(strict=True, reason=SIGN_BUG)
def test_positive_ten():
    # 10 -> 1 + 0 = 1 > 0
    assert count_nums([10]) == 1


@pytest.mark.xfail(strict=True, reason=SIGN_BUG)
def test_negative_ten():
    # -10 -> -1 + 0 = -1
    assert count_nums([-10]) == 0


@pytest.mark.xfail(strict=True, reason=SIGN_BUG)
def test_negative_with_negative_signed_sum():
    # -91 -> -9 + 1 = -8
    assert count_nums([-91]) == 0


@pytest.mark.xfail(strict=True, reason=SIGN_BUG)
def test_mixed_list():
    # 12->3, 23->5, 34->7, -45->1, -55->0, -56->1  => 5
    assert count_nums([12, 23, 34, -45, -55, -56]) == 5


def test_negative_one_and_positive_one():
    # Correct total (only 1 counts). Note: the buggy implementation also
    # returns 1 here, but by counting -1 instead of 1.
    assert count_nums([-1, 1]) == 1
