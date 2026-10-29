"""Tests for counting even and odd palindromes in the inclusive range 1..n."""

import pytest

from solution import even_odd_palindrome


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (1, (0, 1)),
        (2, (1, 1)),
        (3, (1, 2)),
        (9, (4, 5)),
        (10, (4, 5)),
        (11, (4, 6)),
        (12, (4, 6)),
        (21, (4, 6)),
        (22, (5, 6)),
        (99, (8, 10)),
        (100, (8, 10)),
        (101, (8, 11)),
        (202, (9, 20)),
        (999, (48, 60)),
        (1000, (48, 60)),
    ],
)
def test_examples_and_boundaries(n, expected):
    """Cover parity, inclusive endpoints, and decimal-length transitions."""
    result = even_odd_palindrome(n)

    assert isinstance(result, tuple)
    assert result == expected
    assert all(type(count) is int for count in result)


def test_every_supported_input_against_arithmetic_reference():
    """Check the full documented domain using numeric digit reversal."""
    expected = [0, 0]

    for n in range(1, 1001):
        remaining = n
        reversed_number = 0
        while remaining:
            reversed_number = reversed_number * 10 + remaining % 10
            remaining //= 10

        if reversed_number == n:
            expected[n % 2] += 1

        assert even_odd_palindrome(n) == tuple(expected), f"Failed for n={n}"
