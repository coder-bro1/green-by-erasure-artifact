import pytest

from solution import specialFilter


def test_empty_input_returns_zero():
    assert specialFilter([]) == 0


def test_counts_numbers_with_odd_first_and_last_digits():
    assert specialFilter([11, 13, 15, 17, 19, 31, 35, 39]) == 8


def test_values_at_or_below_ten_do_not_count():
    assert specialFilter([1, 3, 9, 10]) == 0


def test_negative_numbers_do_not_count_as_greater_than_ten():
    assert specialFilter([-73, -15, -11]) == 0


def test_first_docstring_example():
    assert specialFilter([15, -73, 14, -15]) == 1


@pytest.mark.xfail(
    strict=True,
    reason="The implementation treats digit 2 as odd, so it counts 21 although its first digit is even.",
)
def test_even_first_digit_is_rejected():
    assert specialFilter([21]) == 0


@pytest.mark.xfail(
    strict=True,
    reason="The implementation treats digit 2 as odd, so it counts 12 although its last digit is even.",
)
def test_even_last_digit_is_rejected():
    assert specialFilter([12]) == 0


@pytest.mark.xfail(
    strict=True,
    reason="The implementation treats digit 2 as odd, incorrectly counting 21; the written rule yields 3 for this list.",
)
def test_second_docstring_example_according_to_written_rule():
    # The stated rule counts 33, 45, and 109. The example's stated result of 2
    # conflicts with that rule, so the rule-based expected value is 3.
    assert specialFilter([33, -2, -3, 45, 21, 109]) == 3


@pytest.mark.xfail(
    strict=True,
    reason="The docstring states this example returns 2, but the implementation returns 4; the rule itself gives 3.",
)
def test_second_docstring_example_stated_result():
    assert specialFilter([33, -2, -3, 45, 21, 109]) == 2
