"""Tests for longest's documented contract and its known implementation defect."""

import pytest

from solution import longest


def test_empty_list_returns_none():
    assert longest([]) is None


@pytest.mark.parametrize(
    "strings, expected",
    [
        pytest.param(["hello"], "hello", id="single-string"),
        pytest.param([""], "", id="single-empty-string"),
        pytest.param(["", "", ""], "", id="all-empty-strings"),
        pytest.param(["a", "bb", "ccc"], "ccc", id="longest-last"),
        pytest.param(["longest", "bb", "a"], "longest", id="longest-first"),
        pytest.param(["a", "longest", "bb"], "longest", id="longest-middle"),
        pytest.param(["a", "b", "c"], "a", id="all-lengths-tied"),
        pytest.param(["a", "first", "later"], "first", id="longest-tie"),
        pytest.param(["", "abc", ""], "abc", id="mixed-empty-strings"),
        pytest.param([" ", "   ", "  "], "   ", id="whitespace-counts"),
        pytest.param(["猫猫", "abc", "🐍"], "abc", id="unicode-character-length"),
    ],
)
@pytest.mark.xfail(
    strict=True,
    reason="Known bug: len(s) > maxlen is never true, so nonempty input returns None.",
)
def test_nonempty_list_returns_first_longest_string(strings, expected):
    assert longest(strings) == expected


@pytest.mark.parametrize("strings", [[], ["a"], ["ccc", "a", "bb", "ccc"]])
def test_input_list_is_not_modified(strings):
    original = strings.copy()
    longest(strings)
    assert strings == original
