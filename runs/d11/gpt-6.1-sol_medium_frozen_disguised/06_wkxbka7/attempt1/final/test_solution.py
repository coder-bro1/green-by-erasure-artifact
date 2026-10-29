"""Tests for the current behavior of solution.no_close_repeats.

The implementation rejects triples of identical characters, while the docstring
describes rejecting any repeated character within a three-character window.
The partial-repeat cases below explicitly record this difference.
"""

import pytest

from solution import no_close_repeats


@pytest.mark.parametrize("text", ["", "a", "ab", "aa", "\n\t", "😀😀"])
def test_fewer_than_three_characters_returns_false(text):
    assert no_close_repeats(text) is False


@pytest.mark.parametrize("text", ["abc", "xyzx", "abcdef", "abcabc", "😀🐍🚀"])
def test_distinct_characters_in_each_window_returns_true(text):
    assert no_close_repeats(text) is True


@pytest.mark.parametrize(
    "text",
    ["aaa", "aaaa", "aaabc", "bcaaade", "bcaaa", "abccc", "   ", "\n\n\n", "😀😀😀"],
)
def test_identical_triple_anywhere_returns_false(text):
    assert no_close_repeats(text) is False


@pytest.mark.parametrize(
    "text", ["xyx", "xxy", "xyy", "aabb", "ababab", "aaAAaa", "😀🐍😀"]
)
def test_partial_repeats_are_accepted_by_current_implementation(text):
    assert no_close_repeats(text) is True


@pytest.mark.parametrize("text", ["AaA", "aAa", "aAA", "AAa"])
def test_character_comparisons_are_case_sensitive(text):
    assert no_close_repeats(text) is True
