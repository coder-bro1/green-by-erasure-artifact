"""Tests for the wrapping and whitespace guarantees in solution.wrap."""

import sys

import pytest

from solution import wrap


def bounded_wrap(text, cols):
    """Stop a non-progressing wrap loop before it hangs or exhausts memory."""
    previous_trace = sys.gettrace()
    remaining_events = 10_000

    def trace(frame, event, arg):
        nonlocal remaining_events
        if frame.f_code is wrap.__code__:
            remaining_events -= 1
            if remaining_events == 0:
                raise RuntimeError("wrap did not finish within 10,000 trace events")
        return trace

    sys.settrace(trace)
    try:
        return wrap(text, cols)
    finally:
        sys.settrace(previous_trace)


@pytest.mark.parametrize(
    "text, cols, expected",
    [
        pytest.param("", 1, [""], id="empty-text"),
        pytest.param("a", 1, ["a"], id="single-character"),
        pytest.param("hello", 10, ["hello"], id="shorter-than-width"),
        pytest.param("hello", 5, ["hello"], id="exact-width"),
        pytest.param(" a  b ", 6, [" a  b "], id="unwrapped-spaces"),
        pytest.param("abc def", 4, ["abc", " def"], id="space-at-line-end"),
        pytest.param("abc def", 6, ["abc", " def"], id="avoid-splitting-fitting-word"),
        pytest.param("alpha beta gamma", 7, ["alpha", " beta", " gamma"], id="multiple-lines"),
        pytest.param("one two three", 8, ["one two", " three"], id="multiple-words-per-line"),
        pytest.param("abcdefgh", 3, ["abc", "def", "gh"], id="split-long-word"),
        pytest.param("abcdef", 3, ["abc", "def"], id="long-word-exact-multiple"),
        pytest.param("abc", 1, ["a", "b", "c"], id="minimum-width"),
        pytest.param("abcdef gh", 4, ["abcd", "ef", " gh"], id="long-word-before-short-word"),
        pytest.param("ab  cd", 4, ["ab ", " cd"], id="preserve-repeated-spaces"),
        pytest.param("ab  ", 3, ["ab ", " "], id="preserve-trailing-spaces"),
        pytest.param("  ab cd", 5, ["  ab", " cd"], id="preserve-leading-spaces"),
        pytest.param("ab\tcd", 3, ["ab\t", "cd"], id="tabs-are-not-space-breaks"),
        pytest.param("ab\ncd", 3, ["ab\n", "cd"], id="preserve-newline-character"),
        pytest.param("café naïve", 6, ["café", " naïve"], id="unicode-words"),
    ],
)
def test_wrap_expected_lines(text, cols, expected):
    result = bounded_wrap(text, cols)

    assert result == expected
    assert "".join(result) == text
    assert all(len(line) <= cols for line in result)


@pytest.mark.parametrize("cols", [1, 2, 3, 7, 16, 26, 30])
def test_long_word_preserves_every_character_and_obeys_width(cols):
    text = "abcdefghijklmnopqrstuvwxyz"

    result = bounded_wrap(text, cols)

    assert result == [text[start : start + cols] for start in range(0, len(text), cols)]
    assert "".join(result) == text
    assert all(0 < len(line) <= cols for line in result)


@pytest.mark.parametrize(
    "text, cols, expected",
    [
        pytest.param("abc def", 3, ["abc", " ", "def"], id="next-word-fills-width"),
        pytest.param(" abcd", 4, [" ", "abcd"], id="leading-space-before-fitting-word"),
        pytest.param("ab abcdef", 3, ["ab", " ab", "cde", "f"], id="later-word-exceeds-width"),
        pytest.param("ab  cd", 2, ["ab", "  ", "cd"], id="repeated-spaces-at-boundary"),
        pytest.param("   ", 1, [" ", " ", " "], id="spaces-only-at-minimum-width"),
    ],
)
def test_wrap_must_make_progress_and_preserve_words(text, cols, expected):
    assert bounded_wrap(text, cols) == expected
