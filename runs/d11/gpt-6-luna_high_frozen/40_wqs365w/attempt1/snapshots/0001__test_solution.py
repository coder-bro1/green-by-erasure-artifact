"""Tests for the behavior currently implemented by solution.sum_product."""

from solution import sum_product


def test_returns_sum_and_product_as_a_tuple():
    result = sum_product([3, 0, -2])

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result == (1, 0)


def test_sum_of_empty_input_is_zero():
    assert sum_product([])[0] == 0


def test_sum_handles_positive_and_negative_integers():
    assert sum_product([8, -3, 5])[0] == 10


def test_product_is_zero_when_input_contains_zero():
    assert sum_product([4, 0, 7]) == (11, 0)
