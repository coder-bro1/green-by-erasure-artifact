"""Tests for the public helpers in solution.py."""

import pytest

from solution import is_palindrome, make_palindrome


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", True),
        ("a", True),
        ("level", True),
        ("abba", True),
        ("ab", False),
        ("cat", False),
        ("abca", False),
    ],
)
def test_is_palindrome(value, expected):
    assert is_palindrome(value) is expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", ""),
        ("a", "a"),
        ("level", "level"),
        ("abba", "abba"),
    ],
)
def test_make_palindrome_when_input_is_already_a_palindrome(value, expected):
    assert make_palindrome(value) == expected

