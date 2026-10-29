import pytest

from solution import words_in_sentence


@pytest.mark.parametrize(
    ("sentence", "expected"),
    [
        pytest.param("This is a test", "is", id="first-documented-example"),
        pytest.param("lets go for swimming", "go for", id="second-documented-example"),
        pytest.param("a I x", "", id="one-letter-words-are-not-prime"),
        pytest.param("four nine twelve", "", id="no-prime-length-words"),
        pytest.param("to cat apple", "to cat apple", id="all-words-qualify"),
        pytest.param("cat four to seven cat", "cat to seven cat", id="order-and-duplicates"),
        pytest.param("Go CAT Apple", "Go CAT Apple", id="preserve-capitalization"),
        pytest.param("  go   for  swimming  ", "go for", id="normalize-spaces"),
    ],
)
def test_words_in_sentence(sentence, expected):
    assert words_in_sentence(sentence) == expected


# Explicit expected primes keep the test independent of the implementation.
PRIME_LENGTHS = {
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
    43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
}


@pytest.mark.parametrize("length", range(1, 101))
def test_every_word_length_within_sentence_limit(length):
    word = "a" * length
    expected = word if length in PRIME_LENGTHS else ""

    assert words_in_sentence(word) == expected
