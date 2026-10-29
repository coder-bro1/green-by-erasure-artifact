from itertools import product

import pytest

from solution import is_happy


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("", False),
        ("a", False),
        ("aa", False),
        ("ab", False),
        ("abcd", True),
        ("aabb", False),
        ("adb", True),
        ("xyy", False),
        ("aaa", False),
        ("aab", False),
        ("aba", False),
        ("abb", False),
        ("abcabc", True),
        ("abca", True),
        ("abcdd", False),
        ("abcdb", False),
        ("aabcde", False),
        ("abcddefg", False),
        ("AaB", True),
        ("αβγ", True),
        ("αβα", False),
    ],
)
def test_is_happy_examples_and_edge_cases(s, expected):
    assert is_happy(s) is expected


def test_is_happy_exhaustive_short_strings():
    """Check all short strings, including every arrangement of repeated letters."""
    for length in range(7):
        for letters in product("abc", repeat=length):
            s = "".join(letters)
            expected = len(s) >= 3 and all(
                len(set(s[i : i + 3])) == 3 for i in range(len(s) - 2)
            )
            assert is_happy(s) is expected, f"Incorrect result for {s!r}"
