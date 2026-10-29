import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solution import is_palindrome, make_palindrome


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", True),
        ("a", True),
        ("racecar", True),
        ("abba", True),
        ("python", False),
        ("Racecar", False),
        ("あいあ", True),
    ],
)
def test_is_palindrome(value, expected):
    assert is_palindrome(value) is expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", ""),
        ("a", "a"),
        ("racecar", "racecar"),
        ("abba", "abba"),
    ],
)
def test_make_palindrome_when_input_is_already_palindrome(value, expected):
    assert make_palindrome(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [("cat", "catac"), ("cata", "catac")],
)
@pytest.mark.xfail(
    strict=True,
    reason="make_palindrome never updates its loop condition, so non-palindromic input does not terminate",
)
def test_make_palindrome_appends_reverse_of_prefix(value, expected):
    # Run separately so the current infinite loop cannot hang the pytest process.
    script = (
        "import sys; from solution import make_palindrome; "
        "print(make_palindrome(sys.argv[1]))"
    )
    try:
        result = subprocess.run(
            [sys.executable, "-c", script, value],
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True,
            text=True,
            timeout=1.5,
            check=True,
        )
        actual = result.stdout.rstrip("\r\n")
    except subprocess.TimeoutExpired:
        actual = "<timed out>"

    assert actual == expected
