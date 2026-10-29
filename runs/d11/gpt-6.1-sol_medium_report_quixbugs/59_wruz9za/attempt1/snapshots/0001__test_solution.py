"""Tests for the wrapping contract documented in solution.wrap."""

import json
from pathlib import Path
import subprocess
import sys

import pytest

from solution import wrap


def test_empty_text():
    assert wrap("", 1) == []


@pytest.mark.parametrize(
    "text, cols",
    [
        pytest.param("a", 1, id="single-character"),
        pytest.param("hello", 5, id="exact-width"),
        pytest.param("hello", 10, id="below-width"),
        pytest.param(" hi", 3, id="leading-space"),
        pytest.param("hi ", 3, id="trailing-space"),
        pytest.param("a  b", 4, id="repeated-spaces"),
        pytest.param("   ", 3, id="spaces-only"),
    ],
)
def test_text_that_fits_is_preserved(text, cols):
    assert wrap(text, cols) == [text]


@pytest.mark.parametrize(
    "text, cols, expected",
    [
        pytest.param("abcdef", 3, ["abc", "def"], id="exact-multiple"),
        pytest.param("abcdefg", 3, ["abc", "def", "g"], id="partial-last-line"),
        pytest.param("abc", 1, ["a", "b", "c"], id="width-one"),
    ],
)
def test_long_word_is_split_only_as_needed(text, cols, expected):
    assert wrap(text, cols) == expected


def test_wrap_at_space_preserves_words_and_original_spacing():
    assert wrap("one two three", 7) == ["one two", " three"]


@pytest.mark.parametrize(
    "text, cols, expected",
    [
        pytest.param("    ", 2, ["  ", "  "], id="spaces-only"),
        pytest.param(" abc", 3, [" ", "abc"], id="leading-space-before-word"),
    ],
)
def test_leading_spaces_make_progress(text, cols, expected):
    # Isolate calls that might loop forever, keeping the pytest run bounded.
    script = (
        "import json, sys; from solution import wrap; "
        "print(json.dumps(wrap(sys.argv[1], int(sys.argv[2]))))"
    )
    try:
        result = subprocess.run(
            [sys.executable, "-c", script, text, str(cols)],
            cwd=Path(__file__).resolve().parent,
            capture_output=True,
            text=True,
            timeout=2,
            check=True,
        )
    except subprocess.TimeoutExpired:
        pytest.fail("wrap did not terminate within 2 seconds", pytrace=False)
    assert json.loads(result.stdout) == expected
