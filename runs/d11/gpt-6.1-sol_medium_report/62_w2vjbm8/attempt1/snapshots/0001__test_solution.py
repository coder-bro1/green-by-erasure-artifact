"""Tests for the substring and rotation contract of cycpattern_check."""

import pytest

from solution import cycpattern_check


@pytest.mark.parametrize(
    "word, pattern, expected",
    [
        ("abcd", "abd", False),
        ("hello", "ell", True),
        ("whassup", "psus", False),
        ("efef", "eeff", False),
    ],
)
def test_docstring_examples_without_rotation(word, pattern, expected):
    assert cycpattern_check(word, pattern) is expected


@pytest.mark.parametrize(
    "word, pattern",
    [
        ("hello", "hello"),
        ("hello", "hel"),
        ("hello", "llo"),
        ("hello", "l"),
        ("a", "a"),
        ("aaaaa", "aaa"),
        ("ababab", "abab"),
        ("Hello", "H"),
        ("café", "fé"),
        ("one two", "e t"),
        ("a.b!", ".b"),
    ],
)
def test_original_pattern_is_substring(word, pattern):
    assert cycpattern_check(word, pattern) is True


@pytest.mark.parametrize(
    "word, pattern",
    [
        ("", "a"),
        ("ab", "abc"),
        ("abc", "abcabc"),
        ("abc", "d"),
        ("abc", "ac"),
        ("abc", "acb"),
        ("aaaa", "aab"),
        ("abcdef", "cdeX"),
        ("Hello", "hello"),
        ("café", "fe"),
        ("aaaa", "aaaaa"),
    ],
)
def test_no_rotation_is_substring(word, pattern):
    assert cycpattern_check(word, pattern) is False


@pytest.mark.xfail(
    strict=True,
    reason="Only the original pattern is checked; matching rotations are skipped.",
)
@pytest.mark.parametrize(
    "word, pattern",
    [
        pytest.param("abab", "baa", id="docstring-abab-baa"),
        pytest.param("himenss", "simen", id="docstring-himenss-simen"),
        pytest.param("xxabcdyy", "bcda", id="rotation-at-offset-one"),
        pytest.param("xxabcdyy", "cdab", id="rotation-at-offset-two"),
        pytest.param("xxabcdyy", "dabc", id="rotation-at-offset-three"),
        pytest.param("ab", "ba", id="rotation-matches-whole-word"),
        pytest.param("baZZ", "ab", id="rotation-at-start"),
        pytest.param("ZZba", "ab", id="rotation-at-end"),
        pytest.param("aab", "aba", id="rotation-with-repeated-letters"),
        pytest.param("xxéayy", "aé", id="unicode-rotation"),
    ],
)
def test_rotated_pattern_is_substring(word, pattern):
    assert cycpattern_check(word, pattern) is True
