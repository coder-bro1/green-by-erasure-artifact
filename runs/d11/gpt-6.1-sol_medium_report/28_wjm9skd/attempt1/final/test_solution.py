"""Tests for the contracts documented in solution.py."""

from itertools import product

import pytest

from solution import is_palindrome, make_palindrome


@pytest.mark.parametrize(
    ("string", "expected"),
    [
        ("", True),
        ("a", True),
        ("aa", True),
        ("aba", True),
        ("abba", True),
        ("racecar", True),
        ("ab", False),
        ("abca", False),
        ("Aa", False),
        ("a a", True),
        (" a", False),
        ("a!a", True),
        ("a!", False),
        ("\naba\n", True),
        ("\taba", False),
        ("é中é", True),
        ("é中", False),
        ("😀a😀", True),
        ("😀a", False),
    ],
)
def test_is_palindrome(string, expected):
    assert is_palindrome(string) is expected


@pytest.mark.parametrize(
    ("string", "expected"),
    [
        ("", ""),
        ("a", "a"),
        ("aa", "aa"),
        ("aba", "aba"),
        ("abba", "abba"),
        ("racecar", "racecar"),
        ("cat", "catac"),
        ("cata", "catac"),
        ("ab", "aba"),
        ("abc", "abcba"),
        ("abcd", "abcdcba"),
        ("abb", "abba"),
        ("aab", "aabaa"),
        ("abab", "ababa"),
        ("abbaa", "abbaabba"),
        ("Aa", "AaA"),
        (" a", " a "),
        ("a!", "a!a"),
        ("a\n", "a\na"),
        ("é中", "é中é"),
        ("😀a", "😀a😀"),
    ],
)
def test_make_palindrome(string, expected):
    assert make_palindrome(string) == expected


def _shortest_palindrome_by_enumeration(string):
    """Try every binary appendage in length order, without suffix detection."""
    for length in range(len(string) + 1):
        for characters in product("ab", repeat=length):
            candidate = string + "".join(characters)
            if all(
                candidate[index] == candidate[-index - 1]
                for index in range(len(candidate) // 2)
            ):
                return candidate
    raise AssertionError("Appending the reversed input must yield a palindrome")


@pytest.mark.parametrize(
    "string",
    [
        "".join(characters)
        for length in range(7)
        for characters in product("ab", repeat=length)
    ],
)
def test_make_palindrome_is_shortest_for_all_short_binary_strings(string):
    result = make_palindrome(string)

    assert isinstance(result, str)
    assert result.startswith(string)
    assert result == result[::-1]
    assert result == _shortest_palindrome_by_enumeration(string)
