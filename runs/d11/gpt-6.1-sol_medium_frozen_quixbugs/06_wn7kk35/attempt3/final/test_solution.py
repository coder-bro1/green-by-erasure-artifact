"""Tests for sieve's documented contract, including its known defect."""

import pytest

from solution import sieve


@pytest.mark.parametrize("upper_bound", [-10, -1, 0, 1])
def test_bounds_below_two_have_no_primes(upper_bound):
    assert sieve(upper_bound) == []


@pytest.mark.parametrize("upper_bound", [None, "10", 2.5, [10]])
def test_non_integer_bounds_raise_type_error(upper_bound):
    with pytest.raises(TypeError):
        sieve(upper_bound)


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="The empty prime list makes any(...) false, so no prime is appended.",
)
@pytest.mark.parametrize(
    ("upper_bound", "expected"),
    [
        (2, [2]),
        (3, [2, 3]),
        (4, [2, 3]),
        (10, [2, 3, 5, 7]),
        (25, [2, 3, 5, 7, 11, 13, 17, 19, 23]),
        (29, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]),
        (49, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]),
    ],
)
def test_primes_up_to_and_including_bound(upper_bound, expected):
    assert sieve(upper_bound) == expected


def test_calls_return_independent_lists():
    first = sieve(1)
    first.append(99)

    assert sieve(1) == []
