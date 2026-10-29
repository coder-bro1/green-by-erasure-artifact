import pytest

from solution import is_happy


@pytest.mark.parametrize("s", ["", "a", "aa", "ab", "\u00e9", "\u00e9\u03b2"])
def test_strings_shorter_than_three_are_not_happy(s):
    assert is_happy(s) is False


@pytest.mark.parametrize(
    "s",
    ["abc", "abcd", "adb", "abcdefg", "abcabc", "abca", "aAb", "\u00e9\u03b2\u03b3\u00e9"],
)
def test_every_consecutive_triple_is_distinct(s):
    # Repeated letters are allowed when they are at least three positions apart.
    assert is_happy(s) is True


@pytest.mark.parametrize("s", ["aaa", "aaaa", "aaabc", "bcaaa", "abcaaadef"])
def test_three_identical_consecutive_letters_are_not_happy(s):
    assert is_happy(s) is False


@pytest.mark.parametrize(
    "s",
    ["aab", "abb", "aba", "aabb", "xyy", "aabc", "abcc", "abcb", "abcdd ef".replace(" ", ""), "\u00e9\u03b2\u00e9"],
)
def test_two_repeated_letters_in_a_triple_are_not_happy(s):
    assert is_happy(s) is False
