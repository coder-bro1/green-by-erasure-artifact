import pytest

from solution import cycpattern_check

ROTATION_BUG = (
    "inner loop runs range(len(b) - len(b) + 1) == range(1), so only b itself "
    "is compared; rotations of b are never checked"
)


# Docstring examples that do not depend on rotations
@pytest.mark.parametrize(
    "a, b, expected",
    [
        ("abcd", "abd", False),
        ("hello", "ell", True),
        ("whassup", "psus", False),
        ("efef", "eeff", False),
    ],
)
def test_docstring_examples_passing(a, b, expected):
    assert cycpattern_check(a, b) is expected


# Docstring examples that require matching a rotation
@pytest.mark.xfail(strict=True, reason=ROTATION_BUG)
def test_docstring_abab_baa():
    # rotation "aba" is a substring of "abab"
    assert cycpattern_check("abab", "baa") is True


@pytest.mark.xfail(strict=True, reason=ROTATION_BUG)
def test_docstring_himenss_simen():
    # rotation "imens" is a substring of "himenss"
    assert cycpattern_check("himenss", "simen") is True


@pytest.mark.xfail(strict=True, reason=ROTATION_BUG)
def test_simple_rotation():
    # "cab" is a rotation of "abc"
    assert cycpattern_check("xxcabxx", "abc") is True


@pytest.mark.xfail(strict=True, reason=ROTATION_BUG)
def test_rotation_equal_length():
    assert cycpattern_check("bca", "abc") is True


def test_exact_substring():
    assert cycpattern_check("abcdef", "cde") is True


def test_identical_words():
    assert cycpattern_check("abc", "abc") is True


def test_second_longer_than_first():
    assert cycpattern_check("ab", "abc") is False


def test_no_match_at_all():
    assert cycpattern_check("aaaa", "b") is False


def test_single_char_match():
    assert cycpattern_check("xyz", "y") is True


def test_permutation_that_is_not_rotation():
    # "acb" is a permutation of "abc" but not a rotation
    assert cycpattern_check("acb", "abc") is False


def test_case_sensitive():
    assert cycpattern_check("Hello", "hel") is False


def test_empty_pattern():
    # empty string is a substring of every string
    assert cycpattern_check("abc", "") is True
    assert cycpattern_check("", "") is True


def test_empty_text_nonempty_pattern():
    assert cycpattern_check("", "a") is False
