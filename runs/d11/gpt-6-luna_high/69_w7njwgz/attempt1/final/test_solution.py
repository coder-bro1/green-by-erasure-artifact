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


@pytest.mark.parametrize("rotation", ["abc", "bca", "cab"])
def test_finds_each_rotation_as_a_substring(rotation):
    assert cycpattern_check(f"x{rotation}y", "abc") is True


def test_accepts_pattern_itself_as_substring():
    assert cycpattern_check("xxabcxx", "abc") is True


@pytest.mark.parametrize(
    ("word", "pattern"),
    [
        ("ab", "abc"),  # The pattern cannot fit in the word.
        ("acb", "abc"),  # Same letters, but no cyclic ordering occurs.
        ("xyzabc", "cabd"),  # A near-match must not be accepted.
    ],
)
def test_returns_false_when_no_rotation_is_a_substring(word, pattern):
    assert cycpattern_check(word, pattern) is False


def test_empty_pattern_is_a_substring():
    assert cycpattern_check("anything", "") is True


def test_empty_word_cannot_contain_nonempty_pattern():
    assert cycpattern_check("", "a") is False
