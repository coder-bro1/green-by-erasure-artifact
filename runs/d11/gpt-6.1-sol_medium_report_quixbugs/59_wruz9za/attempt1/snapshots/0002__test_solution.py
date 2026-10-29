"""Tests for the wrapping contract documented in solution.wrap."""

import json
from pathlib import Path
import subprocess
import sys

import pytest

from solution import wrap


def test_empty_text():
    assert wrap("", 1) == []


@pytest.mark.xfail(
    strict=True,
    reason="wrap omits the final line, returning [] for nonempty text that fits",
)
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
@pytest.mark.xfail(strict=True, reason="wrap never appends the final word fragment")
def test_long_word_is_split_only_as_needed(text, cols, expected):
    assert wrap(text, cols) == expected


@pytest.mark.xfail(strict=True, reason="wrap drops the final line and its spaces")
def test_wrap_at_space_preserves_words_and_original_spacing():
    assert wrap("one two three", 7) == ["one two", " three"]


@pytest.mark.xfail(strict=True, reason="wrap drops the final line of spaces")
def test_wrapped_spaces_are_preserved():
    assert wrap("    ", 2) == ["  ", "  "]


@pytest.mark.xfail(
    strict=True,
    reason="A split at space index 0 leaves text unchanged, so wrap loops forever",
)
def test_leading_spaces_make_progress():
    text, cols, expected = " abc", 3, [" ", "abc"]
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
