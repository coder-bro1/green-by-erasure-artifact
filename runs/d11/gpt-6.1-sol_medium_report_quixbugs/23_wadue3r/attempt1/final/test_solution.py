"""Tests for the documented prime factorization contract."""

from math import isqrt, prod

import pytest

from solution import get_factors


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (1, []),
        (2, [2]),
        (3, [3]),
        (4, [2, 2]),
        (9, [3, 3]),
        (25, [5, 5]),
        (49, [7, 7]),
        (121, [11, 11]),
        (100, [2, 2, 5, 5]),
        (101, [101]),
        (97, [97]),
        (15, [3, 5]),
        (77, [7, 11]),
        (221, [13, 17]),
        (360, [2, 2, 2, 3, 3, 5]),
        (2310, [2, 3, 5, 7, 11]),
        (2**20, [2] * 20),
        (3**10, [3] * 10),
        (5**8, [5] * 8),
    ],
)
def test_known_factorizations(n, expected):
    assert get_factors(n) == expected


@pytest.mark.parametrize("n", range(1, 301))
def test_factorization_contract(n):
    factors = get_factors(n)

    assert isinstance(factors, list)
    assert factors == sorted(factors)
    assert prod(factors) == n
    for factor in factors:
        assert isinstance(factor, int)
        assert factor >= 2
        assert all(factor % divisor for divisor in range(2, isqrt(factor) + 1))


@pytest.mark.xfail(
    strict=True,
    raises=OverflowError,
    reason="The documented integer domain is unbounded, but n ** 0.5 overflows for 2**1024.",
)
def test_integer_beyond_float_range():
    # The documented precondition places no upper bound on Python integers.
    assert get_factors(2**1024) == [2] * 1024
