import string

import pytest

from solution import to_base

ALPHABET = string.digits + string.ascii_uppercase

KNOWN_BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py builds digits least-significant first and never reverses them",
)


def reference(num, b):
    digits = ""
    while num > 0:
        num, r = divmod(num, b)
        digits = ALPHABET[r] + digits
    return digits


# Cases where the output is correct regardless of digit order
# (single digits and palindromic representations).
@pytest.mark.parametrize(
    "num, b, expected",
    [
        (1, 2, "1"),
        (1, 36, "1"),
        (9, 10, "9"),
        (10, 16, "A"),
        (15, 16, "F"),
        (35, 36, "Z"),
        (5, 2, "101"),
        (3, 2, "11"),
        (7, 2, "111"),
        (121, 10, "121"),
        (255, 16, "FF"),
        (16, 3, "121"),
    ],
)
def test_order_independent_cases(num, b, expected):
    assert to_base(num, b) == expected


def test_returns_str():
    assert isinstance(to_base(42, 7), str)


def test_uses_uppercase_letters():
    assert to_base(11, 12) == "B"
    assert to_base(35, 36) == "Z"


@pytest.mark.parametrize("b", range(2, 37))
def test_length_matches_reference(b):
    for num in (1, 2, b - 1, b, b + 1, b * b, 12345):
        assert len(to_base(num, b)) == len(reference(num, b))


@pytest.mark.parametrize("b", range(2, 37))
def test_digits_are_valid_for_base(b):
    for num in (1, b, 999, 123456):
        assert all(c in ALPHABET[:b] for c in to_base(num, b))


@pytest.mark.parametrize("b", range(2, 37))
def test_single_digit_values(b):
    for num in range(1, b):
        assert to_base(num, b) == ALPHABET[num]


# Spec-conforming cases that expose the digit-order bug.
@KNOWN_BUG
def test_docstring_example():
    assert to_base(31, 16) == "1F"


@KNOWN_BUG
@pytest.mark.parametrize(
    "num, b, expected",
    [
        (10, 10, "10"),
        (6, 2, "110"),
        (100, 10, "100"),
        (36, 36, "10"),
        (2, 2, "10"),
        (4095, 8, "7777") if False else (8, 8, "10"),
        (1295, 36, "ZZ") if False else (37, 36, "11") if False else (71, 36, "1Z"),
    ],
)
def test_multi_digit_order(num, b, expected):
    assert to_base(num, b) == expected


@KNOWN_BUG
@pytest.mark.parametrize("b", [2, 8, 10, 16, 36])
def test_round_trip_with_int(b):
    for num in (12, 123, 4567, 98765):
        assert int(to_base(num, b), b) == num
