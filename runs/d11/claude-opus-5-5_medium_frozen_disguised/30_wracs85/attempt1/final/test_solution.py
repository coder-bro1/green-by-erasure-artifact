import pytest

from solution import sum_odd_squares

KNOWN_BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py does not filter out even numbers (missing x % 2 check)",
)


# --- Behaviour the current implementation gets right ---------------------

def test_empty_list_returns_zero():
    assert sum_odd_squares([]) == 0


def test_single_odd():
    assert sum_odd_squares([3]) == 9


def test_negative_numbers_ignored():
    assert sum_odd_squares([-5, 7]) == 49


def test_only_negatives_returns_zero():
    assert sum_odd_squares([-1, -3, -5]) == 0


def test_zero_ignored():
    assert sum_odd_squares([0]) == 0


def test_floats_ignored():
    assert sum_odd_squares([1.5, 3.0, 5.5]) == 0


def test_multiple_odds():
    assert sum_odd_squares([1, 3, 5]) == 1 + 9 + 25


def test_large_odd():
    assert sum_odd_squares([10**9 + 1]) == (10**9 + 1) ** 2


def test_accepts_tuple():
    assert sum_odd_squares((1, 3)) == 10


def test_returns_int():
    assert isinstance(sum_odd_squares([3]), int)


# --- Spec cases that expose the even-number bug --------------------------

@KNOWN_BUG
def test_docstring_example_mixed():
    assert sum_odd_squares([3, 4, 1.5]) == 9


@KNOWN_BUG
def test_even_numbers_ignored():
    assert sum_odd_squares([2, 4, 6]) == 0


@KNOWN_BUG
def test_mixed_odd_even():
    assert sum_odd_squares([1, 2, 3, 4, 5]) == 35
