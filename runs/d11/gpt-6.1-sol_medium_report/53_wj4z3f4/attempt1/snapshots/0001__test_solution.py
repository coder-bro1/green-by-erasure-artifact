"""Tests for the palindrome contracts documented in solution.py."""

import json
from pathlib import Path
import subprocess
import sys

import pytest

from solution import is_palindrome


@pytest.mark.parametrize(
    ("string", "expected"),
    [
        ("", True),
        ("a", True),
        ("aa", True),
        ("aba", True),
        ("abba", True),
        ("racecar", True),
        ("   ", True),
        ("a a", True),
        ("å😊å", True),
        ("ab", False),
        ("cat", False),
        ("aab", False),
        ("Aa", False),
        (" aba", False),
        ("å😊b", False),
    ],
)
def test_is_palindrome(string, expected):
    assert is_palindrome(string) is expected


def call_make_palindrome(string):
    """Isolate calls so a nonterminating implementation cannot hang pytest."""
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import json, sys; from solution import make_palindrome; "
                "print(json.dumps(make_palindrome(sys.argv[1])))",
                string,
            ],
            cwd=Path(__file__).resolve().parent,
            capture_output=True,
            text=True,
            timeout=2,
            check=True,
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"make_palindrome({string!r}) did not terminate within 2 seconds")
    return json.loads(result.stdout)


@pytest.mark.parametrize(
    ("string", "expected"),
    [
        ("", ""),
        ("a", "a"),
        ("aa", "aa"),
        ("aba", "aba"),
        ("abba", "abba"),
        ("racecar", "racecar"),
        ("   ", "   "),
        ("å😊å", "å😊å"),
        ("cat", "catac"),
        ("cata", "catac"),
        ("ab", "aba"),
        ("aab", "aabaa"),
        ("abab", "ababa"),
        ("Aa", "AaA"),
        ("åb", "åbå"),
        ("a b", "a b a"),
    ],
)
def test_make_palindrome_returns_shortest_extension(string, expected):
    actual = call_make_palindrome(string)
    assert actual == expected
    assert actual.startswith(string)
    assert is_palindrome(actual)

    # No shorter prefix of the answer may already satisfy the contract.
    for length in range(len(string), len(actual)):
        assert not is_palindrome(actual[:length])
