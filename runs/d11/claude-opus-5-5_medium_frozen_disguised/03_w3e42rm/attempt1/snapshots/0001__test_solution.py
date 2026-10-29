"""Tests for solution.contains_rotation.

Spec (from the docstring): return True when `word`, or any rotation of
`word`, occurs as a substring of `text`; otherwise False.

KNOWN BUG: the inner loop in solution.py iterates over
range(len(word) - size + 1), which is always range(1), so only the
unrotated word is ever compared. Cases that require a non-trivial rotation
are marked xfail(strict=True): they document the bug, and will start
failing (XPASS -> error) once the bug is fixed, signalling that the marker
should be removed.
"""
import pytest

from solution import contains_rotation

rotation_bug = pytest.mark.xfail(
    strict=True,
    reason="BUG: solution.py only checks the unrotated word (inner loop runs once)",
)


def reference(text, word):
    """Straightforward implementation of the documented spec."""
    if not word:
        return True
    return any(word[k:] + word[:k] in text for k in range(len(word)))


# --- Behaviour the current implementation gets right -----------------------

@pytest.mark.parametrize(
    "text, word",
    [
        ("network", "net"),
        ("network", "work"),
        ("network", "network"),
        ("abc", "b"),
        ("aaaa", "aa"),
    ],
)
def test_word_itself_present(text, word):
    assert contains_rotation(text, word) is True


@pytest.mark.parametrize(
    "text, word",
    [
        ("abcde", "eab"),        # docstring example
        ("abc", "xyz"),
        ("abc", "abcd"),         # word longer than text
        ("", "a"),               # empty text
        ("network", "kron"),     # no rotation of 'kron' occurs
        ("aabb", "abab"),
    ],
)
def test_no_rotation_present(text, word):
    assert contains_rotation(text, word) is False


def test_docstring_example_abcde_eab():
    assert contains_rotation("abcde", "eab") is False


def test_empty_word_is_always_found():
    assert contains_rotation("abc", "") is True
    assert contains_rotation("", "") is True


def test_returns_bool():
    assert isinstance(contains_rotation("abc", "ab"), bool)
    assert isinstance(contains_rotation("abc", "zz"), bool)


def test_case_sensitive():
    assert contains_rotation("Network", "net") is False


# --- Rotation behaviour (currently broken) ---------------------------------

@rotation_bug
def test_docstring_example_network_orkw():
    # 'work' is a rotation of 'orkw' and occurs in 'network'
    assert contains_rotation("network", "orkw") is True


@rotation_bug
def test_docstring_example_abc_cb():
    # 'bc' is a rotation of 'cb'
    assert contains_rotation("abc", "cb") is True


@rotation_bug
@pytest.mark.parametrize(
    "text, word",
    [
        ("hello world", "lohel"),   # rotation 'hello'
        ("xyzabc", "cab"),          # rotation 'abc'
        ("rotation", "tionrota"),   # rotation 'rotation'
        ("ab", "ba"),
    ],
)
def test_proper_rotation_present(text, word):
    assert contains_rotation(text, word) is True


# --- Cross-check against the reference spec on cases the bug doesn't touch --

@pytest.mark.parametrize(
    "text, word",
    [
        ("abcabc", "abc"),
        ("mississippi", "ssi"),
        ("mississippi", "xyz"),
        ("short", "muchlongerword"),
        ("aaaa", "a"),
    ],
)
def test_matches_reference_when_no_rotation_needed(text, word):
    assert contains_rotation(text, word) == reference(text, word)
