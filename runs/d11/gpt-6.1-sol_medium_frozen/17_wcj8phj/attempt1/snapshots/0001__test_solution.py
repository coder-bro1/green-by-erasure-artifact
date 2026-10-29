"""Tests for words_in_sentence, including its existing one-letter behavior."""

import pytest

from solution import words_in_sentence


@pytest.mark.parametrize(
    ("sentence", "expected"),
    [
        ("This is a test", "is a"),
        ("lets go for swimming", "go for"),
        ("we see green flowers", "we see green flowers"),
        ("four book little swimming", ""),
        ("three four two seven eleven", "three two seven"),
        ("go four go for for", "go go for for"),
        ("GO See GREEN", "GO See GREEN"),
        ("  go   for  swimming  ", "go for"),
        ("go\tfor\nswimming", "go for"),
        ("", ""),
        ("   \t\n", ""),
    ],
)
def test_sentence_filtering(sentence, expected):
    assert words_in_sentence(sentence) == expected


# Enumerated independently of the implementation's divisibility loop.
PRIME_LENGTHS = {
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
    53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
}


@pytest.mark.parametrize("length", range(2, 101))
def test_word_lengths_within_documented_sentence_limit(length):
    word = "x" * length
    expected = word if length in PRIME_LENGTHS else ""

    assert words_in_sentence(word) == expected


@pytest.mark.parametrize("sentence", ["a", "I", "a I x"])
def test_current_behavior_keeps_one_letter_words(sentence):
    """Characterize the implementation: it retains length 1 despite the spec."""
    assert words_in_sentence(sentence) == sentence
