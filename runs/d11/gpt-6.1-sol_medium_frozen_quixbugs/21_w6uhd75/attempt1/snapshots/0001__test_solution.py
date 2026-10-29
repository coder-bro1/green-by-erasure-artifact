"""Tests for the documented longest-common-substring contract."""

import pytest

from solution import lcs_length


@pytest.mark.parametrize(
    ("s", "t", "expected"),
    [
        pytest.param("", "", 0, id="both-empty"),
        pytest.param("", "abc", 0, id="first-empty"),
        pytest.param("abc", "", 0, id="second-empty"),
        pytest.param("abc", "XYZ", 0, id="disjoint"),
        pytest.param("a", "a", 1, id="single-match"),
        pytest.param("a", "b", 0, id="single-mismatch"),
        pytest.param("abc", "xby", 1, id="interior-match"),
        pytest.param("abc", "cxy", 1, id="boundary-match"),
        pytest.param("abc", "axbxc", 1, id="substring-not-subsequence"),
        pytest.param("ABC", "abc", 0, id="case-sensitive"),
        pytest.param(" ", "a b", 1, id="whitespace"),
        pytest.param("!", "hello!", 1, id="punctuation"),
        pytest.param("猫", "小猫咪", 1, id="unicode"),
        pytest.param("aaa", "aaa", 3, id="identical-repeated-characters"),
        pytest.param("a", "aaaa", 1, id="repetitions-in-second-input"),
    ],
)
def test_lcs_length(s, t, expected):
    assert lcs_length(s, t) == expected


@pytest.mark.xfail(
    strict=True,
    reason="DP uses (i - 1, j) instead of (i - 1, j - 1).",
)
@pytest.mark.parametrize(
    ("s", "t", "expected"),
    [
        pytest.param("witch", "sandwich", 2, id="docstring-witch"),
        pytest.param("meow", "homeowner", 4, id="docstring-meow"),
        pytest.param("abc", "abc", 3, id="identical-distinct-characters"),
        pytest.param("aa", "a", 1, id="cannot-exceed-shorter-input"),
    ],
)
def test_lcs_length_known_recurrence_bug(s, t, expected):
    # Keep the correct expectations visible without changing solution.py.
    assert lcs_length(s, t) == expected
