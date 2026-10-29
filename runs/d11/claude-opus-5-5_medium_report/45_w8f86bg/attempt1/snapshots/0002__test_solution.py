import pytest

from solution import is_prime


@pytest.mark.parametrize("n", [6, 4, 1])
def test_docstring_non_primes(n):
    assert is_prime(n) is False


@pytest.mark.parametrize("n", [101, 11, 13441, 61])
def test_docstring_primes(n):
    assert is_prime(n) is True


@pytest.mark.parametrize("n", [2, 3, 5, 7, 13, 17, 19, 23, 29, 97, 7919])
def test_small_and_medium_primes(n):
    assert is_prime(n) is True


@pytest.mark.parametrize("n", [0, 1, 4, 8, 9, 15, 25, 49, 121, 169, 1001, 7917])
def test_composites_and_non_primes(n):
    assert is_prime(n) is False


@pytest.mark.parametrize("n", [-1, -2, -7, -100])
def test_negative_numbers_are_not_prime(n):
    assert is_prime(n) is False


def test_square_of_prime_is_not_prime():
    assert is_prime(97 * 97) is False


def test_product_of_two_large_primes_is_not_prime():
    assert is_prime(101 * 103) is False


def test_matches_reference_for_range():
    def reference(n):
        if n < 2:
            return False
        return all(n % d for d in range(2, int(n ** 0.5) + 1))

    for n in range(-5, 500):
        assert is_prime(n) == reference(n), n
