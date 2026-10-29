"""Tests for solution.is_prime.

Tests are written against the documented contract (the docstring). The
current implementation has a bug: its trial-division loop starts at k=1
(``range(1, n - 1)``), and every n is divisible by 1, so it returns False
for every n >= 3, including primes. Because the loop is empty for n=1, it
also returns True for 1.

Cases that the bug breaks are marked ``xfail(strict=True)``. They are
reported as xfail now, and the run fails with XPASS once the bug is fixed,
which is the signal to remove the markers.
"""
import pytest

from solution import is_prime

BUG = pytest.mark.xfail(
    strict=True,
    reason="Bug: loop starts at k=1, so n % 1 == 0 rejects every n >= 3 "
    "and 1 is wrongly accepted",
)


# Behaviour that is correct today.

@pytest.mark.parametrize("n", [0, -1, -2, -7, -101])
def test_non_positive_numbers_are_not_prime(n):
    assert is_prime(n) is False


def test_two_is_prime():
    assert is_prime(2) is True


@pytest.mark.parametrize("n", [4, 6, 8, 9, 15, 25, 49, 100, 13440])
def test_composites_are_not_prime(n):
    assert is_prime(n) is False


def test_returns_bool():
    assert isinstance(is_prime(2), bool)
    assert isinstance(is_prime(4), bool)
    assert isinstance(is_prime(0), bool)


# Documented behaviour that is broken by the bug.

@BUG
def test_one_is_not_prime():
    assert is_prime(1) is False


@BUG
@pytest.mark.parametrize("n", [3, 5, 7, 11, 13, 61, 97, 101, 13441])
def test_primes_are_prime(n):
    assert is_prime(n) is True


@BUG
def test_docstring_examples():
    expected = {6: False, 101: True, 11: True, 13441: True,
                61: True, 4: False, 1: False}
    assert {n: is_prime(n) for n in expected} == expected
