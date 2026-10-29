import math

import pytest

from solution import greatest_common_divisor


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (3, 5, 1),
        (25, 15, 5),
        (15, 25, 5),
        (12, 12, 12),
        (1, 100, 1),
        (100, 1, 1),
        (48, 18, 6),
        (20, 100, 20),
        (0, 0, 0),
        (0, 9, 9),
        (9, 0, 9),
        (-25, 15, 5),
        (25, -15, 5),
        (-25, -15, 5),
        (0, -9, 9),
        (-9, 0, 9),
        (2**200, 2**150, 2**150),
        (10**100, 10**100 + 1, 1),
    ],
)
def test_greatest_common_divisor(a, b, expected):
    assert greatest_common_divisor(a, b) == expected


def test_greatest_common_divisor_matches_standard_library():
    for a in range(-20, 21):
        for b in range(-20, 21):
            assert greatest_common_divisor(a, b) == math.gcd(a, b), (a, b)
