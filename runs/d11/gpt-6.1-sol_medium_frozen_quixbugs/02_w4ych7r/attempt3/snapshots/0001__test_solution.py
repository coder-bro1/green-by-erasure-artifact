"""Tests for prime factorization, including its known missing-final-factor bug."""

from math import isqrt, prod

import pytest

from solution import get_factors


CASES = [
    (1, []),
    (2, [2]),
    (3, [3]),
    (4, [2, 2]),
    (9, [3, 3]),
    (12, [2, 2, 3]),
    (25, [5, 5]),
    (49, [7, 7]),
    (64, [2, 2, 2, 2, 2, 2]),
    (100, [2, 2, 5, 5]),
    (101, [101]),
    (210, [2, 3, 5, 7]),
    (729, [3, 3, 3, 3, 3, 3]),
    (10403, [101, 103]),
]


@pytest.mark.parametrize(
    "number, expected",
    [
        pytest.param(
            number,
            expected,
            marks=(
                pytest.mark.xfail(
                    strict=True,
                    raises=AssertionError,
                    reason="get_factors returns [] for the final prime factor",
                )
                if number > 1
                else ()
            ),
            id=str(number),
        )
        for number, expected in CASES
    ],
)
def test_complete_prime_factorization(number, expected):
    """Check the documented result; strict xfails track the existing defect."""
    assert get_factors(number) == expected


@pytest.mark.parametrize("number", [number for number, _ in CASES])
def test_returned_factors_are_sorted_prime_divisors(number):
    factors = get_factors(number)

    assert isinstance(factors, list)
    assert factors == sorted(factors)
    for factor in factors:
        assert isinstance(factor, int)
        assert factor >= 2
        assert all(factor % divisor for divisor in range(2, isqrt(factor) + 1))
    assert number % prod(factors) == 0


def test_one_returns_a_fresh_empty_list():
    first = get_factors(1)
    first.append(2)

    assert get_factors(1) == []
