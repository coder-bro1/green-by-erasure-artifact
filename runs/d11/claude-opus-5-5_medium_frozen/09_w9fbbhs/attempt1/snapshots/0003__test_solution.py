import itertools

import pytest

from solution import cycpattern_check


def reference(a, b):
    """Spec oracle: True if b or any rotation of b is a substring of a."""
    return any(b[i:] + b[:i] in a for i in range(max(len(b), 1)))


ROTATION_BUG = (
    "Known bug in solution.py: the inner loop is range(len(b) - l + 1) == range(1), "
    "so only b itself is compared and rotations of b are never checked."
)


# --- Docstring examples -----------------------------------------------------

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


@pytest.mark.xfail(reason=ROTATION_BUG, strict=True)
@pytest.mark.parametrize(
    "a, b",
    [
        ("abab", "baa"),       # rotation "aba" is in "abab"
        ("himenss", "simen"),  # rotation "imens" is in "himenss"
    ],
)
def test_docstring_examples_requiring_rotation(a, b):
    assert cycpattern_check(a, b) is True


# --- Direct substring (rotation 0) ------------------------------------------

@pytest.mark.parametrize(
    "a, b",
    [
        ("hello", "hello"),   # whole string
        ("hello", "he"),      # prefix
        ("hello", "lo"),      # suffix
        ("hello", "l"),       # single char
        ("aaaa", "aa"),       # repeated chars
        ("xyzabc", "zab"),
    ],
)
def test_direct_substring_is_true(a, b):
    assert cycpattern_check(a, b) is True


# --- No rotation matches -----------------------------------------------------

@pytest.mark.parametrize(
    "a, b",
    [
        ("hello", "z"),
        ("abc", "abcd"),      # b longer than a
        ("", "a"),            # empty a, non-empty b
        ("abcdef", "xyz"),
        ("aaaa", "ab"),       # rotations "ab"/"ba" both absent
        ("Hello", "hello"),   # case-sensitive
    ],
)
def test_no_match_is_false(a, b):
    assert cycpattern_check(a, b) is False


# --- Edge cases --------------------------------------------------------------

def test_empty_b_is_substring_of_anything():
    assert cycpattern_check("abc", "") is True


def test_both_empty():
    assert cycpattern_check("", "") is True


def test_returns_bool():
    assert isinstance(cycpattern_check("abc", "b"), bool)
    assert isinstance(cycpattern_check("abc", "z"), bool)


def test_inputs_not_mutated():
    a, b = "abcd", "bc"
    cycpattern_check(a, b)
    assert (a, b) == ("abcd", "bc")


# --- Rotation-only matches (spec behaviour the implementation misses) --------

@pytest.mark.xfail(reason=ROTATION_BUG, strict=True)
@pytest.mark.parametrize(
    "a, b",
    [
        ("abcd", "cdab"),     # rotation "abcd" equals a
        ("xxbcaxx", "abc"),   # rotation "bca"
        ("cab", "abc"),       # rotation "cab"
    ],
)
def test_rotation_only_match(a, b):
    assert cycpattern_check(a, b) is True


# --- Agreement with oracle on cases where rotations do not matter ------------

def _small_cases():
    alphabet = "ab"
    words = [""] + [
        "".join(p) for n in range(1, 5) for p in itertools.product(alphabet, repeat=n)
    ]
    for a in words:
        for b in words:
            if len(b) <= 3:
                yield a, b


@pytest.mark.parametrize("a, b", list(_small_cases()))
def test_matches_oracle_when_rotation_is_irrelevant(a, b):
    # Only compare where the answer does not depend on non-trivial rotations:
    # either b itself is in a, or no rotation of b is in a.
    expected = reference(a, b)
    if expected and b not in a:
        pytest.skip("answer depends on a non-trivial rotation (known bug)")
    assert cycpattern_check(a, b) is expected
