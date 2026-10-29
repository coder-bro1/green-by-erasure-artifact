import pytest

from solution import cycpattern_check


@pytest.mark.parametrize(
    ("word", "pattern", "expected"),
    [
        # Examples from the function's docstring.
        ("abcd", "abd", False),
        ("hello", "ell", True),
        ("whassup", "psus", False),
        ("abab", "baa", True),
        ("efef", "eeff", False),
        ("himenss", "simen", True),
        # Rotations at the beginning, middle, and end of a word.
        ("cdeab", "abc", True),
        ("xxcabyy", "abc", True),
        ("xxbcayy", "abc", True),
        # Substring matching is contiguous and case-sensitive.
        ("abXcd", "abc", False),
        ("xxAbcyy", "abc", False),
        # Equal strings, overlapping candidates, and boundary lengths.
        ("abc", "abc", True),
        ("aaaaa", "aaa", True),
        ("ab", "abc", False),
        ("", "a", False),
        ("abc", "", True),
        ("", "", True),
    ],
)
def test_cycpattern_check(word, pattern, expected):
    assert cycpattern_check(word, pattern) is expected
