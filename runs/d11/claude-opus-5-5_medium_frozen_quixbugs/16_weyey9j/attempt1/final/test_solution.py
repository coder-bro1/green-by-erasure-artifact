"""Tests for solution.levenshtein.

Note: solution.py has a known bug -- when the first characters match it adds
1 to the distance instead of 0 (``return 1 + levenshtein(source[1:], target[1:])``).
Tests asserting correct behaviour on inputs that share matching characters
are marked ``xfail(strict=True)`` so the suite documents the bug and will
start failing (XPASS) once it is fixed, prompting removal of the markers.
"""
import itertools

import pytest

from solution import levenshtein

BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py adds 1 on matching characters instead of 0",
)


# --- Behaviour that is correct in the current implementation ---------------

@pytest.mark.parametrize(
    "source, target, expected",
    [
        ("", "", 0),
        ("a", "", 1),
        ("", "a", 1),
        ("abc", "", 3),
        ("", "hello", 5),
    ],
)
def test_empty_strings(source, target, expected):
    assert levenshtein(source, target) == expected


@pytest.mark.parametrize(
    "source, target, expected",
    [
        ("a", "b", 1),
        ("abc", "xyz", 3),
        ("ab", "ba", 2),
        ("a", "xy", 2),
        ("xy", "a", 2),
    ],
)
def test_no_shared_positions(source, target, expected):
    # Inputs where no character match is ever useful, so the bug is not hit.
    assert levenshtein(source, target) == expected


@pytest.mark.parametrize(
    "source, target",
    [("kitten", "sitting"), ("flaw", "lawn"), ("abc", "abd"), ("", "xyz"), ("ab", "ba")],
)
def test_symmetry(source, target):
    assert levenshtein(source, target) == levenshtein(target, source)


@pytest.mark.parametrize(
    "source, target",
    [("kitten", "sitting"), ("flaw", "lawn"), ("abc", "abd"), ("a", "abcd"), ("", "xyz")],
)
def test_bounds(source, target):
    d = levenshtein(source, target)
    assert abs(len(source) - len(target)) <= d <= max(len(source), len(target))


def test_returns_int():
    assert isinstance(levenshtein("abc", "xyz"), int)


# --- Correct Levenshtein behaviour the current implementation gets wrong ---

@BUG
@pytest.mark.parametrize("s", ["a", "abc", "hello world"])
def test_identical_strings_have_zero_distance(s):
    assert levenshtein(s, s) == 0


@BUG
@pytest.mark.parametrize(
    "source, target, expected",
    [
        ("electron", "neutron", 3),  # docstring example
        ("kitten", "sitting", 3),
        ("flaw", "lawn", 2),
        ("abc", "abd", 1),
        ("abc", "abcd", 1),
        ("abcd", "abc", 1),
        ("abc", "ac", 1),
        ("sunday", "saturday", 3),
    ],
)
def test_known_distances(source, target, expected):
    assert levenshtein(source, target) == expected


@BUG
def test_triangle_inequality_and_identity():
    words = ["", "a", "ab", "ba", "abc"]
    for x, y, z in itertools.product(words, repeat=3):
        assert levenshtein(x, z) <= levenshtein(x, y) + levenshtein(y, z)
    for w in words:
        assert levenshtein(w, w) == 0
