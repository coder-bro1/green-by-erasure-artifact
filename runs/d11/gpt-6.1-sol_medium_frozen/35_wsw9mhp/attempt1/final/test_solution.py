"""Characterize reverse_delete without changing its implementation.

The Boolean currently indicates a non-palindrome, contrary to the docstring.
These tests explicitly preserve that existing behavior.
"""

import pytest

from solution import reverse_delete


@pytest.mark.parametrize(
    "source, characters, expected",
    [
        pytest.param("abcde", "ae", ("bcd", True), id="first-docstring-example"),
        pytest.param("abcdef", "b", ("acdef", True), id="second-docstring-example"),
        pytest.param("abcdedcba", "ab", ("cdedc", False), id="third-docstring-example"),
        pytest.param("", "", ("", False), id="both-empty"),
        pytest.param("", "abc", ("", False), id="empty-source"),
        pytest.param("abc", "", ("abc", True), id="empty-removal-non-palindrome"),
        pytest.param("abba", "", ("abba", False), id="empty-removal-palindrome"),
        pytest.param("a", "z", ("a", False), id="single-character-kept"),
        pytest.param("a", "a", ("", False), id="single-character-removed"),
        pytest.param("abccba", "abc", ("", False), id="all-characters-removed"),
        pytest.param("banana", "an", ("b", False), id="all-occurrences-removed"),
        pytest.param("banana", "aaaann", ("b", False), id="duplicate-removal-characters"),
        pytest.param("cabac", "xyz", ("cabac", False), id="no-matches-palindrome"),
        pytest.param("cab", "xyz", ("cab", True), id="no-matches-non-palindrome"),
        pytest.param("abXba", "X", ("abba", False), id="creates-even-palindrome"),
        pytest.param("racecar", "e", ("raccar", False), id="preserves-palindrome"),
        pytest.param("abca", "b", ("aca", False), id="creates-odd-palindrome"),
        pytest.param("AaA", "a", ("AA", False), id="case-sensitive-removal"),
        pytest.param("Aa", "", ("Aa", True), id="case-sensitive-comparison"),
        pytest.param("a b\ta\nb", " \t\n", ("abab", True), id="whitespace-removal"),
        pytest.param("a,!a", ",!", ("aa", False), id="punctuation-removal"),
        pytest.param("a.b*a", ".*", ("aba", False), id="literal-regex-metacharacters"),
        pytest.param("é🙂x🙂é", "x", ("é🙂🙂é", False), id="unicode-palindrome"),
        pytest.param("🙂é🙂x", "🙂", ("éx", True), id="unicode-removal"),
        pytest.param("cabbage", "ag", ("cbbe", True), id="retains-order-and-duplicates"),
    ],
)
def test_reverse_delete_current_behavior(source, characters, expected):
    result = reverse_delete(source, characters)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], str)
    assert type(result[1]) is bool
    assert result == expected


def test_long_input_removes_every_occurrence():
    source = "ab" * 10_000 + "x" + "ba" * 10_000

    assert reverse_delete(source, "b") == ("a" * 10_000 + "x" + "a" * 10_000, False)
