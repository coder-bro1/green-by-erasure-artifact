"""Tests for the prime-length word filtering contract in solution.py."""

import pytest

from solution import words_in_sentence


@pytest.mark.parametrize(
    ("sentence", "expected"),
    [
        ("This is a test", "is"),
        ("lets go for swimming", "go for"),
    ],
)
def test_docstring_examples(sentence, expected):
    assert words_in_sentence(sentence) == expected


PRIME_LENGTHS = {
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
    43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
}


@pytest.mark.parametrize("length", range(1, 101))
def test_single_word_at_every_permitted_length(length):
    word = "a" * length
    expected = word if length in PRIME_LENGTHS else ""
    assert words_in_sentence(word) == expected


@pytest.mark.parametrize(
    ("sentence", "expected"),
    [
        ("a I x", ""),
        ("four eight nine", "eight"),
        ("four nine sixteen", "sixteen"),
        ("four nine abcd abcdef abcdefghi", ""),
        ("go cat apple oranges", "go cat apple oranges"),
        ("apple a go four cat nine oranges", "apple go cat oranges"),
        ("go four go cat a cat", "go go cat cat"),
        ("Go CAT Apple four ORANGES", "Go CAT Apple ORANGES"),
    ],
)
def test_filtering_preserves_word_order_duplicates_and_case(sentence, expected):
    assert words_in_sentence(sentence) == expected
