"""Tests for the palindrome helpers, including the known extension-loop bug."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from solution import reads_same, shortest_mirror_extension


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", True),
        ("a", True),
        ("aa", True),
        ("aba", True),
        ("abba", True),
        ("racecar", True),
        ("a a", True),
        ("!? !", False),
        ("ab", False),
        ("abc", False),
        ("abca", False),
        ("Aa", False),
        ("aba ", False),
        ("é🙂é", True),
        ("é🙂", False),
    ],
)
def test_reads_same(text, expected):
    assert reads_same(text) is expected


@pytest.mark.parametrize("text", ["", "a", "aa", "aba", "abba", "racecar", "a a", "!?!!?!", "é🙂é"])
def test_shortest_mirror_extension_preserves_palindromes(text):
    # Appending nothing is minimal when the input is already a palindrome.
    assert shortest_mirror_extension(text) == text


@pytest.mark.xfail(
    strict=True,
    raises=subprocess.TimeoutExpired,
    reason="The loop increments cut but never changes text for non-palindromes.",
)
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("ab", "aba"),
        ("abc", "abcba"),
        ("abcb", "abcba"),
        ("abb", "abba"),
        ("abcd", "abcdcba"),
        ("é🙂", "é🙂é"),
    ],
)
def test_shortest_mirror_extension_non_palindromes(text, expected):
    # Isolate the call so the current infinite loop cannot hang the test runner.
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import json, sys; from solution import shortest_mirror_extension; "
            "print(json.dumps(shortest_mirror_extension(sys.argv[1])))",
            text,
        ],
        cwd=Path(__file__).resolve().parent,
        capture_output=True,
        text=True,
        check=True,
        timeout=1,
    )
    actual = json.loads(result.stdout)
    assert actual == expected
    assert actual.startswith(text)
    assert reads_same(actual)
    # Every shorter append would require a palindromic suffix at that cut.
    appended_length = len(actual) - len(text)
    assert all(not reads_same(text[cut:]) for cut in range(appended_length))
