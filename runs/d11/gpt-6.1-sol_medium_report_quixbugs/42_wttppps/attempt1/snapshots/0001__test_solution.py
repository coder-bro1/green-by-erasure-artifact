"""Tests for to_base within its documented input preconditions."""

import pytest

from solution import to_base


DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


@pytest.mark.parametrize("base", range(2, 37))
@pytest.mark.parametrize("position", ["first", "last"])
def test_single_digit_conversion(base, position):
    number = 1 if position == "first" else base - 1
    assert to_base(number, base) == DIGITS[number]


@pytest.mark.parametrize(
    "number, base, expected",
    [
        (3, 2, "11"),
        (5, 2, "101"),
        (65, 8, "101"),
        (121, 10, "121"),
        (257, 16, "101"),
        (1295, 36, "ZZ"),
        (int("1" * 100, 2), 2, "1" * 100),
    ],
)
def test_palindromic_multidigit_conversion(number, base, expected):
    assert to_base(number, base) == expected


@pytest.mark.parametrize("base", range(2, 37))
def test_base_boundary(base):
    assert to_base(base, base) == "10"


@pytest.mark.parametrize(
    "number, base, expected",
    [
        pytest.param(31, 16, "1F", id="docstring-example"),
        pytest.param(6, 2, "110", id="binary"),
        pytest.param(83, 8, "123", id="octal"),
        pytest.param(12345, 10, "12345", id="decimal"),
        pytest.param(2748, 16, "ABC", id="hexadecimal-uppercase"),
        pytest.param(71, 36, "1Z", id="base-36"),
        pytest.param(1000, 10, "1000", id="trailing-zeroes"),
        pytest.param(2**100, 2, "1" + "0" * 100, id="large-integer"),
    ],
)
def test_nonpalindromic_multidigit_conversion(number, base, expected):
    assert to_base(number, base) == expected
