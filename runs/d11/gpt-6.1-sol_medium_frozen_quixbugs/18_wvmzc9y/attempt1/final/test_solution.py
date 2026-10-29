"""Regression tests and explicit checks for known wrap contract defects."""

import json
from pathlib import Path
import subprocess
import sys

import pytest

from solution import wrap


@pytest.mark.parametrize("cols", [1, 2, 10, 100])
def test_empty_text(cols):
    assert wrap("", cols) == []


@pytest.mark.parametrize(
    ("text", "cols", "expected"),
    [
        ("a", 1, []),
        ("abc", 3, []),
        ("abc", 10, []),
        ("abcd", 3, ["abc"]),
        ("abcdef", 3, ["abc"]),
        ("abcdefg", 3, ["abc", "def"]),
        ("abcd", 1, ["a", "b", "c"]),
        ("abcdefghij", 4, ["abcd", "efgh"]),
        ("\u00e9\u732b\U0001f642xyz", 2, ["\u00e9\u732b", "\U0001f642x"]),
    ],
)
def test_current_unbroken_word_behavior(text, cols, expected):
    # Characterize the emitted chunks; the missing final chunk is tested below.
    result = wrap(text, cols)
    assert result == expected
    assert all(len(line) == cols for line in result)
    assert text.startswith("".join(result))


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="wrap never appends the remaining text after its loop",
)
@pytest.mark.parametrize(
    ("text", "cols", "expected"),
    [
        ("abc", 10, ["abc"]),
        ("abc", 3, ["abc"]),
        ("abcd", 3, ["abc", "d"]),
        ("abcdef", 3, ["abc", "def"]),
        ("abcd", 1, ["a", "b", "c", "d"]),
    ],
)
def test_preserves_final_chunk(text, cols, expected):
    assert wrap(text, cols) == expected


@pytest.mark.xfail(
    strict=True,
    raises=subprocess.TimeoutExpired,
    reason="a space at index zero makes wrap loop without consuming text",
)
@pytest.mark.parametrize(
    ("text", "cols"),
    [("hello world", 5), (" abc", 2), ("abc  dddd", 3)],
)
def test_space_wrapping_terminates_and_preserves_text(text, cols):
    # Isolate the infinite loop so it cannot hang the pytest process.
    script = (
        "import json, sys; from solution import wrap; "
        "print(json.dumps(wrap(sys.argv[1], int(sys.argv[2]))))"
    )
    completed = subprocess.run(
        [sys.executable, "-B", "-c", script, text, str(cols)],
        cwd=Path(__file__).resolve().parent,
        capture_output=True,
        text=True,
        timeout=1,
        check=True,
    )
    lines = json.loads(completed.stdout)
    assert "".join(lines) == text
    assert all(0 < len(line) <= cols for line in lines)
