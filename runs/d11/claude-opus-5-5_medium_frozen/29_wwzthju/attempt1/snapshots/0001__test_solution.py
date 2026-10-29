"""Tests for solution.largest_divisor.

NOTE: solution.py contains a bug. The loop condition is `n - i == 0` where it
should be `n % i == 0`. Because `range(n)` never yields `n`, that condition is
never true and the function always falls through and returns None.

The spec tests below describe the documented behaviour (largest divisor of n
smaller than n). They are marked xfail(strict=True), so the suite passes while
the bug exists, and the xfail tests start reporting XPASS (failing the run)
once the bug is fixed, which is the signal to remove the markers.
"""
import doctest

import pytest

import solution
from solution import largest_divisor

BUG = "solution.py checks `n - i == 0` instead of `n % i == 0`; always returns None"


# --- Spec tests (documented behaviour) -------------------------------------

@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize(
    "n, expected",
    [
        (15, 5),     # docstring example
        (2, 1),      # smallest prime
        (3, 1),
        (7, 1),      # prime -> 1
        (97, 1),     # larger prime
        (4, 2),
        (10, 5),
        (49, 7),     # square of a prime
        (100, 50),   # even -> n // 2
        (27, 9),
        (1024, 512),
    ],
)
def test_largest_divisor_spec(n, expected):
    assert largest_divisor(n) == expected


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize("n", [6, 12, 35, 81, 360, 997])
def test_result_divides_n_and_is_maximal(n):
    d = largest_divisor(n)
    assert isinstance(d, int)
    assert 1 <= d < n
    assert n % d == 0
    assert all(n % k != 0 for k in range(d + 1, n))


@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_example():
    failures, _ = doctest.testmod(solution)
    assert failures == 0


# --- Current behaviour (pins what the code actually does today) ------------

@pytest.mark.parametrize("n", [2, 3, 15, 49, 100, 1024])
def test_current_behaviour_returns_none(n):
    assert largest_divisor(n) is None


@pytest.mark.parametrize("n", [-5, 0, 1])
def test_degenerate_inputs_do_not_raise(n):
    # range(n) is empty for n <= 0; for n == 1 only i == 0 is checked.
    assert largest_divisor(n) is None
