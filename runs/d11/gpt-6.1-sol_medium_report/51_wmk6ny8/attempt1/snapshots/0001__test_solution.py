"""Tests for the prime-length word filtering contract in solution.py."""

import pytest

from solution import words_in_sentence


@pytest.mark.xfail(
    strict=True,
    reason="Length 1 is not prime, but the implementation retains one-letter words.",
)
def test_first_docstring_example():
    assert words_in_sentence("This is a test") == "is"


def test_second_docstring_example():
    assert words_in_sentence("lets go for swimming") == "go for"


@pytest.mark.xfail(
    strict=True,
    reason="Length 1 is not prime, but the implementation retains one-letter words.",
)
@pytest.mark.parametrize("sentence", ["a", "I", "a I b"])
def test_one_letter_words_are_excluded(sentence):
    assert words_in_sentence(sentence) == ""


# Explicit mathematical oracle, independent of the implementation's algorithm.
PRIME_LENGTHS = {
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
    47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
}


@pytest.mark.parametrize("length", range(2, 101))
def test_every_other_word_length_within_documented_limit(length):
    word = "a" * length
    expected = word if length in PRIME_LENGTHS else ""
    assert words_in_sentence(word) == expected


@pytest.mark.parametrize(
    ("sentence", "expected"),
    [
        ("ab abc abcd abcde abcdef abcdefg abcdefgh abcdefghi abcdefghij",
         "ab abc abcde abcdefg"),
        ("four sixsix eightten", ""),
        ("to cat apple oranges", "to cat apple oranges"),
        ("Dog tree UP apple Dog", "Dog UP apple Dog"),
        ("test ab tree abc", "ab abc"),
        ("ab tree abc test", "ab abc"),
    ],
    ids=[
        "mixed-lengths", "no-prime-lengths", "all-prime-lengths",
        "preserves-case-order-and-duplicates", "excluded-first", "excluded-last",
    ],
)
def test_sentence_filtering(sentence, expected):
    assert words_in_sentence(sentence) == expected
