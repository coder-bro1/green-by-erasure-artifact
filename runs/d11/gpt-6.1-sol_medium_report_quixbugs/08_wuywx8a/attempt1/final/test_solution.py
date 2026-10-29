"""Tests for to_base within its documented input preconditions."""

import pytest

from solution import to_base


@pytest.mark.parametrize(
    "num, base, expected",
    [
        (31, 16, "1F"),  # The docstring example.
        (1, 2, "1"),
        (2, 2, "10"),
        (42, 2, "101010"),
        (255, 2, "11111111"),
        (10, 3, "101"),
        (64, 8, "100"),
        (511, 8, "777"),
        (1234567890, 10, "1234567890"),
        (10, 11, "A"),
        (11, 12, "B"),
        (255, 16, "FF"),
        (4096, 16, "1000"),
        (65535, 16, "FFFF"),
        (34, 35, "Y"),
        (35, 36, "Z"),
        (36, 36, "10"),
        (71, 36, "1Z"),
        (1295, 36, "ZZ"),
        (1296, 36, "100"),
        (2**128 - 1, 16, "F" * 32),
        (10**100 + 1, 10, "1" + "0" * 99 + "1"),
    ],
)
def test_known_conversions(num, base, expected):
    assert to_base(num, base) == expected


@pytest.mark.parametrize("base", range(2, 37))
def test_every_single_digit(base):
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for num in range(1, base):
        assert to_base(num, base) == alphabet[num]


@pytest.mark.parametrize("base", range(2, 37))
@pytest.mark.parametrize("exponent", [1, 2, 5, 20])
def test_digit_boundaries(base, exponent):
    power = base**exponent
    largest_digit = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[base - 1]
    assert to_base(power - 1, base) == largest_digit * exponent
    assert to_base(power, base) == "1" + "0" * exponent
    assert to_base(power + 1, base) == "1" + "0" * (exponent - 1) + "1"


@pytest.mark.parametrize("base", range(2, 37))
@pytest.mark.parametrize("num", [1, 37, 1000, 123456789, 2**256 + 12345])
def test_representation_round_trips_through_python(num, base):
    result = to_base(num, base)

    assert isinstance(result, str)
    assert result
    assert not result.startswith("0")
    assert result == result.upper()
    assert set(result) <= set("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:base])
    assert int(result, base) == num
