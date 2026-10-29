"""Regression tests for the current implementation.

The boolean currently means 'is not a palindrome', contrary to the docstring.
These tests preserve that observable behavior without changing solution.py.
"""

import pytest

from solution import strip_and_mirror_check


@pytest.mark.parametrize(
    ("text", "banned", "expected"),
    [
        pytest.param("", "", ("", False), id="both-empty"),
        pytest.param("", "abc", ("", False), id="empty-text"),
        pytest.param("a", "", ("a", False), id="single-character"),
        pytest.param("abba", "", ("abba", False), id="even-palindrome"),
        pytest.param("abc", "", ("abc", True), id="non-palindrome"),
        pytest.param("racecar", "x", ("racecar", False), id="absent-ban"),
        pytest.param("banana", "b", ("anana", False), id="remove-prefix"),
        pytest.param("level", "v", ("leel", False), id="remove-middle"),
        pytest.param("abaca", "a", ("bc", True), id="remove-all-occurrences"),
        pytest.param("abcabc", "ca", ("bb", False), id="multiple-banned-chars"),
        pytest.param("abc", "cba", ("", False), id="remove-everything"),
        pytest.param("banana", "bbnn", ("aaa", False), id="duplicate-bans"),
        pytest.param("Aa", "a", ("A", False), id="case-sensitive-filter"),
        pytest.param("Aa", "", ("Aa", True), id="case-sensitive-mirror"),
        pytest.param("a b!a", " !", ("aba", False), id="spaces-and-punctuation"),
        pytest.param("a\nb\ta", "\n\t", ("aba", False), id="control-characters"),
        pytest.param("é🙂é", "🙂", ("éé", False), id="unicode-filter"),
        pytest.param("🙂é", "", ("🙂é", True), id="unicode-non-palindrome"),
        pytest.param("abcd", "bd", ("ac", True), id="preserve-order"),
        pytest.param("abca", "b", ("aca", False), id="mirror-after-filtering"),
        pytest.param("abxba", "a", ("bxb", False), id="remove-both-ends"),
        pytest.param("abcba", "ab", ("c", False), id="one-character-left"),
        pytest.param("abcba", "cba", ("", False), id="ban-is-character-set"),
    ],
)
def test_strip_and_mirror_check_current_behavior(text, banned, expected):
    result = strip_and_mirror_check(text, banned)

    assert result == expected
    assert isinstance(result, tuple)
    assert type(result[0]) is str
    assert type(result[1]) is bool
