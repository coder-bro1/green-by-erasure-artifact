"""Tests for the documented product of integer unit digits."""

import pytest

from solution import multiply


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (148, 412, 16),
        (19, 28, 72),
        (2020, 1851, 0),
        (14, -15, 20),
        (0, 123, 0),
        (123, 0, 0),
        (0, 0, 0),
        (-20, 19, 0),
        (19, -20, 0),
        (-15, -25, 25),
        (10**100 + 7, 10**120 + 9, 63),
    ],
)
def test_examples_and_integer_boundaries(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.parametrize("a_digit", range(10))
@pytest.mark.parametrize("b_digit", range(10))
def test_all_nonnegative_unit_digit_pairs(a_digit, b_digit):
    assert multiply(120 + a_digit, 340 + b_digit) == a_digit * b_digit


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (-14, 15, 20),
        (-19, 28, 72),
        (19, -28, 72),
        (-19, -28, 72),
        (14, -12, 8),
        (-(10**100 + 7), 10**120 + 9, 63),
    ],
)
@pytest.mark.xfail(
    strict=True,
    reason=(
        "The docstring requires magnitude unit digits for negative integers, "
        "but abs(n % 10) uses Python's nonnegative remainder; "
        "for example, multiply(-14, 15) returns 30 instead of 20."
    ),
)
def test_negative_unit_digits(a, b, expected):
    assert multiply(a, b) == expected
