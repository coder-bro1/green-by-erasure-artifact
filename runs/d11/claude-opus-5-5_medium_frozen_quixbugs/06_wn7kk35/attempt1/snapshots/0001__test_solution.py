"""Tests for solution.sieve (Sieve of Eratosthenes).

NOTE: solution.py currently has a bug: the primality check uses
`any(n % p > 0 for p in primes)` on an initially empty list, so `any(...)`
is always False and no number is ever appended -- sieve() always returns [].
The correct check is `all(...)`.

Tests that specify correct behaviour but fail because of this bug are marked
`xfail(strict=True)`. Once the bug is fixed they will XPASS, which strict mode
reports as a failure -- remove the BUG marker at that point.
"""

import pytest

from solution import sieve

BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py bug: any() over empty primes list never appends; should be all()",
)


def reference_primes(limit):
    """Simple trial-division reference implementation."""
    return [
        n
        for n in range(2, limit + 1)
        if all(n % d for d in range(2, int(n ** 0.5) + 1))
    ]


# --- Behaviour that holds regardless of the bug -------------------------------

def test_returns_list():
    assert isinstance(sieve(10), list)


@pytest.mark.parametrize("limit", [0, 1])
def test_no_primes_below_two(limit):
    assert sieve(limit) == []


def test_negative_bound_returns_empty():
    assert sieve(-5) == []


@pytest.mark.parametrize("limit", [0, 1, 2, 10, 50, 100])
def test_result_is_sorted_and_unique(limit):
    result = sieve(limit)
    assert result == sorted(set(result))


@pytest.mark.parametrize("limit", [2, 10, 50, 100])
def test_all_results_within_bounds(limit):
    assert all(2 <= p <= limit for p in sieve(limit))


@pytest.mark.parametrize("limit", [10, 100])
def test_no_composites_returned(limit):
    expected = set(reference_primes(limit))
    assert set(sieve(limit)) <= expected


# --- Correct behaviour, currently broken by the bug --------------------------

@BUG
def test_two_is_prime():
    assert sieve(2) == [2]


@BUG
def test_three():
    assert sieve(3) == [2, 3]


@BUG
def test_small_bound():
    assert sieve(10) == [2, 3, 5, 7]


@BUG
def test_bound_is_inclusive_when_prime():
    assert sieve(13)[-1] == 13


@BUG
def test_bound_not_prime():
    assert sieve(20) == [2, 3, 5, 7, 11, 13, 17, 19]


@BUG
def test_primes_up_to_100():
    assert sieve(100) == [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
        53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
    ]


@BUG
def test_count_up_to_1000():
    assert len(sieve(1000)) == 168


@BUG
@pytest.mark.parametrize("limit", [30, 97, 500])
def test_matches_reference(limit):
    assert sieve(limit) == reference_primes(limit)
