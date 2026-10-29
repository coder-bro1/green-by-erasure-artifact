"""Tests for solution.lcs_length (longest common substring length).

NOTE: solution.py contains a known bug. The DP recurrence uses
``dp[i - 1, j]`` instead of ``dp[i - 1, j - 1]``, so it counts runs of a
repeated character in ``s`` rather than diagonal matches. Tests asserting
the documented (correct) behaviour that the bug breaks are marked
``xfail(strict=True)``: they document the defect, and will start failing
(XPASS -> error) once the bug is fixed, signalling the marker should go.
"""
import itertools
import random

import pytest

from solution import lcs_length

BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py bug: uses dp[i-1, j] instead of dp[i-1, j-1]",
)


def reference_lcs_length(s, t):
    """Brute-force reference implementation."""
    best = 0
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            if s[i:j] in t:
                best = max(best, j - i)
    return best


# --- Cases where the current implementation is correct -------------------

@pytest.mark.parametrize(
    "s, t",
    [("", ""), ("", "abc"), ("abc", ""), ("abc", "xyz"), ("a", "b")],
)
def test_no_common_substring_returns_zero(s, t):
    assert lcs_length(s, t) == 0


@pytest.mark.parametrize(
    "s, t",
    [("a", "a"), ("a", "banana"), ("xyz", "z"), ("ab", "ba"), ("abc", "cxx")],
)
def test_single_character_overlap_returns_one(s, t):
    assert lcs_length(s, t) == 1


def test_returns_int():
    assert isinstance(lcs_length("abc", "c"), int)
    assert isinstance(lcs_length("", ""), int)


def test_case_sensitive():
    assert lcs_length("ABC", "abc") == 0


def test_works_with_lists():
    assert lcs_length([1, 2, 3], [4, 5, 3]) == 1


# --- Documented behaviour broken by the bug ------------------------------

@BUG
def test_docstring_example_witch_sandwich():
    assert lcs_length("witch", "sandwich") == 2


@BUG
def test_docstring_example_meow_homeowner():
    assert lcs_length("meow", "homeowner") == 4


@BUG
def test_identical_strings():
    assert lcs_length("abcdef", "abcdef") == 6


@BUG
def test_substring_contained():
    assert lcs_length("ell", "hello") == 3


@BUG
def test_repeated_char_in_s_not_overcounted():
    # Buggy version returns 3 here.
    assert lcs_length("aaa", "a") == 1


@BUG
def test_symmetric():
    assert lcs_length("witch", "sandwich") == lcs_length("sandwich", "witch") == 2


@BUG
def test_matches_reference_exhaustive_small_alphabet():
    for n, m in [(3, 3), (4, 2)]:
        for s in map("".join, itertools.product("ab", repeat=n)):
            for t in map("".join, itertools.product("ab", repeat=m)):
                assert lcs_length(s, t) == reference_lcs_length(s, t), (s, t)


@BUG
def test_matches_reference_random():
    rng = random.Random(0)
    for _ in range(200):
        s = "".join(rng.choice("abc") for _ in range(rng.randint(0, 10)))
        t = "".join(rng.choice("abc") for _ in range(rng.randint(0, 10)))
        assert lcs_length(s, t) == reference_lcs_length(s, t), (s, t)


def test_reference_implementation_sanity():
    assert reference_lcs_length("witch", "sandwich") == 2
    assert reference_lcs_length("meow", "homeowner") == 4
    assert reference_lcs_length("", "abc") == 0
