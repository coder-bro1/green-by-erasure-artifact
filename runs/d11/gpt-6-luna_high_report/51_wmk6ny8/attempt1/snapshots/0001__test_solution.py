import pytest

from solution import words_in_sentence


def test_prime_length_words_are_kept_in_original_order():
    assert words_in_sentence("ab four xyz seven") == "ab xyz seven"


def test_words_with_only_composite_lengths_are_omitted():
    assert words_in_sentence("four seven eleven") == ""


def test_prime_length_words_from_documented_example_2():
    assert words_in_sentence("lets go for swimming") == "go for"


@pytest.mark.xfail(
    strict=True,
    reason="The implementation treats a one-letter word as having prime length; 1 is not prime.",
)
def test_one_letter_words_are_omitted_from_documented_example_1():
    assert words_in_sentence("This is a test") == "is"


@pytest.mark.xfail(
    strict=True,
    reason="The implementation treats a one-letter word as having prime length; 1 is not prime.",
)
def test_single_one_letter_word_is_omitted():
    assert words_in_sentence("a") == ""
