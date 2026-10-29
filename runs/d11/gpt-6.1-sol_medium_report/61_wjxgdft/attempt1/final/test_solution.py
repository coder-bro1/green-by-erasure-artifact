"""Tests for the documented happy-string rule."""

from itertools import product

import pytest

from solution import is_happy


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        pytest.param("a", False, id="example-a"),
        pytest.param("aa", False, id="example-aa"),
        pytest.param("abcd", True, id="example-abcd"),
        pytest.param("aabb", False, id="example-aabb"),
        pytest.param("adb", True, id="example-adb"),
        pytest.param("xyy", False, id="example-xyy"),
    ],
)
def test_docstring_examples(s, expected):
    assert is_happy(s) is expected


@pytest.mark.parametrize("s", ["", "b", "ab", "xy"])
def test_strings_shorter_than_three_are_unhappy(s):
    assert is_happy(s) is False


@pytest.mark.parametrize(
    "s",
    [
        pytest.param("aab", id="first-two-match"),
        pytest.param("abb", id="last-two-match"),
        pytest.param("aba", id="first-and-last-match"),
        pytest.param("aaa", id="all-three-match"),
        pytest.param("abacdef", id="invalid-first-window"),
        pytest.param("abcbd", id="invalid-middle-window"),
        pytest.param("abcdeef", id="adjacent-match-near-end"),
        pytest.param("abcded", id="invalid-final-window"),
    ],
)
def test_any_invalid_three_letter_window_is_unhappy(s):
    assert is_happy(s) is False


@pytest.mark.parametrize("s", ["abc", "abcdef", "abca", "abcabcabc"])
def test_distinct_windows_are_happy_even_when_distant_letters_repeat(s):
    assert is_happy(s) is True


def test_all_short_strings_over_three_letters_match_the_documented_rule():
    # Set cardinality provides an independent check of each three-letter window.
    for length in range(7):
        for letters in product("abc", repeat=length):
            s = "".join(letters)
            expected = len(s) >= 3 and all(
                len(set(s[start : start + 3])) == 3
                for start in range(len(s) - 2)
            )
            assert is_happy(s) is expected, f"Unexpected result for {s!r}"
