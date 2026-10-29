"""Tests for the documented integer greatest-common-divisor operation."""

import doctest
import math

import pytest

import solution
from solution import greatest_common_divisor


def test_docstring_examples():
    result = doctest.testmod(solution)
    assert result.attempted == 2
    assert result.failed == 0


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (3, 5, 1),
        (25, 15, 5),
        (15, 25, 5),
        (12, 18, 6),
        (18, 12, 6),
        (7, 7, 7),
        (1, 99, 1),
        (99, 1, 1),
        (21, 7, 7),
        (7, 21, 7),
        (13, 17, 1),
        (0, 0, 0),
        (0, 9, 9),
        (9, 0, 9),
        (-25, 15, 5),
        (-3, 5, 1),
        (10**100, 10**80, 10**80),
        (2**200 * 3, 2**150 * 5, 2**150),
        (10**100 + 1, 10**100, 1),
    ],
)
def test_greatest_common_divisor(a, b, expected):
    assert greatest_common_divisor(a, b) == expected


def test_nonnegative_inputs_match_standard_library():
    for a in range(51):
        for b in range(51):
            assert greatest_common_divisor(a, b) == math.gcd(a, b), (a, b)


@pytest.mark.xfail(
    strict=True,
    reason=(
        "The documented GCD of integers must be nonnegative, but solution.py "
        "returns a negative result when b < 0 or when a < 0 and b == 0."
    ),
)
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (25, -15, 5),
        (-25, -15, 5),
        (3, -5, 1),
        (0, -9, 9),
        (-9, 0, 9),
    ],
)
def test_greatest_common_divisor_is_nonnegative_for_signed_integers(a, b, expected):
    assert greatest_common_divisor(a, b) == expected
