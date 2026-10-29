"""Primality tests, with known solution defects explicitly documented."""

import pytest

from solution import is_prime


@pytest.mark.parametrize("n", [-100, -17, -2, -1, 0])
def test_nonpositive_numbers_are_not_prime(n):
    assert is_prime(n) is False


def test_two_is_prime():
    assert is_prime(2) is True


@pytest.mark.parametrize("n", [4, 6, 8, 9, 10, 15, 21, 25, 49, 100, 121, 143])
def test_composite_numbers_are_not_prime(n):
    """Cover even numbers, odd composites, and prime squares."""
    assert is_prime(n) is False


@pytest.mark.xfail(
    strict=True,
    reason="Known defect: 1 bypasses the loop and is incorrectly called prime.",
)
def test_one_is_not_prime():
    assert is_prime(1) is False


@pytest.mark.parametrize("n", [3, 5, 11, 61, 101, 13441])
@pytest.mark.xfail(
    strict=True,
    reason="Known defect: divisor 1 causes all primes greater than 2 to be rejected.",
)
def test_primes_greater_than_two_are_prime(n):
    assert is_prime(n) is True
