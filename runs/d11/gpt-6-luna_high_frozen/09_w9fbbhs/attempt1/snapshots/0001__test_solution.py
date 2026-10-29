import pytest

from solution import cycpattern_check


@pytest.mark.parametrize(
    ("text", "pattern"),
    [
        ("hello", "ell"),
        ("himenss", "simen"),
        ("abcabc", "cab"),
    ],
)
def test_returns_true_when_pattern_is_a_substring(text, pattern):
    assert cycpattern_check(text, pattern) is True


@pytest.mark.parametrize(
    ("text", "pattern"),
    [
        ("abcd", "abd"),
        ("whassup", "psus"),
        ("efef", "eeff"),
        ("short", "longer"),
        ("CaseSensitive", "casesensitive"),
    ],
)
def test_returns_false_when_pattern_is_not_a_substring(text, pattern):
    assert cycpattern_check(text, pattern) is False


def test_matches_pattern_at_start_or_end():
    assert cycpattern_check("pattern-tail", "pattern") is True
    assert cycpattern_check("head-pattern", "pattern") is True
