import math

import pytest

from solution import greatest_common_divisor


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (3, 5, 1),        # docstring example
        (25, 15, 5),      # docstring example
        (15, 25, 5),      # argument order reversed
        (49, 14, 7),
        (144, 60, 12),
        (7, 7, 7),        # equal arguments
        (1, 100, 1),
        (12, 36, 12),     # one divides the other
        (17, 13, 1),      # coprime primes
        (2**40, 2**20, 2**20),
        (123456789, 987654321, 9),
    ],
)
def test_positive_inputs(a, b, expected):
    assert greatest_common_divisor(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (0, 5, 5),
        (5, 0, 5),
        (0, 0, 0),
    ],
)
def test_zero_inputs(a, b, expected):
    assert greatest_common_divisor(a, b) == expected


def test_result_divides_both_and_matches_math_gcd():
    for a in range(0, 60):
        for b in range(0, 60):
            g = greatest_common_divisor(a, b)
            assert g == math.gcd(a, b)
            if g:
                assert a % g == 0 and b % g == 0


def test_negative_first_argument():
    assert greatest_common_divisor(-4, 6) == 2


@pytest.mark.xfail(
    strict=True,
    reason="Euclid with Python's % keeps the divisor's sign, so a negative b "
    "can yield a negative result (-2) instead of the greatest divisor (2)",
)
def test_negative_second_argument():
    assert greatest_common_divisor(4, -6) == 2


@pytest.mark.xfail(
    strict=True,
    reason="both arguments negative returns a negative value (-2), not the greatest divisor 2",
)
def test_both_negative():
    assert greatest_common_divisor(-4, -6) == 2
