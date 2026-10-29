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
        ("ab", False),
        ("abca", False),
        ("Aa", False),
        ("a a", True),
        ("a ", False),
        ("a!a", True),
        ("été", True),
        ("🙂a🙂", True),
        ("🙂🙃", False),
        ("a\na", True),
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
        ("cat", "catac"),
        ("cata", "catac"),
        ("abcd", "abcdcba"),
        ("abcc", "abccba"),
        ("ababa", "ababa"),
        ("aabb", "aabbaa"),
        ("Aa", "AaA"),
        ("a ", "a a"),
        ("ab!", "ab!ba"),
        ("été", "été"),
        ("🙂🙃", "🙂🙃🙂"),
        ("ab\n", "ab\nba"),
    ],
)
def test_make_palindrome(string, expected):
    assert make_palindrome(string) == expected


def test_make_palindrome_is_shortest_for_all_small_binary_strings():
    """Compare against an independent exhaustive search of appended strings."""
    for length in range(7):
        for letters in product("ab", repeat=length):
            string = "".join(letters)
            result = make_palindrome(string)

            assert result.startswith(string), string
            assert list(result) == list(reversed(result)), string
            assert make_palindrome(result) == result, string

            # Appending at most length - 1 characters always suffices.
            for appended_length in range(max(1, length)):
                candidates = (
                    string + "".join(suffix)
                    for suffix in product("ab", repeat=appended_length)
                )
                shortest = next(
                    (
                        candidate
                        for candidate in candidates
                        if list(candidate) == list(reversed(candidate))
                    ),
                    None,
                )
                if shortest is not None:
                    assert result == shortest, string
                    break
            else:
                pytest.fail(f"No palindrome found for {string!r}")
