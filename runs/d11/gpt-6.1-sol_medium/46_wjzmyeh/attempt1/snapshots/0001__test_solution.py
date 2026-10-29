import pytest

from solution import is_prime


@pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 61, 101, 13441])
def test_prime_numbers(n):
    assert is_prime(n) is True


@pytest.mark.parametrize(
    "n",
    [-100, -2, -1, 0, 1, 4, 6, 8, 9, 15, 25, 49, 121, 169, 997 * 997],
)
def test_non_prime_numbers(n):
    assert is_prime(n) is False


def test_numbers_against_sieve():
    """Check consecutive integers against an independent sieve of primes."""
    limit = 500
    primes = set(range(2, limit + 1))
    for candidate in range(2, limit + 1):
        if candidate in primes:
            primes.difference_update(range(candidate * 2, limit + 1, candidate))

    for n in range(limit + 1):
        assert is_prime(n) is (n in primes), f"Incorrect result for {n}"
