import pytest

from solution import words_in_sentence


@pytest.mark.parametrize(
    ("sentence", "expected"),
    [
        ("This is a test", "is"),
        ("lets go for swimming", "go for"),
        ("a bb cat four", "bb cat"),
        ("one three seven", "one three seven"),
        ("a to an", ""),
    ],
)
def test_words_in_sentence_keeps_words_with_prime_lengths(sentence, expected):
    assert words_in_sentence(sentence) == expected


def test_words_in_sentence_preserves_original_order():
    assert words_in_sentence("three go swimming for") == "three go for"


def test_words_in_sentence_returns_empty_string_when_no_word_has_prime_length():
    assert words_in_sentence("a an four") == ""
