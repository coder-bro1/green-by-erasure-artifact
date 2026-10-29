"""Tests for the contract documented by count_vowel_sounds."""

import pytest

from solution import count_vowel_sounds


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("", 0),
        ("sky", 1),
        ("Queue", 4),
        ("Banana", 3),
        ("bcdfghjklmnpqrstvwxz", 0),
        ("BCDFGHJKLMNPQRSTVWXZ", 0),
        ("aeiou", 5),
        ("AEIOU", 5),
        ("aEiOu", 5),
        ("aaaEEEiiiOOOuuu", 15),
        ("y", 1),
        ("Y", 1),
        ("SKY", 1),
        ("day", 2),
        ("DAY", 2),
        ("rhythm", 0),
        ("123 !?\t\n", 0),
        ("a! E? i1 O2 u3", 5),
        ("café", 1),
        ("áéíóú", 0),
        ("aeiou" * 1000, 5000),
    ],
)
def test_count_vowel_sounds(word, expected):
    assert count_vowel_sounds(word) == expected


@pytest.mark.parametrize("vowel", "aeiouAEIOU")
def test_each_standard_vowel_counts_in_any_position(vowel):
    assert count_vowel_sounds(vowel + "bc") == 1
    assert count_vowel_sounds("b" + vowel + "c") == 1
    assert count_vowel_sounds("bc" + vowel) == 1


@pytest.mark.xfail(
    strict=True,
    reason="Known bug: implementation counts y/Y even when not the last character",
)
@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("yes", 1),
        ("YES", 1),
        ("rhythm", 0),
        ("yy", 1),
        ("YyY", 1),
        ("y ", 0),
        ("sky!", 0),
        ("y\n", 0),
    ],
)
def test_only_terminal_y_counts(word, expected):
    assert count_vowel_sounds(word) == expected
