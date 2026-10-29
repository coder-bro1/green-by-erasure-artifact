"""Tests for the longest-common-substring contract in solution.py."""

from itertools import product

import pytest

from solution import lcs_length


@pytest.mark.parametrize(
    "s, t, expected",
    [
        pytest.param("witch", "sandwich", 2, id="docstring-witch"),
        pytest.param("meow", "homeowner", 4, id="docstring-meow"),
        pytest.param("", "", 0, id="both-empty"),
        pytest.param("", "abc", 0, id="first-empty"),
        pytest.param("abc", "", 0, id="second-empty"),
        pytest.param("abc", "XYZ", 0, id="disjoint"),
        pytest.param("a", "a", 1, id="single-match"),
        pytest.param("a", "b", 0, id="single-mismatch"),
        pytest.param("banana", "banana", 6, id="identical"),
        pytest.param("needle", "a needle here", 6, id="contained"),
        pytest.param("abcXYZ", "abc123", 3, id="common-prefix"),
        pytest.param("XYZabc", "123abc", 3, id="common-suffix"),
        pytest.param("xxabczz", "yyabcww", 3, id="common-interior"),
        pytest.param("abcXYZ", "123abc", 3, id="different-offsets"),
        pytest.param("abc", "aXbYc", 1, id="subsequence-is-not-substring"),
        pytest.param("abXcd", "abYcd", 2, id="mismatch-resets-length"),
        pytest.param("aaaaa", "aaa", 3, id="repeated-character"),
        pytest.param("ababab", "babab", 5, id="overlapping-matches"),
        pytest.param("ABC", "abc", 0, id="case-sensitive"),
        pytest.param("a b\tc", "x b\ty", 3, id="whitespace"),
        pytest.param("café", "félicité", 2, id="unicode"),
        pytest.param("a🙂🚀b", "x🙂🚀y", 2, id="emoji"),
        pytest.param("a\x00b", "x\x00by", 2, id="embedded-null"),
    ],
)
def test_lcs_length_examples_and_edges(s, t, expected):
    result = lcs_length(s, t)
    assert type(result) is int
    assert result == expected
    assert lcs_length(t, s) == expected


def brute_force_lcs_length(s, t):
    """Enumerate substrings directly, independently of the DP algorithm."""
    return max(
        (end - start
         for start in range(len(s))
         for end in range(start + 1, len(s) + 1)
         if s[start:end] in t),
        default=0,
    )


SMALL_STRINGS = [
    "".join(characters)
    for length in range(5)
    for characters in product("ab", repeat=length)
]


@pytest.mark.parametrize("s", SMALL_STRINGS)
def test_lcs_length_matches_brute_force_for_small_strings(s):
    for t in SMALL_STRINGS:
        expected = brute_force_lcs_length(s, t)
        assert lcs_length(s, t) == expected, (s, t, expected)
