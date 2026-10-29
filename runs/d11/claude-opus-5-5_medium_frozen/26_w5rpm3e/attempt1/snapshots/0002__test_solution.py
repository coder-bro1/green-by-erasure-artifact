import subprocess
import sys
from pathlib import Path

import pytest

from solution import is_palindrome, make_palindrome

HERE = Path(__file__).resolve().parent
TIMEOUT = 3  # seconds


# ---------------------------------------------------------------- is_palindrome

@pytest.mark.parametrize("s", ["", "a", "aa", "aba", "abba", "racecar", "xywyx", "12321", "  "])
def test_is_palindrome_true(s):
    assert is_palindrome(s) is True


@pytest.mark.parametrize("s", ["ab", "abc", "zbcd", "xywyz", "Aa", "abca", "race car"])
def test_is_palindrome_false(s):
    assert is_palindrome(s) is False


def test_is_palindrome_is_case_and_space_sensitive():
    assert not is_palindrome("Racecar")
    assert not is_palindrome("a ba")


# ------------------------------------------------- make_palindrome (safe inputs)
# Inputs that are already palindromes return before the buggy loop advances.

def test_make_palindrome_empty():
    assert make_palindrome("") == ""


@pytest.mark.parametrize("s", ["a", "x", "aa", "aba", "abba", "racecar", "xyx", "jerrrej"])
def test_make_palindrome_already_palindrome_unchanged(s):
    assert make_palindrome(s) == s


# ------------------------------------------ make_palindrome (non-palindromes)
# solution.py's loop tests is_palindrome(string) rather than the suffix
# string[beginning_of_suffix:], so it never terminates for non-palindromic
# input. Run in a subprocess with a timeout so the suite can't hang; marked
# strict xfail so these flip to XPASS (and fail the run) once the bug is fixed.

def _run_make_palindrome(s):
    code = f"from solution import make_palindrome; print(repr(make_palindrome({s!r})))"
    try:
        out = subprocess.run(
            [sys.executable, "-c", code],
            cwd=HERE, capture_output=True, text=True, timeout=TIMEOUT, check=True,
        ).stdout.strip()
    except subprocess.TimeoutExpired:
        pytest.fail(f"make_palindrome({s!r}) did not terminate within {TIMEOUT}s")
    return eval(out)


@pytest.mark.xfail(strict=True, reason="bug: loop checks whole string, not suffix -> infinite loop")
@pytest.mark.parametrize("s, expected", [
    ("cat", "catac"),
    ("cata", "catac"),
    ("xy", "xyx"),
    ("xyz", "xyzyx"),
    ("jerry", "jerryrrej"),
])
def test_make_palindrome_non_palindrome(s, expected):
    assert _run_make_palindrome(s) == expected


def test_make_palindrome_non_palindrome_hangs():
    """Documents current behavior: non-palindromic input never returns."""
    code = "from solution import make_palindrome; make_palindrome('ab')"
    with pytest.raises(subprocess.TimeoutExpired):
        subprocess.run([sys.executable, "-c", code], cwd=HERE,
                       capture_output=True, timeout=1)
