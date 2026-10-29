import pytest

from solution import words_in_sentence


@pytest.mark.parametrize(
    ("sentence", "expected"),
    [
        ("This is a test", "is"),
        ("lets go for swimming", "go for"),
        ("aa bbb cccc ddddd ffffff ggggggg", "aa bbb ddddd ggggggg"),
        ("abcd abcdef abcdefgh", ""),
        ("one three seven", "one three seven"),
    ],
)
def test_words_with_prime_lengths_keep_original_order(sentence, expected):
    assert words_in_sentence(sentence) == expected


def test_single_letter_words_are_not_prime_length_words():
    assert words_in_sentence("a bb ccc") == "bb ccc"
