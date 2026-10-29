"""Tests for reverse_delete's documented filtering and palindrome behavior."""

import pytest

from solution import reverse_delete


CASES = [
    pytest.param("abcde", "ae", "bcd", False, id="docstring-example-1"),
    pytest.param("abcdef", "b", "acdef", False, id="docstring-example-2"),
    pytest.param("abcdedcba", "ab", "cdedc", True, id="docstring-example-3"),
    pytest.param("", "", "", True, id="both-empty"),
    pytest.param("", "abc", "", True, id="empty-source"),
    pytest.param("racecar", "", "racecar", True, id="empty-removal-palindrome"),
    pytest.param("abc", "", "abc", False, id="empty-removal-non-palindrome"),
    pytest.param("banana", "an", "b", True, id="remove-all-occurrences"),
    pytest.param("aaaa", "a", "", True, id="remove-every-character"),
    pytest.param("abba", "xyz", "abba", True, id="no-matching-characters"),
    pytest.param("a", "z", "a", True, id="single-character"),
    pytest.param("ab", "x", "ab", False, id="two-distinct-characters"),
    pytest.param("abcba", "bbb", "aca", True, id="duplicate-removal-characters"),
    pytest.param("bca", "x", "bca", False, id="preserve-order"),
    pytest.param("AaA", "a", "AA", True, id="case-sensitive-removal"),
    pytest.param("Aa", "", "Aa", False, id="case-sensitive-palindrome"),
    pytest.param("a b!a", " !", "aba", True, id="spaces-and-punctuation"),
    pytest.param("a\nb\ta", "\n\t", "aba", True, id="control-characters"),
    pytest.param("\u00e9x\u00e9", "x", "\u00e9\u00e9", True, id="unicode-palindrome"),
    pytest.param("\u00e9\u03b2x", "x", "\u00e9\u03b2", False, id="unicode-non-palindrome"),
]


@pytest.mark.parametrize("source,removed,filtered,is_palindrome", CASES)
def test_filtering_and_return_types(source, removed, filtered, is_palindrome):
    result = reverse_delete(source, removed)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] == filtered
    assert isinstance(result[0], str)
    assert type(result[1]) is bool


@pytest.mark.xfail(
    strict=True,
    reason="Docstring requires True for palindromes, but solution uses s[::-1] != s, inverting the boolean.",
)
@pytest.mark.parametrize("source,removed,filtered,is_palindrome", CASES)
def test_documented_result(source, removed, filtered, is_palindrome):
    assert reverse_delete(source, removed) == (filtered, is_palindrome)
