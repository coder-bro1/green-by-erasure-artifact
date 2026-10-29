"""Tests for the behavior currently implemented by ``solution.add``."""

from solution import add


def test_add_sums_even_values_after_the_first_element():
    # The implementation starts at index 1 and checks every subsequent index.
    assert add([4, 2, 6, 7]) == 8


def test_add_ignores_the_first_element():
    assert add([100, 3, 5]) == 0


def test_add_handles_negative_even_values():
    assert add([9, -2, 3, -8]) == -10


def test_add_returns_zero_when_no_later_values_are_even():
    assert add([2, 1, 3, 5]) == 0


def test_add_accepts_a_single_element_list():
    assert add([12]) == 0
