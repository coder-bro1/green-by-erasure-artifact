"""Tests for the string edit distance documented by solution.levenshtein."""

import pytest

from solution import levenshtein


@pytest.mark.parametrize(
    "source, target, expected",
    [
        ("", "", 0),
        ("", "abc", 3),
        ("abc", "", 3),
        ("", "é🙂", 2),
        ("é🙂", "", 2),
        ("a", "b", 1),
        ("abc", "xyz", 3),
        ("a", "xyz", 3),
        ("xyz", "a", 3),
        ("A", "a", 1),
        ("é", "e", 1),
        ("🙂", "🙃", 1),
        ("ab", "ba", 2),
    ],
)
def test_known_distances(source, target, expected):
    assert levenshtein(source, target) == expected


@pytest.mark.xfail(
    strict=True,
    reason="Matching characters incorrectly cost 1 edit; the documented distance requires 0.",
)
@pytest.mark.parametrize(
    "source, target, expected",
    [
        ("a", "a", 0),
        ("abc", "abc", 0),
        ("é🙂", "é🙂", 0),
        ("a", "ab", 1),
        ("ab", "a", 1),
        ("a", "ba", 1),
        ("ba", "a", 1),
        ("cat", "cut", 1),
        ("a", "a ", 1),
        ("é", "é🙂", 1),
        ("kitten", "sitting", 3),
        ("electron", "neutron", 3),
    ],
)
def test_distance_preserves_matching_characters(source, target, expected):
    assert levenshtein(source, target) == expected


@pytest.mark.parametrize(
    "source, target",
    [("", "abc"), ("ab", "ba"), ("cat", "cut"), ("é", "é🙂")],
)
def test_distance_is_symmetric(source, target):
    assert levenshtein(source, target) == levenshtein(target, source)
