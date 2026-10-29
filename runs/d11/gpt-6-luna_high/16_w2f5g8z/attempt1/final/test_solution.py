"""Tests for the prime_length function."""

import pytest

from solution import prime_length


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", False),
        ("a", False),
        ("ab", True),
        ("abc", True),
        ("abcd", False),
        ("Hello", True),
        ("abcdcba", True),
        ("kittens", True),
        ("orange", False),
        ("a" * 11, True),
        ("a" * 12, False),
    ],
)
def test_prime_length(value, expected):
    assert prime_length(value) is expected


def test_prime_length_uses_string_length():
    # Contents do not matter; only the number of characters does.
    assert prime_length("!@#$%") is True
    assert prime_length("123456") is False
