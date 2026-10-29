"""Regression tests for the current implementation of select_words.

The implementation counts vowels, despite the docstring specifying consonants.
These tests explicitly preserve that existing behavior.
"""

import pytest

from solution import select_words


@pytest.mark.parametrize("text", ["", " ", "     "])
def test_empty_or_space_only_input(text):
    assert select_words(text, 1) == []


@pytest.mark.parametrize(
    ("text", "count", "expected"),
    [
        ("Mary had a little lamb", 1, ["Mary", "had", "a", "lamb"]),
        ("Mary had a little lamb", 2, ["little"]),
        ("Hello world", 2, ["Hello"]),
        ("Uncle sam", 2, ["Uncle"]),
        ("simple white space", 3, []),
        ("aeiou AEIOU", 5, ["aeiou", "AEIOU"]),
        ("rhythm crypt sky", 0, ["rhythm", "crypt", "sky"]),
        ("a e i o u", 0, []),
        ("banana", 2, []),
        ("banana", 3, ["banana"]),
        ("banana", 4, []),
        ("one two", 100, []),
    ],
)
def test_selects_words_by_exact_vowel_count(text, count, expected):
    assert select_words(text, count) == expected


def test_vowel_count_is_case_insensitive_and_preserves_original_spelling():
    assert select_words("Apple APPLE aPpLe sky SKY", 2) == [
        "Apple", "APPLE", "aPpLe"
    ]


def test_ignores_leading_trailing_and_repeated_spaces():
    assert select_words("   cat    tree  dog   ", 1) == ["cat", "dog"]


def test_preserves_order_and_duplicate_words():
    assert select_words("dog tree cat dog apple cat", 1) == [
        "dog", "cat", "dog", "cat"
    ]


def test_calls_return_independent_lists():
    first = select_words("cat dog", 1)
    first.append("extra")

    assert select_words("cat dog", 1) == ["cat", "dog"]
