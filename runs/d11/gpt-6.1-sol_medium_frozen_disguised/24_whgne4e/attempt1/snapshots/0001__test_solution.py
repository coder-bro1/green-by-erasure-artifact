"""Test the documented primality contract, recording known solution defects."""

import pytest

from solution import has_no_divisors


@pytest.mark.parametrize("num", [-100, -7, -1, 0])
def test_nonpositive_numbers_are_not_prime(num):
    assert has_no_divisors(num) is False


def test_two_is_prime():
    assert has_no_divisors(2) is True


@pytest.mark.parametrize("num", [4, 6, 8, 9, 15, 25, 49, 77, 100, 121])
def test_composite_numbers_are_not_prime(num):
    assert has_no_divisors(num) is False


@pytest.mark.xfail(
    strict=True,
    reason="The num < 1 guard incorrectly allows 1 to be classified as prime.",
)
def test_one_is_not_prime():
    assert has_no_divisors(1) is False


@pytest.mark.parametrize("num", [3, 5, 7, 11, 29, 97, 101])
@pytest.mark.xfail(
    strict=True,
    reason="The divisor loop starts at 1, rejecting every prime greater than 2.",
)
def test_primes_greater_than_two_are_prime(num):
    assert has_no_divisors(num) is True
