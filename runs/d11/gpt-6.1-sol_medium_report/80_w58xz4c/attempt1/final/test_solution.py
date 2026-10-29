"""Tests for the filtering and ordering promised by sorted_list_sum."""

import pytest

from solution import sorted_list_sum


@pytest.mark.parametrize(
    ("words", "expected"),
    [
        pytest.param([], [], id="empty-input"),
        pytest.param(["aa", "a", "aaa"], ["aa"], id="first-docstring-example"),
        pytest.param(
            ["ab", "a", "aaa", "cd"],
            ["ab", "cd"],
            id="second-docstring-example",
        ),
        pytest.param(["a", "cat", "seven"], [], id="all-odd-lengths"),
        pytest.param(["word"], ["word"], id="single-even-word"),
        pytest.param(["x"], [], id="single-odd-word"),
        pytest.param(
            ["zz", "aa", "cc", "bb"],
            ["aa", "bb", "cc", "zz"],
            id="alphabetical-ties",
        ),
        pytest.param(
            ["aaaaaa", "zz", "bbbb"],
            ["zz", "bbbb", "aaaaaa"],
            id="length-precedes-alphabetical-order",
        ),
        pytest.param(
            ["dddd", "zz", "bbbb", "aa", "ccc", "ffffff", "e"],
            ["aa", "zz", "bbbb", "dddd", "ffffff"],
            id="mixed-lengths-and-alphabetical-ties",
        ),
        pytest.param(
            ["bb", "a", "aa", "bb", "a", "aa"],
            ["aa", "aa", "bb", "bb"],
            id="retain-even-duplicates-and-remove-odd-duplicates",
        ),
        pytest.param(["", "a", "bb", ""], ["", "", "bb"], id="zero-length-strings"),
        pytest.param(
            ["éé", "猫", "猫狗", "é"],
            ["éé", "猫狗"],
            id="unicode-character-lengths",
        ),
        pytest.param(
            ["aa", "bb", "cccc"],
            ["aa", "bb", "cccc"],
            id="already-sorted",
        ),
        pytest.param(
            ["dddd", "cccc", "bb", "aa"],
            ["aa", "bb", "cccc", "dddd"],
            id="reverse-sorted",
        ),
    ],
)
def test_sorted_list_sum_documented_behavior(words, expected):
    result = sorted_list_sum(words)

    assert isinstance(result, list)
    assert all(isinstance(word, str) for word in result)
    assert result == expected
