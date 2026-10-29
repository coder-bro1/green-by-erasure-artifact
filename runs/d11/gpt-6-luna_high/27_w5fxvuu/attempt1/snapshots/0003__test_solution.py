import pytest

from solution import words_in_sentence


@pytest.mark.parametrize(
    ("sentence", "expected"),
    [
        ("This is a test", "is"),
        ("lets go for swimming", "go for"),
        ("a to cat four seven", "to cat seven"),
        ("abcdefg abcdefgh", "abcdefg"),
        ("cat", "cat"),
        ("a", ""),
        ("to", "to"),
        ("four", ""),
        ("letters only", "letters"),
    ],
)
def test_words_in_sentence_selects_prime_length_words_in_order(sentence, expected):
    assert words_in_sentence(sentence) == expected


def test_words_in_sentence_returns_empty_string_when_no_word_has_prime_length():
    assert words_in_sentence("a four eight") == ""


def test_words_in_sentence_preserves_order_of_matching_words():
    assert words_in_sentence("seven cat four two apple dog") == "seven cat two apple dog"
