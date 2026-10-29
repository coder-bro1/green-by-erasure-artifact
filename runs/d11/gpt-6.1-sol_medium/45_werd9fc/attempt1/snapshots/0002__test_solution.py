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
        ("cat", False),
        ("Aa", False),
        ("a a", True),
        ("aba ", False),
        ("été", True),
        ("🙂a🙂", True),
        ("\na\n", True),
    ],
)
def test_is_palindrome(string, expected):
    assert is_palindrome(string) is expected


@pytest.mark.parametrize(
    ("string", "expected"),
    [
        ("", ""),
        ("a", "a"),
        ("aaaa", "aaaa"),
        ("aba", "aba"),
        ("abba", "abba"),
        ("racecar", "racecar"),
        ("cat", "catac"),
        ("cata", "catac"),
        ("ab", "aba"),
        ("abcd", "abcdcba"),
        ("abb", "abba"),
        ("aab", "aabaa"),
        ("abac", "abacaba"),
        ("abbaa", "abbaabba"),
        ("Aa", "AaA"),
        ("a ", "a a"),
        ("a!", "a!a"),
        ("été", "été"),
        ("éa", "éaé"),
        ("🙂a", "🙂a🙂"),
        ("a\n", "a\na"),
    ],
)
def test_make_palindrome(string, expected):
    assert make_palindrome(string) == expected


def test_make_palindrome_is_shortest_for_all_small_binary_strings():
    # Independently enumerate appended strings in increasing length instead
    # of reproducing the implementation's palindromic-suffix algorithm.
    for length in range(7):
        for characters in product("ab", repeat=length):
            string = "".join(characters)
            expected = next(
                candidate
                for extension_length in range(max(1, length))
                for extension in product("ab", repeat=extension_length)
                if (candidate := string + "".join(extension)) == candidate[::-1]
            )
            result = make_palindrome(string)
            assert result == expected, string
            assert result.startswith(string)
            assert result == result[::-1]
            assert make_palindrome(result) == result
