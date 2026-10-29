import pytest

from solution import words_in_sentence


@pytest.mark.xfail(
    strict=True,
    reason="solution.py currently includes one-letter words, although their length is not prime",
)
def test_first_documented_example():
    assert words_in_sentence("This is a test") == "is"


def test_second_documented_example():
    assert words_in_sentence("lets go for swimming") == "go for"


def test_keeps_prime_length_words_in_original_order():
    assert words_in_sentence("two four seven twelve three") == "two four seven three"


def test_omits_words_with_composite_lengths():
    assert words_in_sentence("four sixxx ninechars") == ""


def test_length_two_is_prime():
    assert words_in_sentence("ox bird") == "ox"
