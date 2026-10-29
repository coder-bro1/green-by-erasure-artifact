"""Tests for the substring and rotation contract of cycpattern_check."""

from itertools import product

import pytest

from solution import cycpattern_check


@pytest.mark.parametrize(
    "word, pattern, expected",
    [
        ("abcd", "abd", False),
        ("hello", "ell", True),
        ("whassup", "psus", False),
        ("abab", "baa", True),
        ("efef", "eeff", False),
        ("himenss", "simen", True),
    ],
)
def test_docstring_examples(word, pattern, expected):
    assert cycpattern_check(word, pattern) is expected


@pytest.mark.parametrize("offset", range(5))
@pytest.mark.parametrize("prefix, suffix", [("", ""), ("xx", ""), ("", "yy"), ("xx", "yy")])
def test_every_rotation_at_substring_boundaries(offset, prefix, suffix):
    pattern = "abcde"
    rotation = pattern[offset:] + pattern[:offset]
    assert cycpattern_check(prefix + rotation + suffix, pattern) is True


@pytest.mark.parametrize(
    "word, pattern, expected",
    [
        ("", "", True),
        ("abc", "", True),
        ("", "a", False),
        ("ab", "abc", False),
        ("a", "a", True),
        ("a", "b", False),
        ("aaaa", "aaa", True),
        ("aaaa", "aab", False),
        ("ababab", "baba", True),
        ("acb", "abc", False),  # An arbitrary permutation is not a rotation.
        ("cba", "abc", False),  # Reversal is not necessarily a rotation.
        ("abXXc", "abc", False),  # Characters must be contiguous.
        ("cab", "abcd", False),  # The first word does not wrap around.
        ("aBC", "abc", False),
        ("xx\u00e9\u03bb\u732byy", "\u732b\u00e9\u03bb", True),
        ("xx! a?yy", "a?! ", True),
        ("xxb\nayy", "ab\n", True),
    ],
)
def test_edge_cases(word, pattern, expected):
    assert cycpattern_check(word, pattern) is expected


def test_exhaustive_short_binary_words_against_rotation_oracle():
    """Check repeats, overlaps, absent matches, and all relative lengths."""
    words = [
        "".join(chars)
        for length in range(6)
        for chars in product("ab", repeat=length)
    ]
    patterns = [word for word in words if len(word) <= 4]
    for word in words:
        for pattern in patterns:
            rotations = {
                pattern[offset:] + pattern[:offset]
                for offset in range(len(pattern))
            } or {""}
            expected = any(rotation in word for rotation in rotations)
            assert cycpattern_check(word, pattern) is expected, (word, pattern)
