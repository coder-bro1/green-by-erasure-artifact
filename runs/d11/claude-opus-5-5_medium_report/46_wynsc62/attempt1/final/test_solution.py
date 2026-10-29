import pytest

from solution import is_prime

LOOP_BUG = (
    "is_prime's trial-division loop starts at k=1 and n % 1 == 0 for every n, "
    "so every n >= 3 (including primes) is reported as not prime"
)
ONE_BUG = (
    "is_prime(1) returns True: the guard is `n < 1` instead of `n < 2`, and the "
    "loop range(1, 0) is empty, so 1 falls through to `return True`"
)


# Docstring examples: non-primes (these pass)
@pytest.mark.parametrize("n", [6, 4])
def test_docstring_composites(n):
    assert is_prime(n) is False


# Docstring examples: primes (fail because of the loop bug)
@pytest.mark.xfail(strict=True, reason=LOOP_BUG)
@pytest.mark.parametrize("n", [101, 11, 13441, 61])
def test_docstring_primes(n):
    assert is_prime(n) is True


@pytest.mark.xfail(strict=True, reason=ONE_BUG)
def test_one_is_not_prime():
    assert is_prime(1) is False


def test_two_is_prime():
    assert is_prime(2) is True


@pytest.mark.xfail(strict=True, reason=LOOP_BUG)
@pytest.mark.parametrize("n", [3, 5, 7, 97, 7919])
def test_small_and_larger_primes(n):
    assert is_prime(n) is True


@pytest.mark.parametrize("n", [0, -1, -7, -13])
def test_zero_and_negatives_are_not_prime(n):
    assert is_prime(n) is False


@pytest.mark.parametrize("n", [8, 9, 15, 25, 49, 100, 121, 7917])
def test_other_composites(n):
    assert is_prime(n) is False


def test_returns_bool():
    assert isinstance(is_prime(4), bool)
    assert isinstance(is_prime(2), bool)
