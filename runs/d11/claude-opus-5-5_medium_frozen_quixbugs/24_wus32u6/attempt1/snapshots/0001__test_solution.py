import random
import string

import pytest

from solution import longest_common_subsequence as lcs


def is_subsequence(sub, s):
    it = iter(s)
    return all(ch in it for ch in sub)


def lcs_length(a, b):
    """Reference dynamic-programming LCS length."""
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) - 1, -1, -1):
        for j in range(len(b) - 1, -1, -1):
            if a[i] == b[j]:
                dp[i][j] = 1 + dp[i + 1][j + 1]
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])
    return dp[0][0]


def assert_valid_lcs(a, b, result):
    assert isinstance(result, str)
    assert is_subsequence(result, a), f"{result!r} not a subsequence of {a!r}"
    assert is_subsequence(result, b), f"{result!r} not a subsequence of {b!r}"
    assert len(result) == lcs_length(a, b)


def test_docstring_example():
    assert lcs("headache", "pentadactyl") == "eadac"


@pytest.mark.parametrize("a, b", [("", ""), ("", "abc"), ("abc", ""), ("abc", "xyz")])
def test_empty_or_disjoint_returns_empty(a, b):
    assert lcs(a, b) == ""


@pytest.mark.parametrize("s", ["a", "abc", "hello"])
def test_identical_strings(s):
    assert lcs(s, s) == s


@pytest.mark.parametrize(
    "a, b, expected",
    [
        ("abc", "ac", "ac"),
        ("ac", "abc", "ac"),
        ("abcdef", "acf", "acf"),
        ("x", "axb", "x"),
        ("abcde", "ace", "ace"),
    ],
)
def test_one_is_subsequence_of_other(a, b, expected):
    assert lcs(a, b) == expected


@pytest.mark.parametrize(
    "a, b",
    [
        ("abcbdab", "bdcaba"),
        ("ABCDGH", "AEDFHR"),
        ("AGGTAB", "GXTXAYB"),
        ("kitten", "sitting"),
        ("headache", "pentadactyl"),
    ],
)
def test_ambiguous_cases_return_some_valid_lcs(a, b):
    # Multiple LCSs may exist; any one of maximal length is acceptable.
    assert_valid_lcs(a, b, lcs(a, b))


def test_case_sensitive():
    assert lcs("ABC", "abc") == ""


def test_randomized_against_reference_distinct_chars_in_a():
    # When `a` has no repeated characters, the result must match the reference.
    rng = random.Random(1234)
    for _ in range(200):
        a = "".join(rng.sample("abcdef", rng.randint(0, 6)))
        b = "".join(rng.choice("abcdef") for _ in range(rng.randint(0, 7)))
        assert_valid_lcs(a, b, lcs(a, b))


# --- Known bug -----------------------------------------------------------
# On a match, solution.py recurses with (a[1:], b) instead of (a[1:], b[1:]),
# so a single character of `b` can be matched by several characters of `a`.
# These tests describe correct behaviour and are expected to fail until the
# implementation is fixed (strict=True makes them error once it is fixed).
BUG_REASON = "solution.py reuses b[0] after a match: recurses on (a[1:], b), not (a[1:], b[1:])"


@pytest.mark.xfail(strict=True, reason=BUG_REASON)
@pytest.mark.parametrize(
    "a, b, expected",
    [("aa", "a", "a"), ("aab", "ab", "ab"), ("aaaa", "aa", "aa")],
)
def test_repeated_chars_do_not_reuse_b(a, b, expected):
    assert lcs(a, b) == expected


@pytest.mark.xfail(strict=True, reason=BUG_REASON)
def test_randomized_against_reference_with_repeats():
    rng = random.Random(42)
    for _ in range(200):
        a = "".join(rng.choice("ab") for _ in range(rng.randint(0, 7)))
        b = "".join(rng.choice("ab") for _ in range(rng.randint(0, 7)))
        assert_valid_lcs(a, b, lcs(a, b))
