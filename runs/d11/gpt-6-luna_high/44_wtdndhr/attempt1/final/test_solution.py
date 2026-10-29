import pytest

from solution import cycpattern_check


@pytest.mark.parametrize(
    ("word", "pattern", "expected"),
    [
        ("abcd", "abd", False),
        ("hello", "ell", True),
        ("whassup", "psus", False),
        ("abab", "baa", True),
        ("efef", "eeff", False),
        ("himenss", "simen", True),
    ],
)
def test_documented_examples(word, pattern, expected):
    assert cycpattern_check(word, pattern) is expected


def test_matches_rotation_at_the_start_or_middle_of_word():
    assert cycpattern_check("xxbcay", "abc") is True
    assert cycpattern_check("xxcabyy", "abc") is True


def test_does_not_match_when_no_rotation_is_a_substring():
    assert cycpattern_check("abxx", "abc") is False


def test_pattern_longer_than_word_cannot_match():
    assert cycpattern_check("ab", "abc") is False


def test_repeated_characters_are_handled():
    assert cycpattern_check("xxbaa", "aab") is True
    assert cycpattern_check("xxabc", "aaa") is False


def test_empty_pattern_is_a_substring():
    assert cycpattern_check("anything", "") is True
    assert cycpattern_check("", "") is True


def test_nonempty_pattern_does_not_match_empty_word():
    assert cycpattern_check("", "a") is False
