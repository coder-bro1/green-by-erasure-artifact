"""Tests for the current behavior of solution.gcd, including its recursion bug."""

import pytest

from solution import gcd


@pytest.mark.parametrize("a", [0, 1, 2, 7, 35, 100, 2**128, 10**100])
def test_zero_second_argument_returns_first_argument(a):
    """The base case works for zero, small values, and arbitrary-size integers."""
    assert gcd(a, 0) == a


@pytest.mark.parametrize(
    "a, b",
    [
        (0, 1),  # Zero first argument.
        (0, 35),
        (1, 1),  # Equal arguments.
        (21, 21),
        (35, 21),  # The example in the docstring.
        (21, 35),  # First argument smaller than the second.
        (12, 4),  # Exact divisibility.
        (17, 13),  # Coprime arguments.
        (2**128, 2**64),  # Arbitrary-size integers.
    ],
)
def test_positive_second_argument_currently_raises_recursion_error(a, b):
    """Document the bug: recursion never changes the positive second argument."""
    with pytest.raises(RecursionError):
        gcd(a, b)
