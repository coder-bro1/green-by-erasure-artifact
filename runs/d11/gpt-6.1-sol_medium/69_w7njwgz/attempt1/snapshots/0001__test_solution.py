from itertools import product

import pytest

from solution import cycpattern_check


@pytest.mark.parametrize(
    ("text", "pattern", "expected"),
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
        ("a", "a", True),
        ("a", "b", False),
        ("abc", "abc", True),
        ("abc", "acb", False),
        ("xxabcdyy", "abcd", True),
        ("abcdxx", "abcd", True),
        ("xxabcd", "abcd", True),
        ("aaaa", "aaa", True),
        ("aaaa", "aab", False),
        ("abab", "aabb", False),
        ("ABCD", "abcd", False),
        ("xx\u00e9\u732b\U0001f642yy", "\U0001f642\u00e9\u732b", True),
        ("x b\nay", "a b\n", True),
        ("x\x00aby", "ab\x00", True),
    ],
)
def test_examples_and_edge_cases(text, pattern, expected):
    assert cycpattern_check(text, pattern) is expected


@pytest.mark.parametrize("rotation", ["abcd", "bcda", "cdab", "dabc"])
def test_every_rotation_matches(rotation):
    assert cycpattern_check(f"xx{rotation}yy", "abcd") is True


def test_text_boundary_does_not_wrap():
    assert cycpattern_check("dab", "bd") is False


def test_all_short_binary_strings_against_rotation_oracle():
    words = [
        "".join(chars)
        for length in range(5)
        for chars in product("ab", repeat=length)
    ]
    for text in words:
        for pattern in words:
            rotations = {
                pattern[offset:] + pattern[:offset]
                for offset in range(len(pattern))
            } or {""}
            expected = any(rotation in text for rotation in rotations)
            assert cycpattern_check(text, pattern) is expected, (text, pattern)
