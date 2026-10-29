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
        ("aab", False),
        ("aba", False),
        ("aaa", False),
        ("abcadef", True),
        ("abcabcabc", True),
        ("abccde", False),
        ("abcdd", False),
        ("abcdb", True),
        ("abcdc", False),
        ("aAa", False),
        ("aAb", True),
        ("a b", True),
        ("a  b", False),
        ("αβγ", True),
        ("αβα", False),
    ],
)
def test_is_happy_examples_and_edge_cases(s, expected):
    assert is_happy(s) is expected


def test_is_happy_matches_definition_for_all_short_strings():
    for length in range(8):
        for characters in product("abc", repeat=length):
            s = "".join(characters)
            expected = len(s) >= 3 and all(
                len(set(s[start : start + 3])) == 3
                for start in range(len(s) - 2)
            )
            assert is_happy(s) is expected, f"Unexpected result for {s!r}"
