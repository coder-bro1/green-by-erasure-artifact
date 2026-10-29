"""Tests for solution.gcd.

NOTE: solution.gcd has a bug. Its recursive step is ``gcd(a % b, b)`` instead
of ``gcd(b, a % b)``, so every call with ``b != 0`` recurses forever and
raises RecursionError. solution.py must not be modified, so the tests that
specify correct behavior for ``b != 0`` are marked strict xfail. Once the bug
is fixed they will XPASS, strict mode will fail the run, and the markers
should then be removed.
"""
import math

import pytest

from solution import gcd

BUG = pytest.mark.xfail(
    raises=RecursionError,
    strict=True,
    reason="bug: recursion is gcd(a % b, b) instead of gcd(b, a % b)",
)


# --- Behavior that works today (base case, b == 0) -------------------------

@pytest.mark.parametrize("a", [0, 1, 2, 7, 35, 10**18])
def test_gcd_with_zero_second_arg_returns_first(a):
    assert gcd(a, 0) == a


def test_gcd_zero_zero_is_zero():
    assert gcd(0, 0) == 0


def test_returns_int():
    assert isinstance(gcd(12, 0), int)


def test_nonzero_b_currently_raises_recursion_error():
    # Pins down the current (buggy) behavior so it can't change unnoticed.
    with pytest.raises(RecursionError):
        gcd(35, 21)


# --- Specification for b != 0 (fails because of the bug) -------------------

@BUG
def test_docstring_example():
    assert gcd(35, 21) == 7


@BUG
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (0, 5, 5),
        (1, 1, 1),
        (12, 18, 6),
        (18, 12, 6),
        (17, 13, 1),       # coprime primes
        (100, 10, 10),     # one divides the other
        (10, 100, 10),
        (7, 7, 7),         # equal arguments
        (2**40, 2**20, 2**20),
        (123456789, 987654321, 9),
    ],
)
def test_known_values(a, b, expected):
    assert gcd(a, b) == expected


@BUG
@pytest.mark.parametrize("a, b", [(48, 180), (270, 192), (1071, 462)])
def test_matches_math_gcd(a, b):
    assert gcd(a, b) == math.gcd(a, b)


@BUG
@pytest.mark.parametrize("a, b", [(48, 180), (9, 28), (0, 4)])
def test_symmetric(a, b):
    assert gcd(a, b) == gcd(b, a)
