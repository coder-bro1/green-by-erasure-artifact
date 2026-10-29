import pytest

from solution import words_in_sentence

ONE_LETTER_BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py treats length-1 words as prime (range(2, 1) is empty, "
    "so flg stays 0); 1 is not prime per the spec",
)


def is_prime(n):
    return n >= 2 and all(n % i for i in range(2, int(n ** 0.5) + 1))


# --- Docstring examples -----------------------------------------------------

@ONE_LETTER_BUG
def test_docstring_example_1():
    assert words_in_sentence("This is a test") == "is"


def test_docstring_example_2():
    assert words_in_sentence("lets go for swimming") == "go for"


# --- Behaviour without single-letter words ----------------------------------

@pytest.mark.parametrize(
    "sentence, expected",
    [
        ("there is no place available here", "there is no place"),
        ("Hi we am Hussein", "Hi we am Hussein"),
        ("go for it", "go for it"),
        ("here", ""),
        ("here is", "is"),
        ("abcd efgh ijkl", ""),          # all length 4 -> none
        ("ab abc abcde abcdefg", "ab abc abcde abcdefg"),  # 2,3,5,7
        ("abcdef abcdefgh abcdefghi", ""),                 # 6,8,9
        ("abcdefghijk", "abcdefghijk"),                    # 11
        ("abcdefghijklm", "abcdefghijklm"),                # 13
        ("abcdefghijklmnop", ""),                          # 16
    ],
)
def test_prime_length_filtering(sentence, expected):
    assert words_in_sentence(sentence) == expected


def test_order_preserved():
    assert words_in_sentence("zz yyy xxxx wwwww") == "zz yyy wwwww"


def test_duplicates_kept():
    assert words_in_sentence("go go stop go") == "go go go"


def test_case_preserved():
    assert words_in_sentence("Go FOR iT") == "Go FOR iT"


def test_returns_string():
    assert isinstance(words_in_sentence("hello world"), str)


def test_no_matches_returns_empty_string():
    assert words_in_sentence("four nine") == ""


def test_extra_whitespace_collapsed():
    # str.split() with no args ignores runs of spaces.
    assert words_in_sentence("  go   for  ") == "go for"


def test_input_not_mutated():
    s = "lets go for swimming"
    words_in_sentence(s)
    assert s == "lets go for swimming"


@pytest.mark.parametrize("length", range(2, 101))
def test_single_word_of_each_length(length):
    word = "a" * length
    expected = word if is_prime(length) else ""
    assert words_in_sentence(word) == expected


# --- Single-letter words (known defect in solution.py) ----------------------

@ONE_LETTER_BUG
def test_single_letter_word_excluded():
    assert words_in_sentence("a") == ""


@ONE_LETTER_BUG
def test_single_letter_words_among_others():
    assert words_in_sentence("I am a go") == "am go"


@ONE_LETTER_BUG
def test_single_letter_pronoun():
    assert words_in_sentence("Hi I am Hussein") == "Hi am Hussein"
