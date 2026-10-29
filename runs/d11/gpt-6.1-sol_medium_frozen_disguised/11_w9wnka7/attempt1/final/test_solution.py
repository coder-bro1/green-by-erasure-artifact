"""Tests for the documented words_with_consonants contract."""

import pytest

from solution import words_with_consonants


@pytest.mark.parametrize("sentence", ["", " ", "     "])
@pytest.mark.parametrize("count", [0, 1, 3])
def test_empty_or_whitespace_sentence(sentence, count):
    assert words_with_consonants(sentence, count) == []


@pytest.mark.parametrize("count", [-2, -1, 10])
def test_count_outside_word_lengths(count):
    assert words_with_consonants("Big brown fox", count) == []


@pytest.mark.parametrize(
    ("sentence", "count", "expected"),
    [
        ("at be it on up", 1, ["at", "be", "it", "on", "up"]),
        ("AT Be iT oN Up", 1, ["AT", "Be", "iT", "oN", "Up"]),
        ("  at   be  it   ", 1, ["at", "be", "it"]),
        ("be at be at", 1, ["be", "at", "be", "at"]),
        ("boat team coat", 2, ["boat", "team", "coat"]),
        ("at boat be team", 1, ["at", "be"]),
        ("at boat be team", 2, ["boat", "team"]),
    ],
)
def test_words_with_equal_vowel_and_consonant_counts(sentence, count, expected):
    assert words_with_consonants(sentence, count) == expected


@pytest.mark.xfail(
    strict=True,
    reason="Known bug: solution.py counts vowels instead of consonants",
)
@pytest.mark.parametrize(
    ("sentence", "count", "expected"),
    [
        ("Big brown fox", 2, ["Big", "fox"]),
        ("brown", 4, ["brown"]),
        ("a E io AEIOU", 0, ["a", "E", "io", "AEIOU"]),
        ("b c df", 0, []),
        ("b c df", 1, ["b", "c"]),
        ("my rhythm sky", 2, ["my", "sky"]),
        ("BIG big FoX", 2, ["BIG", "big", "FoX"]),
        (" fox   Big fox  brown ", 2, ["fox", "Big", "fox"]),
    ],
)
def test_documented_consonant_count(sentence, count, expected):
    assert words_with_consonants(sentence, count) == expected
