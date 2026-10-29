"""Tests for palindrome helpers, including the known non-terminating cases."""

import itertools
import json
from pathlib import Path
import subprocess
import sys

import pytest

from solution import is_palindrome, make_palindrome


@pytest.mark.parametrize(
    ("string", "expected"),
    [
        ("", True),
        ("a", True),
        ("aa", True),
        ("abba", True),
        ("racecar", True),
        ("ab", False),
        ("cat", False),
        ("Racecar", False),
        ("aba ", False),
        ("a b a", True),
        ("a\nb\na", True),
        ("été", True),
        ("🙂a🙂", True),
        ("éa", False),
    ],
)
def test_is_palindrome(string, expected):
    assert is_palindrome(string) is expected


def test_is_palindrome_exhaustive_short_strings():
    for length in range(7):
        for characters in itertools.product("ab", repeat=length):
            string = "".join(characters)
            expected = all(
                string[index] == string[-index - 1]
                for index in range(length // 2)
            )
            assert is_palindrome(string) is expected


@pytest.mark.parametrize(
    "string", ["", "a", "aa", "aba", "abba", "racecar", " ", "a b a", "été", "🙂a🙂"]
)
def test_make_palindrome_preserves_existing_palindromes(string):
    # An existing palindrome needs no appended characters, so it is shortest.
    assert make_palindrome(string) == string


@pytest.mark.parametrize(
    ("string", "expected"),
    [("cat", "catac"), ("cata", "catac"), ("ab", "aba")],
)
@pytest.mark.xfail(
    strict=True,
    raises=subprocess.TimeoutExpired,
    reason="make_palindrome checks the unchanged non-palindromic string forever",
)
def test_make_palindrome_appends_shortest_completion(string, expected):
    # Isolate the infinite loop so a regression test cannot hang pytest.
    program = (
        "import json, sys; from solution import make_palindrome; "
        "print(json.dumps(make_palindrome(sys.argv[1])))"
    )
    result = subprocess.run(
        [sys.executable, "-c", program, string],
        cwd=Path(__file__).resolve().parent,
        capture_output=True,
        text=True,
        timeout=2,
        check=True,
    )
    assert json.loads(result.stdout) == expected
