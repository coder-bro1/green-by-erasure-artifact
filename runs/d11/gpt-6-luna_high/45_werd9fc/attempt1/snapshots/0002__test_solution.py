import pytest

from solution import is_palindrome, make_palindrome


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", True),
        ("a", True),
        ("racecar", True),
        ("abba", True),
        ("cat", False),
        ("ab", False),
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
        ("cat", "catac"),
        ("cata", "catac"),
        ("ab", "aba"),
        ("abcd", "abcdcba"),
        ("aab", "aabaa"),
    ],
)
def test_make_palindrome(value, expected):
    result = make_palindrome(value)

    assert result == expected
    assert result.startswith(value)
    assert is_palindrome(result)


def test_make_palindrome_appends_the_minimum_required_characters():
    for value in ("abc", "abac", "abbc", "abcd", "aab"):
        result = make_palindrome(value)
        # Every shorter suffix of the result would leave a non-palindrome.
        assert all(not is_palindrome(value + value[:length][::-1])
                   for length in range(len(result) - len(value)))
