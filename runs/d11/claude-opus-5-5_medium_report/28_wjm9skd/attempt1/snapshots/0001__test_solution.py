import pytest

from solution import is_palindrome, make_palindrome


@pytest.mark.parametrize("s", ["", "a", "aa", "aba", "abba", "racecar", "xywyx"])
def test_is_palindrome_true(s):
    assert is_palindrome(s) is True


@pytest.mark.parametrize("s", ["ab", "abc", "abca", "Aba", "xywyz"])
def test_is_palindrome_false(s):
    assert is_palindrome(s) is False


@pytest.mark.parametrize(
    "s, expected",
    [
        ("", ""),
        ("cat", "catac"),
        ("cata", "catac"),
        ("x", "x"),
        ("xyz", "xyzyx"),
        ("xyx", "xyx"),
        ("jerry", "jerryrrej"),
        ("ab", "aba"),
        ("aab", "aabaa"),
        ("abb", "abba"),
    ],
)
def test_make_palindrome_examples(s, expected):
    assert make_palindrome(s) == expected


def _brute_force_shortest(s):
    # Shortest palindrome starting with s: try appending k chars for k=0..len(s).
    for k in range(len(s) + 1):
        candidate = s + s[:k][::-1]
        if candidate == candidate[::-1]:
            return candidate


@pytest.mark.parametrize(
    "s", ["", "a", "ab", "abc", "abac", "aacecaaa", "banana", "abcba", "abcd", "zzzy"]
)
def test_make_palindrome_properties(s):
    result = make_palindrome(s)
    assert result.startswith(s)
    assert is_palindrome(result)
    assert result == _brute_force_shortest(s)
    assert len(result) <= 2 * len(s)
