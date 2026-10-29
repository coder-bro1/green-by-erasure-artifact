"""Tests for the primality behavior documented by solution.is_prime."""

import pytest

from solution import is_prime


@pytest.mark.parametrize("n", [-101, -7, -2, -1, 0])
def test_nonpositive_integers_are_not_prime(n):
    assert is_prime(n) is False


def test_two_is_prime():
    assert is_prime(2) is True


@pytest.mark.parametrize("n", [4, 6, 8, 9, 15, 25, 49, 100, 121, 1000])
def test_composites_are_not_prime(n):
    assert is_prime(n) is False


@pytest.mark.parametrize("n", [3, 5, 7, 11, 61, 97, 101, 13441])
def test_primes_greater_than_two_are_prime(n):
    assert is_prime(n) is True


def test_one_is_not_prime():
    assert is_prime(1) is False
