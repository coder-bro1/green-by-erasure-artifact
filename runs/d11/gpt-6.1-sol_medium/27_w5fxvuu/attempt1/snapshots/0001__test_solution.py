import pytest

from solution import words_in_sentence


@pytest.mark.parametrize(
    ("sentence", "expected"),
    [
        ("This is a test", "is"),
        ("lets go for swimming", "go for"),
        ("a I x", ""),
        ("four nine sixteen", "sixteen"),
        ("This test", ""),
        ("go cat apple bananas", "go cat apple bananas"),
        ("apple a go four cat apple", "apple go cat apple"),
        ("He AND seven", "He AND seven"),
        ("go  for   swimming", "go for"),
    ],
)
def test_filters_words_by_prime_length(sentence, expected):
    assert words_in_sentence(sentence) == expected


# Explicit primes provide an oracle independent of the implementation's loop.
PRIME_LENGTHS = {
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97,
}


@pytest.mark.parametrize("length", range(1, 101))
def test_every_word_length_within_sentence_limit(length):
    word = "a" * length
    expected = word if length in PRIME_LENGTHS else ""
    assert words_in_sentence(word) == expected


def test_sentence_at_maximum_length_preserves_selected_words():
    sentence = " ".join(["a" * 47, "b" * 4, "c" * 47])
    assert len(sentence) == 100
    assert words_in_sentence(sentence) == " ".join(["a" * 47, "c" * 47])
