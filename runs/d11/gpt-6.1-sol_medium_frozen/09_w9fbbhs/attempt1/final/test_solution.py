"""Tests for substring matching, boundaries, and the documented rotation behavior."""

import pytest

from solution import cycpattern_check


ROTATION_BUG = pytest.mark.xfail(
    strict=True,
    reason="The inner loop checks only the original pattern, not its rotations.",
)


@pytest.mark.parametrize(
    ("word", "pattern", "expected"),
    [
        pytest.param("abcd", "abd", False, id="doc-missing-substring"),
        pytest.param("hello", "ell", True, id="doc-middle-substring"),
        pytest.param("whassup", "psus", False, id="doc-no-matching-rotation"),
        pytest.param("abab", "baa", True, marks=ROTATION_BUG, id="doc-rotation-baa"),
        pytest.param("efef", "eeff", False, id="doc-anagram-is-not-rotation"),
        pytest.param("himenss", "simen", True, marks=ROTATION_BUG, id="doc-rotation-simen"),
    ],
)
def test_documented_examples(word, pattern, expected):
    assert cycpattern_check(word, pattern) is expected


@pytest.mark.parametrize(
    ("word", "pattern", "expected"),
    [
        pytest.param("", "", True, id="both-empty"),
        pytest.param("abc", "", True, id="empty-pattern"),
        pytest.param("", "a", False, id="empty-word"),
        pytest.param("ab", "abc", False, id="pattern-longer-than-word"),
        pytest.param("abc", "abc", True, id="whole-word"),
        pytest.param("abcdef", "abc", True, id="prefix"),
        pytest.param("abcdef", "def", True, id="suffix"),
        pytest.param("abcdef", "cd", True, id="interior"),
        pytest.param("abc", "a", True, id="single-character-start"),
        pytest.param("abc", "c", True, id="single-character-end"),
        pytest.param("abc", "z", False, id="single-character-absent"),
        pytest.param("aaaaa", "aaa", True, id="repeated-characters"),
        pytest.param("aaaaa", "aab", False, id="repeated-characters-mismatch"),
        pytest.param("Abc", "abc", False, id="case-sensitive"),
        pytest.param("a b!c", " b!", True, id="spaces-and-punctuation"),
        pytest.param("café猫", "é猫", True, id="unicode"),
        pytest.param("acb", "abc", False, id="permutation-not-rotation"),
        pytest.param("ab", "ba", True, marks=ROTATION_BUG, id="whole-word-rotation"),
        pytest.param("xxcabyy", "abc", True, marks=ROTATION_BUG, id="interior-rotation"),
        pytest.param("abc", "cab", True, marks=ROTATION_BUG, id="last-rotation"),
    ],
)
def test_substrings_and_boundaries(word, pattern, expected):
    assert cycpattern_check(word, pattern) is expected


@pytest.mark.parametrize("pattern", ["abc", "aab", "aaaa", "é猫!"])
def test_original_pattern_embedded_at_every_position(pattern):
    for prefix_length in range(5):
        for suffix_length in range(5):
            word = "#" * prefix_length + pattern + "#" * suffix_length
            assert cycpattern_check(word, pattern) is True
