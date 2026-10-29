"""Tests for substring matching and the documented rotation contract."""

import pytest

from solution import contains_rotation


@pytest.mark.parametrize(
    ("text", "word", "expected"),
    [
        pytest.param("abc", "abc", True, id="whole-text"),
        pytest.param("abcdef", "abc", True, id="prefix"),
        pytest.param("abcdef", "cde", True, id="middle"),
        pytest.param("abcdef", "def", True, id="suffix"),
        pytest.param("xxabc", "abc", True, id="last-possible-position"),
        pytest.param("aaaab", "aaab", True, id="overlapping-prefixes"),
        pytest.param("aaaa", "aa", True, id="repeated-characters"),
        pytest.param("abc", "b", True, id="single-character-present"),
        pytest.param("abc", "z", False, id="single-character-absent"),
        pytest.param("abc", "xyz", False, id="unrelated-word"),
        pytest.param("abc", "abcd", False, id="word-longer-than-text"),
        pytest.param("", "a", False, id="empty-text"),
        pytest.param("", "", True, id="both-empty"),
        pytest.param("abc", "", True, id="empty-word"),
        pytest.param("abcde", "eab", False, id="documented-negative-example"),
        pytest.param("ab", "aba", False, id="partial-match"),
        pytest.param("abXcd", "abcd", False, id="noncontiguous-match"),
        pytest.param("ABC", "abc", False, id="case-sensitive"),
        pytest.param("a b\nc", " b\n", True, id="whitespace"),
        pytest.param("x.*?y", ".*?", True, id="literal-punctuation"),
        pytest.param("café", "fé", True, id="unicode"),
        pytest.param("aU0001f600b", "U0001f600", True, id="emoji"),
    ],
)
def test_contains_rotation(text, word, expected):
    assert contains_rotation(text, word) is expected


@pytest.mark.xfail(
    strict=True,
    reason="The inner loop checks only rotation zero, missing rotated matches.",
)
@pytest.mark.parametrize(
    ("text", "word"),
    [
        pytest.param("network", "orkw", id="documented-network-example"),
        pytest.param("abc", "cb", id="documented-two-character-example"),
        pytest.param("xxcabyy", "abc", id="rotation-inside-text"),
        pytest.param("bca", "abc", id="rotation-at-word-length"),
    ],
)
def test_nontrivial_rotation_matches(text, word):
    assert contains_rotation(text, word) is True
