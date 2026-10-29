"""Regression tests for count_vowel_sounds as currently implemented."""

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
        ("aaaa", 4),
        ("rhythm", 1),
        ("SKY", 1),
        ("y", 1),
        ("Y", 1),
        ("12345 !?", 0),
        ("a1 E! i? O_u", 5),
        ("\t\n ", 0),
        ("áéíóú", 0),
    ],
)
def test_count_vowel_sounds(word, expected):
    assert count_vowel_sounds(word) == expected


@pytest.mark.parametrize("vowel", "aeiouAEIOU")
def test_each_vowel_counts_at_any_position(vowel):
    assert count_vowel_sounds(f"{vowel}b{vowel}c{vowel}") == 3


@pytest.mark.parametrize(
    ("word", "expected"),
    [("yes", 2), ("Yacht", 2), ("byb", 1), ("bYb", 1), ("yyYY", 4)],
)
def test_current_behavior_counts_nonfinal_y(word, expected):
    # The implementation counts every y/Y, despite the docstring's final-only rule.
    assert count_vowel_sounds(word) == expected
