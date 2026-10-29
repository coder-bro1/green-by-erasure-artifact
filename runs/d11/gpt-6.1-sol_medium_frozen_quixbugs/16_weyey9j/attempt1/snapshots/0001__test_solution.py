"""Tests for Levenshtein distance, including the known matching-character bug."""

import pytest

from solution import levenshtein


@pytest.mark.parametrize(
    ("source", "target", "expected"),
    [
        ("", "", 0),
        ("", "abc", 3),
        ("abc", "", 3),
        ("", "\u00e9\U0001f600", 2),
        ("\u00e9\U0001f600", "", 2),
        ("a", "b", 1),
        ("a", "B", 1),
        ("\u00e9", "e", 1),
        ("\U0001f600", "\U0001f601", 1),
        (" ", "\t", 1),
        ("a", "bb", 2),
        ("aa", "b", 2),
        ("abc", "xyz", 3),
        ("aa", "bbb", 3),
        ("ab", "ba", 2),
    ],
)
def test_levenshtein_distance(source, target, expected):
    assert levenshtein(source, target) == expected


@pytest.mark.parametrize(
    ("source", "target"),
    [("", "abc"), ("a", "bb"), ("ab", "ba"), ("kitten", "sitting")],
)
def test_distance_is_symmetric(source, target):
    assert levenshtein(source, target) == levenshtein(target, source)


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Matching characters incorrectly add 1 instead of contributing zero edits",
)
@pytest.mark.parametrize(
    ("source", "target", "expected"),
    [
        pytest.param("a", "a", 0, id="identical-single-character"),
        pytest.param("same", "same", 0, id="identical-string"),
        pytest.param("ab", "ac", 1, id="shared-prefix"),
        pytest.param("ba", "ca", 1, id="shared-suffix"),
        pytest.param("a", "aa", 1, id="insertion"),
        pytest.param("aa", "a", 1, id="deletion"),
        pytest.param("kitten", "sitting", 3, id="mixed-edits"),
        pytest.param("electron", "neutron", 3, id="documented-example"),
    ],
)
def test_distance_with_matching_characters(source, target, expected):
    assert levenshtein(source, target) == expected
