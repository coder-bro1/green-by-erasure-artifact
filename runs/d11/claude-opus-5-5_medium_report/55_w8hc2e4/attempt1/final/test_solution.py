import pytest

from solution import words_in_sentence


def test_docstring_example_1():
    assert words_in_sentence("This is a test") == "is"


def test_docstring_example_2():
    assert words_in_sentence("lets go for swimming") == "go for"


@pytest.mark.parametrize(
    "sentence, expected",
    [
        ("there is no place available here", "there is no place"),
        ("Hi I am Hussein", "Hi am Hussein"),
        ("go for it", "go for it"),
        ("here", ""),
        ("here is", "is"),
    ],
)
def test_mixed_sentences(sentence, expected):
    assert words_in_sentence(sentence) == expected


def test_single_letter_words_excluded():
    # 1 is not prime
    assert words_in_sentence("a b c") == ""


def test_single_word_with_prime_length():
    assert words_in_sentence("abc") == "abc"


def test_single_word_with_nonprime_length():
    assert words_in_sentence("abcd") == ""


@pytest.mark.parametrize("length", [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 97])
def test_prime_lengths_kept(length):
    word = "x" * length
    assert words_in_sentence(word) == word


@pytest.mark.parametrize("length", [1, 4, 6, 8, 9, 10, 12, 15, 21, 25, 49, 91, 100])
def test_nonprime_lengths_dropped(length):
    assert words_in_sentence("x" * length) == ""


def test_order_preserved():
    assert words_in_sentence("abc ab abcde abcd abcdefg") == "abc ab abcde abcdefg"


def test_duplicates_preserved():
    assert words_in_sentence("hi hi a hi") == "hi hi hi"


def test_case_preserved():
    assert words_in_sentence("HeLLo WoRLD") == "HeLLo WoRLD"


def test_returns_string():
    assert isinstance(words_in_sentence("nothing"), str)
