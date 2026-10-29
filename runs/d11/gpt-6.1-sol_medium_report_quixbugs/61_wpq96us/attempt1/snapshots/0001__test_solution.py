"""Tests for the documented nonnegative-integer inputs to gcd."""

import math

import pytest

from solution import gcd


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (35, 21, 7),  # The docstring example.
        (21, 35, 7),
        (0, 1, 1),
        (1, 0, 1),
        (0, 42, 42),
        (42, 0, 42),
        (1, 1, 1),
        (42, 42, 42),
        (1, 99, 1),
        (99, 1, 1),
        (13, 17, 1),
        (8, 9, 1),
        (12, 36, 12),
        (36, 12, 12),
        (48, 18, 6),
        (54, 24, 6),
        (270, 192, 6),
        (2**200, 2**150, 2**150),
        (3 * 10**100, 7 * 10**100, 10**100),
        (10**100, 10**100 + 1, 1),
    ],
)
def test_gcd_documented_examples_and_edge_cases(a, b, expected):
    result = gcd(a, b)
    assert type(result) is int
    assert result == expected


@pytest.mark.parametrize("a", range(31))
def test_gcd_matches_standard_library_for_small_nonnegative_inputs(a):
    for b in range(31):
        # With both inputs zero there is no greatest integer divisor, so
        # the docstring does not define an expected result for that pair.
        if a == b == 0:
            continue
        result = gcd(a, b)
        assert result == math.gcd(a, b), (a, b)
        assert a % result == 0, (a, b)
        assert b % result == 0, (a, b)
