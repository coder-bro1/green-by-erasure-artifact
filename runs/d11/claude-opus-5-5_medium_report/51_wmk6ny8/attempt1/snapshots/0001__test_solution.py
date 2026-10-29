import pytest

from solution import words_in_sentence

ONE_LETTER_BUG = (
    "solution.py treats words of length 1 as prime (the divisor loop "
    "range(2, 1) is empty, so flg stays 0), but 1 is not a prime number"
)


@pytest.mark.xfail(strict=True, reason=ONE_LETTER_BUG)
def test_docstring_example_1():
    assert words_in_sentence("This is a test") == "is"


def test_docstring_example_2():
    assert words_in_sentence("lets go for swimming") == "go for"


@pytest.mark.parametrize(
    "word, expected",
    [
        ("ab", "ab"),          # 2 prime
        ("abc", "abc"),        # 3 prime
        ("abcd", ""),          # 4
        ("abcde", "abcde"),    # 5 prime
        ("abcdef", ""),        # 6
        ("abcdefg", "abcdefg"),  # 7 prime
        ("abcdefgh", ""),      # 8
        ("abcdefghi", ""),     # 9
        ("a" * 11, "a" * 11),  # 11 prime
        ("a" * 25, ""),        # 25
        ("a" * 97, "a" * 97),  # 97 prime
        ("a" * 100, ""),       # 100
    ],
)
def test_single_word_lengths(word, expected):
    assert words_in_sentence(word) == expected


@pytest.mark.xfail(strict=True, reason=ONE_LETTER_BUG)
def test_single_letter_word_excluded():
    assert words_in_sentence("a") == ""


@pytest.mark.xfail(strict=True, reason=ONE_LETTER_BUG)
def test_single_letter_words_in_sentence_excluded():
    assert words_in_sentence("I am a go") == "am go"


def test_order_preserved():
    assert words_in_sentence("there is no place here") == "there is no place"


def test_no_prime_words_returns_empty_string():
    assert words_in_sentence("here this four test") == ""


def test_all_prime_words():
    assert words_in_sentence("go for it now") == "go for it now"


def test_duplicates_kept():
    assert words_in_sentence("hi hi test hi") == "hi hi hi"


def test_case_preserved():
    assert words_in_sentence("Hello WORLD here") == "Hello WORLD"


def test_returns_str():
    assert isinstance(words_in_sentence("lets go"), str)
