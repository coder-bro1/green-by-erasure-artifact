import pytest

from solution import positive_digit_sums


@pytest.mark.parametrize(
    "values, expected",
    [
        ([-12, 3, 0], 2),   # docstring example
        ([24, -8], 1),      # docstring example
        ([], 0),            # docstring example
    ],
)
def test_docstring_examples(values, expected):
    assert positive_digit_sums(values) == expected


def test_negative_first_digit_counts_negative():
    # -45 -> -4 + 5 = 1 > 0
    assert positive_digit_sums([-45]) == 1


def test_negative_sum_not_counted():
    # -54 -> -5 + 4 = -1
    assert positive_digit_sums([-54]) == 0


def test_negative_sum_zero_not_counted():
    # -11 -> -1 + 1 = 0
    assert positive_digit_sums([-11]) == 0


def test_single_digit_negative_not_counted():
    assert positive_digit_sums([-1, -9]) == 0


def test_positive_numbers_counted():
    assert positive_digit_sums([1, 9, 10, 123]) == 4


def test_zero_not_counted():
    assert positive_digit_sums([0, 0]) == 0


def test_mixed():
    # 1 (yes), 11 (yes), -1 (no), -11 (no), -45 (yes), 0 (no)
    assert positive_digit_sums([1, 11, -1, -11, -45, 0]) == 3


def test_large_negative():
    # -1999 -> -1 + 9 + 9 + 9 = 26
    assert positive_digit_sums([-1999]) == 1
