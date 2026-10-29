import pytest

from solution import is_palindrome, make_palindrome


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", True),
        ("a", True),
        ("racecar", True),
        ("abba", True),
        ("python", False),
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
        ("racecar", "racecar"),
        ("abba", "abba"),
        ("cat", "catac"),
        ("cata", "catac"),
        ("abac", "abacaba"),
        ("abcd", "abcdcba"),
    ],
)
def test_make_palindrome(value, expected):
    result = make_palindrome(value)

    assert result == expected
    assert result.startswith(value)
    assert is_palindrome(result)
