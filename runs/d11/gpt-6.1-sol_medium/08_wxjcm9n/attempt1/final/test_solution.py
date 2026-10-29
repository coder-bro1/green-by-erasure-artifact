"""Tests for character removal and palindrome detection in reverse_delete."""

import pytest

from solution import reverse_delete


@pytest.mark.parametrize(
    ("s", "c", "expected"),
    [
        pytest.param("abcde", "ae", ("bcd", False), id="example-non-palindrome"),
        pytest.param("abcdef", "b", ("acdef", False), id="example-single-removal"),
        pytest.param("abcdedcba", "ab", ("cdedc", True), id="example-palindrome"),
        pytest.param("", "", ("", True), id="both-empty"),
        pytest.param("", "abc", ("", True), id="empty-input"),
        pytest.param("racecar", "", ("racecar", True), id="no-removals-palindrome"),
        pytest.param("abc", "", ("abc", False), id="no-removals-non-palindrome"),
        pytest.param("abc", "cba", ("", True), id="all-characters-removed"),
        pytest.param("a", "x", ("a", True), id="single-character-retained"),
        pytest.param("a", "a", ("", True), id="single-character-removed"),
        pytest.param("banana", "an", ("b", True), id="all-occurrences-removed"),
        pytest.param("abacaba", "bbxx", ("aacaa", True), id="duplicate-and-absent-targets"),
        pytest.param("abca", "xyz", ("abca", False), id="no-matching-targets"),
        pytest.param("aabb", "", ("aabb", False), id="order-preserved"),
        pytest.param("abba", "", ("abba", True), id="even-length-palindrome"),
        pytest.param("AaA", "a", ("AA", True), id="case-sensitive-removal"),
        pytest.param("Aa", "", ("Aa", False), id="case-sensitive-palindrome"),
        pytest.param("a b\ta\n", " \t\n", ("aba", True), id="whitespace-removal"),
        pytest.param("a,b!a", ",!", ("aba", True), id="punctuation-removal"),
        pytest.param("é🙂x🙂é", "x", ("é🙂🙂é", True), id="unicode-characters"),
    ],
)
def test_reverse_delete(s, c, expected):
    result = reverse_delete(s, c)

    assert result == expected
    assert isinstance(result, tuple)
    assert type(result[1]) is bool
