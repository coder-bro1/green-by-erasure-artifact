import pytest

from solution import is_prime


@pytest.mark.parametrize("n", [-100, -7, -1, 0, 1])
def test_numbers_below_two_are_not_prime(n):
    assert is_prime(n) is False


@pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 29, 61, 97, 101, 13441])
def test_prime_numbers(n):
    assert is_prime(n) is True


@pytest.mark.parametrize("n", [4, 6, 8, 9, 15, 21, 25, 49, 77, 121, 169, 221])
def test_composite_numbers(n):
    assert is_prime(n) is False


def test_matches_sieve_for_small_nonnegative_integers():
    limit = 300
    prime_flags = [True] * (limit + 1)
    prime_flags[0] = prime_flags[1] = False
    for prime in range(2, limit + 1):
        if prime_flags[prime]:
            for multiple in range(prime * prime, limit + 1, prime):
                prime_flags[multiple] = False

    for n, expected in enumerate(prime_flags):
        assert is_prime(n) is expected, f"Incorrect primality result for {n}"
