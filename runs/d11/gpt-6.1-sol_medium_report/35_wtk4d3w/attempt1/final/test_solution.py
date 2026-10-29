"""Tests for the documented behavior of solution.longest."""

import pytest

from solution import longest


@pytest.mark.parametrize(
    ("strings", "expected"),
    [
        pytest.param([], None, id="empty-list"),
        pytest.param([""], "", id="single-empty-string"),
        pytest.param(["only"], "only", id="single-string"),
        pytest.param(["", "", ""], "", id="all-empty-strings"),
        pytest.param(["a", "b", "c"], "a", id="docstring-tie"),
        pytest.param(["a", "bb", "ccc"], "ccc", id="docstring-increasing"),
        pytest.param(["longest", "bb", "c"], "longest", id="longest-first"),
        pytest.param(["a", "longest", "bb"], "longest", id="longest-middle"),
        pytest.param(["", "abc", ""], "abc", id="mixed-empty-strings"),
        pytest.param(["a", "four", "tiny", "b"], "four", id="first-maximal-tie"),
        pytest.param(["zz", "aa"], "zz", id="tie-keeps-input-order"),
        pytest.param(["same", "x", "same"], "same", id="duplicate-longest"),
        pytest.param(["abc", "    ", "x"], "    ", id="whitespace-counts"),
        pytest.param(["ab", "a\nb\nc", "abcd"], "a\nb\nc", id="newlines-count"),
        pytest.param(["猫", "éé", "🙂🙂🙂"], "🙂🙂🙂", id="unicode-strings"),
    ],
)
def test_longest_matches_documented_behavior(strings, expected):
    assert longest(strings) == expected
