"""Tests for solution.get_factors.

NOTE: solution.py contains a known bug -- its final statement is `return []`
instead of `return [n]`, so the last (largest) prime factor is dropped for
every n > 1. Tests asserting the documented behaviour that the bug breaks are
marked xfail(strict=True): they will start failing (XPASS -> error) as soon as
the bug is fixed, signalling that the markers should be removed.
"""
import math

import pytest

from solution import get_factors

BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py bug: trailing `return []` should be `return [n]`",
)


def is_prime(k):
    return k >= 2 and all(k % d for d in range(2, math.isqrt(k) + 1))


# --- Behaviour that is correct today -------------------------------------

def test_one_has_no_factors():
    assert get_factors(1) == []


def test_returns_list():
    assert isinstance(get_factors(12), list)


@pytest.mark.parametrize("n", list(range(1, 200)) + [1024, 9973, 123456, 600851475143])
def test_partial_result_properties(n):
    """Holds even with the bug: output is sorted, made of primes, and
    its product divides n."""
    factors = get_factors(n)
    assert factors == sorted(factors)
    assert all(is_prime(f) for f in factors)
    assert n % math.prod(factors) == 0


# --- Documented behaviour (broken by the bug) -----------------------------

@BUG
@pytest.mark.parametrize(
    "n, expected",
    [
        (2, [2]),
        (3, [3]),
        (4, [2, 2]),
        (12, [2, 2, 3]),
        (100, [2, 2, 5, 5]),          # docstring example
        (101, [101]),                 # docstring example
        (1024, [2] * 10),
        (9973, [9973]),
        (2 * 3 * 5 * 7 * 11 * 13, [2, 3, 5, 7, 11, 13]),
        (600851475143, [71, 839, 1471, 6857]),
    ],
)
def test_documented_examples(n, expected):
    assert get_factors(n) == expected


@BUG
@pytest.mark.parametrize("n", range(2, 300))
def test_product_equals_n(n):
    assert math.prod(get_factors(n)) == n


@BUG
@pytest.mark.parametrize("p", [2, 3, 5, 7, 13, 97, 7919])
def test_prime_returns_itself(p):
    assert get_factors(p) == [p]
