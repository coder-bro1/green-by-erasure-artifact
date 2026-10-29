import os
import subprocess
import sys

import pytest

from solution import is_palindrome, make_palindrome

HERE = os.path.dirname(os.path.abspath(__file__))
TIMEOUT = 5

INFINITE_LOOP_REASON = (
    "make_palindrome loops forever on non-palindromic input: the while loop tests "
    "is_palindrome(string) instead of is_palindrome(string[beginning_of_suffix:])"
)


def run_make_palindrome(arg):
    """Call make_palindrome in a subprocess so an infinite loop becomes a failure, not a hang."""
    code = (
        "import sys; sys.path.insert(0, sys.argv[1]);"
        "from solution import make_palindrome;"
        "sys.stdout.write(repr(make_palindrome(sys.argv[2])))"
    )
    try:
        out = subprocess.run(
            [sys.executable, "-c", code, HERE, arg],
            capture_output=True, text=True, timeout=TIMEOUT, check=True,
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"make_palindrome({arg!r}) did not return within {TIMEOUT}s")
    return eval(out.stdout)


# ---------- is_palindrome ----------

@pytest.mark.parametrize("s", ["", "a", "aa", "aba", "abba", "racecar", "zbcbz"])
def test_is_palindrome_true(s):
    assert is_palindrome(s) is True


@pytest.mark.parametrize("s", ["ab", "abc", "abca", "Aa", "xywyz"])
def test_is_palindrome_false(s):
    assert is_palindrome(s) is False


# ---------- make_palindrome: inputs that already are palindromes ----------

@pytest.mark.parametrize("s", ["", "a", "aa", "aba", "racecar", "abba"])
def test_make_palindrome_already_palindrome(s):
    assert make_palindrome(s) == s


# ---------- make_palindrome: non-palindromic inputs (docstring examples and more) ----------

@pytest.mark.xfail(strict=True, reason=INFINITE_LOOP_REASON)
@pytest.mark.parametrize(
    "s, expected",
    [
        ("cat", "catac"),      # docstring example
        ("cata", "catac"),     # docstring example
        ("ab", "aba"),
        ("abc", "abcba"),
        ("xyz", "xyzyx"),
        ("abb", "abba"),
        ("jerry", "jerryrrej"),
    ],
)
def test_make_palindrome_non_palindrome(s, expected):
    result = run_make_palindrome(s)
    assert result == expected
    assert is_palindrome(result)
    assert result.startswith(s)
