import pytest

from solution import is_prime


@pytest.mark.parametrize(
    "number, expected",
    [
        (6, False),
        (101, True),
        (11, True),
        (13441, True),
        (61, True),
        (4, False),
        (1, False),
    ],
)
def test_docstring_examples(number, expected):
    assert is_prime(number) is expected


@pytest.mark.parametrize("number", [-100, -7, -2, -1, 0])
def test_numbers_below_two_are_not_prime(number):
    assert is_prime(number) is False


@pytest.mark.parametrize("number", [2, 3, 5, 7, 13, 17, 29, 97, 997])
def test_primes(number):
    assert is_prime(number) is True


@pytest.mark.parametrize(
    "number", [8, 9, 15, 21, 25, 27, 35, 49, 77, 121, 143, 169, 221, 561, 1024]
)
def test_composites_including_squares_and_carmichael_number(number):
    assert is_prime(number) is False


def test_matches_sieve_for_integers_up_to_one_thousand():
    """Use a sieve as an independent reference for the full small-integer range."""
    limit = 1000
    prime_flags = [True] * (limit + 1)
    prime_flags[0] = prime_flags[1] = False
    for candidate in range(2, limit + 1):
        if prime_flags[candidate]:
            for multiple in range(candidate * candidate, limit + 1, candidate):
                prime_flags[multiple] = False

    for number, expected in enumerate(prime_flags):
        assert is_prime(number) is expected, f"Incorrect primality for {number}"
