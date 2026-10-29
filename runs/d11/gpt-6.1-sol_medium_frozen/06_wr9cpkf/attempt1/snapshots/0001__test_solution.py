"""Tests for the implemented, exclusive-upper-bound palindrome counter."""

import pytest

from solution import even_odd_palindrome


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (1, (0, 0)),
        (2, (0, 1)),
        (3, (1, 1)),
        (9, (4, 4)),
        (10, (4, 5)),
        (11, (4, 5)),
        (12, (4, 6)),
        (22, (4, 6)),
        (23, (5, 6)),
        (99, (8, 9)),
        (100, (8, 10)),
        (101, (8, 10)),
        (102, (8, 11)),
        (1000, (48, 60)),
    ],
)
def test_known_counts(n, expected):
    result = even_odd_palindrome(n)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(type(count) is int for count in result)
    assert result == expected


def test_all_supported_inputs_against_arithmetic_oracle():
    """Reverse digits arithmetically to avoid copying the string-based logic."""
    expected = [0, 0]
    for n in range(1, 1001):
        # Check before adding n: the implementation counts values below n.
        assert even_odd_palindrome(n) == tuple(expected), f"n={n}"

        remaining = n
        reversed_number = 0
        while remaining:
            remaining, digit = divmod(remaining, 10)
            reversed_number = reversed_number * 10 + digit
        if reversed_number == n:
            expected[n % 2] += 1
