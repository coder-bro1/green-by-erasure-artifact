"""Characterize is_happy's current behavior, including its docstring mismatch."""

import pytest

from solution import is_happy


@pytest.mark.parametrize("s", ["", "a", "aa", "ab", "🙂", "🙂🙃"])
def test_strings_shorter_than_three_are_not_happy(s):
    assert is_happy(s) is False


@pytest.mark.parametrize("s", ["abc", "abcd", "adb", "abcabc", "🙂🙃😊"])
def test_distinct_consecutive_triples_are_happy(s):
    assert is_happy(s) is True


@pytest.mark.parametrize(
    "s",
    ["aaa", "aaaa", "aaabc", "baaac", "bcaaa", "abcdddxyz", "   ", "🙂🙂🙂"],
)
def test_identical_triples_anywhere_are_not_happy(s):
    assert is_happy(s) is False


@pytest.mark.parametrize("s", ["aab", "abb", "aba", "aabb", "xyy", "ababab"])
def test_repeated_pairs_are_currently_accepted(s):
    # The docstring requires all three characters to be distinct, but the
    # implementation only rejects triples where all three are identical.
    assert is_happy(s) is True


@pytest.mark.parametrize("s", ["aAa", "AAa", "111", "\n\n\n", "\t\t\t"])
def test_character_comparison_is_literal(s):
    expected = s in ("aAa", "AAa")
    assert is_happy(s) is expected
