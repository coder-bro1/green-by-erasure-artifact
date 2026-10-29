import pytest

from solution import is_palindrome, make_palindrome


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", True),
        ("a", True),
        ("abba", True),
        ("racecar", True),
        ("ab", False),
        ("abca", False),
        ("Racecar", False),
        ("a b a", True),
    ],
)
def test_is_palindrome(value, expected):
    assert is_palindrome(value) is expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", ""),
        ("a", "a"),
        ("aaa", "aaa"),
        ("aba", "aba"),
        ("ab", "aba"),
        ("abc", "abcba"),
        ("cat", "catac"),
        ("cata", "catac"),
        ("aab", "aabaa"),
        ("abac", "abacaba"),
        ("race", "racecar"),
    ],
)
def test_make_palindrome(value, expected):
    result = make_palindrome(value)

    assert result == expected
    assert result.startswith(value)
    assert is_palindrome(result)


def test_make_palindrome_appends_only_when_needed():
    value = "abac"

    result = make_palindrome(value)

    assert result[len(value) :] == "aba"

