from itertools import product

import pytest

from solution import cycpattern_check


@pytest.mark.parametrize(
    "text, pattern, expected",
    [
        ("abcd", "abd", False),
        ("hello", "ell", True),
        ("whassup", "psus", False),
        ("abab", "baa", True),
        ("efef", "eeff", False),
        ("himenss", "simen", True),
        ("", "", True),
        ("abc", "", True),
        ("", "a", False),
        ("ab", "abc", False),
        ("abc", "abc", True),
        ("xabc", "abc", True),
        ("abcx", "abc", True),
        ("aaaa", "aa", True),
        ("aaaa", "ab", False),
        ("ABC", "abc", False),
        ("x", "x", True),
        ("x", "y", False),
        ("x\u00e9\u732b\u03bbx", "\u03bb\u00e9\u732b", True),
        ("x a!x", "! a", True),
    ],
)
def test_documented_examples_and_edge_cases(text, pattern, expected):
    assert cycpattern_check(text, pattern) is expected


@pytest.mark.parametrize("offset", range(5))
def test_every_rotation(offset):
    pattern = "abcde"
    rotation = pattern[offset:] + pattern[:offset]
    assert cycpattern_check("--" + rotation + "--", pattern) is True


def test_exhaustive_short_binary_words():
    words = [
        "".join(letters)
        for length in range(5)
        for letters in product("ab", repeat=length)
    ]
    for text in words:
        for pattern in words:
            # Equal-length strings are rotations iff one occurs in the doubled other.
            expected = pattern == "" or any(
                pattern in (window + window)
                for start in range(len(text) - len(pattern) + 1)
                for window in [text[start : start + len(pattern)]]
            )
            assert cycpattern_check(text, pattern) is expected, (text, pattern)
