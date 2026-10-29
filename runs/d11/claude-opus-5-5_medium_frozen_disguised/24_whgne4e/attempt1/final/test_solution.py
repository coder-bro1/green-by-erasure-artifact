import doctest

import pytest

import solution
from solution import has_no_divisors

PRIMES = [2, 3, 5, 7, 11, 13, 29, 97, 7919]
COMPOSITES = [4, 6, 8, 9, 15, 25, 49, 91, 100, 7917]
BELOW_TWO = [-10, -2, -1, 0, 1]


@pytest.mark.parametrize("n", PRIMES)
def test_primes_return_true(n):
    assert has_no_divisors(n) is True


@pytest.mark.parametrize("n", COMPOSITES)
def test_composites_return_false(n):
    assert has_no_divisors(n) is False


@pytest.mark.parametrize("n", BELOW_TWO)
def test_numbers_below_two_are_not_prime(n):
    assert has_no_divisors(n) is False


def test_matches_reference_up_to_200():
    def ref(n):
        return n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1))

    for n in range(-5, 201):
        assert has_no_divisors(n) == ref(n), n


def test_docstring_examples():
    result = doctest.testmod(solution)
    assert result.failed == 0
