import math

import pytest

from solution import common_factor_max


@pytest.mark.parametrize(
    "p, q, expected",
    [
        (12, 18, 6),   # docstring example
        (7, 13, 1),    # docstring example (coprime)
        (18, 12, 6),   # argument order should not matter
        (100, 10, 10), # one divides the other
        (17, 17, 17),  # equal inputs
        (1, 999, 1),
        (270, 192, 6),
        (2**10 * 3, 2**7 * 5, 2**7),
    ],
)
def test_known_values(p, q, expected):
    assert common_factor_max(p, q) == expected


def test_zero_second_argument():
    assert common_factor_max(5, 0) == 5


def test_zero_first_argument():
    assert common_factor_max(0, 5) == 5


def test_matches_math_gcd_for_range():
    for p in range(1, 40):
        for q in range(1, 40):
            assert common_factor_max(p, q) == math.gcd(p, q), (p, q)


def test_result_divides_both_inputs():
    p, q = 123456, 7890
    g = common_factor_max(p, q)
    assert g > 0
    assert p % g == 0 and q % g == 0
