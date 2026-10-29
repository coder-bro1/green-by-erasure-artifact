import math

import pytest

from solution import greatest_common_divisor


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (3, 5, 1),
        (25, 15, 5),
        (48, 18, 6),
        (18, 48, 6),
        (7, 7, 7),
        (12, 36, 12),
        (1, 100, 1),
        (0, 0, 0),
        (0, 9, 9),
        (9, 0, 9),
        (-48, 18, 6),
        (48, -18, 6),
        (-48, -18, 6),
        (-9, 0, 9),
        (0, -9, 9),
        (2**100, 2**80, 2**80),
        (10**100, 10**100 + 1, 1),
    ],
)
def test_greatest_common_divisor(a, b, expected):
    assert greatest_common_divisor(a, b) == expected


def test_greatest_common_divisor_matches_math_gcd():
    for a in range(-25, 26):
        for b in range(-25, 26):
            assert greatest_common_divisor(a, b) == math.gcd(a, b), (a, b)
