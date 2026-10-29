"""Tests for solution.count_nums.

Spec (from the docstring): count the elements whose sum of *signed* digits is
> 0, where a negative number's first digit carries the minus sign
(-123 -> -1 + 2 + 3 = 4).

Known defect in solution.py: digits_sum computes ``n[0] * neg * -1``, which
negates the leading digit of *positive* numbers and leaves the leading digit of
negative numbers positive -- the inverse of the spec. Tests that expose this are
marked ``xfail(strict=True)`` so the suite stays green while documenting the
bug; once solution.py is fixed they will XPASS, fail strictly, and the markers
should be removed.
"""

import pytest

from solution import count_nums

BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py inverts the sign of the leading digit (n[0] * neg * -1)",
)


# --- Behaviour where the implementation agrees with the spec ---------------

def test_empty_list_returns_zero():
    assert count_nums([]) == 0


def test_zero_has_digit_sum_zero_and_is_not_counted():
    assert count_nums([0]) == 0
    assert count_nums([0, 0, 0]) == 0


@pytest.mark.parametrize(
    "arr, expected",
    [
        ([19], 1),         # spec: 1 + 9 = 10
        ([-19], 1),        # spec: -1 + 9 = 8
        ([-123], 1),       # spec: -1 + 2 + 3 = 4 (docstring example number)
        ([12, 23, 34, -45, -56, 0], 5),
        ([-0], 0),
    ],
)
def test_cases_matching_spec(arr, expected):
    assert count_nums(arr) == expected


def test_returns_int():
    result = count_nums([19, -19])
    assert isinstance(result, int)
    assert result == 2


def test_does_not_mutate_input():
    arr = [19, -123, 0]
    snapshot = list(arr)
    count_nums(arr)
    assert arr == snapshot


def test_accepts_any_iterable():
    assert count_nums((19, -19, 0)) == 2
    assert count_nums(x for x in [19, -19, 0]) == 2


def test_large_number():
    # spec: 9 * 20 = 180 > 0
    assert count_nums([int("9" * 20)]) == 1


# --- Spec cases the current implementation gets wrong ----------------------

@BUG
def test_docstring_example_mixed_signs():
    assert count_nums([-1, 11, -11]) == 1


@BUG
def test_docstring_example_all_positive():
    assert count_nums([1, 1, 2]) == 3


@BUG
@pytest.mark.parametrize("n", [1, 5, 10, 100])
def test_positive_number_with_positive_digit_sum_is_counted(n):
    assert count_nums([n]) == 1


@BUG
@pytest.mark.parametrize("n", [-1, -10, -11, -100])
def test_negative_number_with_non_positive_digit_sum_not_counted(n):
    # spec: -1 -> -1, -10 -> -1, -11 -> 0, -100 -> -1
    assert count_nums([n]) == 0
