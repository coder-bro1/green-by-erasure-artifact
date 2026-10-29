"""Tests for the documented largest proper divisor of positive integers.

The contract has a well-defined answer for integers greater than one.
"""

import pytest

from solution import largest_divisor


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        pytest.param(15, 5, id="docstring-example"),
        pytest.param(2, 1, id="smallest-prime"),
        pytest.param(3, 1, id="odd-prime"),
        pytest.param(29, 1, id="larger-prime"),
        pytest.param(97, 1, id="prime-near-one-hundred"),
        pytest.param(4, 2, id="smallest-composite"),
        pytest.param(6, 3, id="even-composite"),
        pytest.param(9, 3, id="odd-square"),
        pytest.param(16, 8, id="power-of-two"),
        pytest.param(25, 5, id="prime-square"),
        pytest.param(27, 9, id="odd-prime-power"),
        pytest.param(36, 18, id="square-with-larger-proper-divisor"),
        pytest.param(49, 7, id="larger-prime-square"),
        pytest.param(77, 11, id="distinct-odd-prime-factors"),
        pytest.param(81, 27, id="higher-odd-prime-power"),
        pytest.param(100, 50, id="multiple-divisors"),
        pytest.param(1024, 512, id="larger-power-of-two"),
    ],
)
def test_largest_divisor_examples(n, expected):
    assert largest_divisor(n) == expected


@pytest.mark.parametrize("n", range(2, 301))
def test_largest_divisor_matches_all_proper_divisors(n):
    """Independently enumerate divisors to check divisibility and maximality."""
    proper_divisors = [candidate for candidate in range(1, n) if n % candidate == 0]

    assert largest_divisor(n) == max(proper_divisors)
