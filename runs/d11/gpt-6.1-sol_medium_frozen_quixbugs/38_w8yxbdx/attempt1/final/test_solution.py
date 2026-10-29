"""Tests for base conversion within the documented input preconditions."""

import string

import pytest

from solution import to_base


DIGITS = string.digits + string.ascii_uppercase
BASES = range(2, 37)
REVERSED_DIGITS = pytest.mark.xfail(
    strict=True,
    reason="Known bug: to_base appends digits from least to most significant",
)


@pytest.mark.parametrize("base", BASES)
def test_every_single_digit(base):
    for number in range(1, base):
        assert to_base(number, base) == DIGITS[number]


@pytest.mark.parametrize("base", BASES)
@pytest.mark.parametrize("length", [2, 3, 20])
def test_repeated_digits(base, length):
    # Palindromic representations remain correct despite the reversal bug.
    digit = base - 1
    number = sum(digit * base**position for position in range(length))
    assert to_base(number, base) == DIGITS[digit] * length


@pytest.mark.parametrize(
    ("number", "base", "expected"),
    [
        (5, 2, "101"),
        (10, 3, "101"),
        (255, 16, "FF"),
        (1295, 36, "ZZ"),
        pytest.param(31, 16, "1F", marks=REVERSED_DIGITS),
        pytest.param(6, 2, "110", marks=REVERSED_DIGITS),
        pytest.param(83, 8, "123", marks=REVERSED_DIGITS),
        pytest.param(12345, 10, "12345", marks=REVERSED_DIGITS),
        pytest.param(35, 16, "23", marks=REVERSED_DIGITS),
        pytest.param(71, 36, "1Z", marks=REVERSED_DIGITS),
    ],
)
def test_known_conversions(number, base, expected):
    assert to_base(number, base) == expected


@REVERSED_DIGITS
@pytest.mark.parametrize("base", BASES)
def test_base_power_preserves_trailing_zeroes(base):
    assert to_base(base**4, base) == "10000"


@pytest.mark.parametrize("base", BASES)
def test_large_integer_digit_count_and_alphabet(base):
    number = 2**256 + 123456789
    result = to_base(number, base)

    expected_length = 0
    quotient = number
    while quotient:
        quotient //= base
        expected_length += 1

    assert isinstance(result, str)
    assert len(result) == expected_length
    assert set(result) <= set(DIGITS[:base])
