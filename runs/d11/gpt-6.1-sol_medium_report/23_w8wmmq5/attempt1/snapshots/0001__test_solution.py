"""Tests for the filtering and ordering documented by sorted_list_sum."""

import pytest

from solution import sorted_list_sum


@pytest.mark.parametrize(
    ("words", "expected"),
    [
        pytest.param([], [], id="empty-input"),
        pytest.param(["aa", "a", "aaa"], ["aa"], id="first-docstring-example"),
        pytest.param(
            ["ab", "a", "aaa", "cd"], ["ab", "cd"],
            id="second-docstring-example",
        ),
        pytest.param(["a", "bbb", "ccccc"], [], id="all-odd-lengths"),
        pytest.param(["abcd"], ["abcd"], id="single-even-word"),
        pytest.param(["x"], [], id="single-odd-word"),
        pytest.param([""], [""], id="zero-length-is-even"),
        pytest.param(["", "a", ""], ["", ""], id="duplicate-empty-strings"),
        pytest.param(["zz", "ab", "aa"], ["aa", "ab", "zz"], id="alphabetical-ties"),
        pytest.param(["aa", "ab", "zz"], ["aa", "ab", "zz"], id="already-sorted"),
        pytest.param(
            ["bb", "aa", "bb", "a", "a", "aa"],
            ["aa", "aa", "bb", "bb"], id="retain-even-duplicates",
        ),
        pytest.param(["ab", "AB", "Aa", "aB"], ["AB", "Aa", "aB", "ab"], id="case-sensitive-order"),
        pytest.param(["éé", "猫猫", "é", "猫"], ["éé", "猫猫"], id="unicode-character-length"),
        pytest.param(["  ", " ", "a ", "!"] , ["  ", "a "], id="spaces-count-as-characters"),
        pytest.param(["zzzz", "aa", "b", "ccc"], ["aa", "zzzz"], id="mixed-lengths-already-aligned"),
    ],
)
def test_filter_and_sort(words, expected):
    result = sorted_list_sum(words)

    assert isinstance(result, list)
    assert result == expected


@pytest.mark.parametrize(
    ("words", "expected"),
    [
        pytest.param(["aaaa", "zz"], ["zz", "aaaa"], id="length-before-alphabet"),
        pytest.param(
            ["bbbb", "zz", "aaaa", "yy", "c", "ddd"],
            ["yy", "zz", "aaaa", "bbbb"], id="length-then-alphabet-with-filtering",
        ),
        pytest.param(
            ["aaaaaa", "bbbb", "zz", "bbbb", "zz"],
            ["zz", "zz", "bbbb", "bbbb", "aaaaaa"], id="multiple-lengths-with-duplicates",
        ),
    ],
)
def test_length_takes_priority_over_alphabetical_order(words, expected):
    assert sorted_list_sum(words) == expected
