"""Tests for the documented inclusive prime-sieve contract."""

from math import isqrt

import pytest

from solution import sieve


@pytest.mark.parametrize(
    ("upper_bound", "expected"),
    [
        (1, []),
        (2, [2]),
        (3, [2, 3]),
        (4, [2, 3]),
        (9, [2, 3, 5, 7]),
        (10, [2, 3, 5, 7]),
        (11, [2, 3, 5, 7, 11]),
        (25, [2, 3, 5, 7, 11, 13, 17, 19, 23]),
        (29, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]),
        (30, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]),
        (49, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]),
    ],
)
def test_sieve_documented_examples(upper_bound, expected):
    """Include prime endpoints and exclude composites, including squares."""
    result = sieve(upper_bound)
    assert isinstance(result, list)
    assert result == expected


@pytest.mark.parametrize("upper_bound", [100, 257, 1000])
def test_sieve_matches_independent_trial_division(upper_bound):
    """Check completeness and primality using all possible small divisors."""
    expected = [
        candidate
        for candidate in range(2, upper_bound + 1)
        if all(
            candidate % divisor != 0
            for divisor in range(2, isqrt(candidate) + 1)
        )
    ]
    result = sieve(upper_bound)
    assert isinstance(result, list)
    assert result == expected
