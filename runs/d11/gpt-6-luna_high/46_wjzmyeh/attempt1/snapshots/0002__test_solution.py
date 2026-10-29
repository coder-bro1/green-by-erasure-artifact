import pytest

from solution import is_prime


@pytest.mark.parametrize("n", [-10, -1, 0, 1])
def test_numbers_less_than_two_are_not_prime(n):
    assert is_prime(n) is False


@pytest.mark.parametrize("n", [2, 3, 5, 11, 61, 101, 13441])
def test_primes_are_prime(n):
    assert is_prime(n) is True


@pytest.mark.parametrize("n", [4, 6, 9, 25, 100, 13440])
def test_composites_are_not_prime(n):
    assert is_prime(n) is False


def test_square_of_prime_is_not_prime():
    assert is_prime(49) is False
