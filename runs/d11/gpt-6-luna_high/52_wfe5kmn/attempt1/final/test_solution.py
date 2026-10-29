import pytest

from solution import is_prime


@pytest.mark.parametrize("number", [-10, -1, 0, 1])
def test_numbers_below_two_are_not_prime(number):
    assert is_prime(number) is False


@pytest.mark.parametrize("number", [2, 3, 5, 11, 61, 101, 13441])
def test_primes_are_prime(number):
    assert is_prime(number) is True


@pytest.mark.parametrize("number", [4, 6, 9, 25, 100, 13441 * 3])
def test_composites_are_not_prime(number):
    assert is_prime(number) is False
