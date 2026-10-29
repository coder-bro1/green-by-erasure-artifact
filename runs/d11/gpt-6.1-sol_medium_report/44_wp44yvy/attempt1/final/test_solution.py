"""Tests for the deletion and palindrome contract in solution.py."""

import pytest

from solution import reverse_delete


@pytest.mark.parametrize(
    "s, c, expected",
    [
        pytest.param("abcde", "ae", ("bcd", False), id="docstring-example-1"),
        pytest.param("abcdef", "b", ("acdef", False), id="docstring-example-2"),
        pytest.param("abcdedcba", "ab", ("cdedc", True), id="docstring-example-3"),
        pytest.param("", "", ("", True), id="both-empty"),
        pytest.param("", "abc", ("", True), id="empty-source"),
        pytest.param("racecar", "", ("racecar", True), id="no-deletions-palindrome"),
        pytest.param("hello", "", ("hello", False), id="no-deletions-nonpalindrome"),
        pytest.param("level", "xyz", ("level", True), id="absent-removal-characters"),
        pytest.param("abc", "cba", ("", True), id="delete-every-character"),
        pytest.param("aaaa", "a", ("", True), id="delete-every-occurrence"),
        pytest.param("banana", "a", ("bnn", False), id="delete-repeated-occurrences"),
        pytest.param("banana", "an", ("b", True), id="delete-multiple-character-kinds"),
        pytest.param("banana", "aaannn", ("b", True), id="duplicate-removal-characters"),
        pytest.param("cabdab", "ab", ("cd", False), id="removal-is-not-substring-based"),
        pytest.param("a", "z", ("a", True), id="single-surviving-character"),
        pytest.param("abba", "x", ("abba", True), id="even-length-palindrome"),
        pytest.param("abca", "x", ("abca", False), id="matching-ends-are-insufficient"),
        pytest.param("abxba", "x", ("abba", True), id="deletion-creates-even-palindrome"),
        pytest.param("racecar", "r", ("aceca", True), id="deletion-preserves-palindrome"),
        pytest.param("AaA", "A", ("a", True), id="deletion-is-case-sensitive"),
        pytest.param("Aa", "", ("Aa", False), id="palindrome-is-case-sensitive"),
        pytest.param(" a b a ", " ", ("aba", True), id="delete-spaces"),
        pytest.param("a a", "", ("a a", True), id="preserve-spaces"),
        pytest.param("a\nb\ta", "\n\t", ("aba", True), id="delete-control-characters"),
        pytest.param("a.b,a!", ".,!", ("aba", True), id="delete-punctuation"),
        pytest.param("é🙂x🙂é", "x", ("é🙂🙂é", True), id="unicode-palindrome"),
        pytest.param("猫犬猫", "猫", ("犬", True), id="delete-unicode-characters"),
        pytest.param("é", "e", ("é", True), id="distinct-accented-character"),
        pytest.param("abc123cba", "123", ("abccba", True), id="delete-digits"),
        pytest.param("cab", "", ("cab", False), id="preserve-original-order"),
    ],
)
def test_reverse_delete(s, c, expected):
    result = reverse_delete(s, c)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], str)
    assert type(result[1]) is bool
    assert result == expected
