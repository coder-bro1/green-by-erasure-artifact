import pytest
from solution import words_with_consonants


def test_docstring_example():
    assert words_with_consonants('Big brown fox', 2) == ['Big', 'fox']


def test_empty_sentence():
    assert words_with_consonants('', 1) == []
    assert words_with_consonants('', 0) == []


def test_only_spaces():
    assert words_with_consonants('   ', 0) == []


def test_preserves_order_and_duplicates():
    assert words_with_consonants('cat dog cat', 2) == ['cat', 'dog', 'cat']


def test_case_insensitive_vowels():
    # 'AEIOU' has 0 consonants regardless of case
    assert words_with_consonants('AEIOU aeiou xyz', 0) == ['AEIOU', 'aeiou']


def test_y_is_a_consonant():
    assert words_with_consonants('sky my a', 2) == ['my']
    assert words_with_consonants('sky my a', 3) == ['sky']


def test_multiple_whitespace():
    assert words_with_consonants('  the   street  ', 2) == ['the']


def test_no_match():
    assert words_with_consonants('hello world', 10) == []


@pytest.mark.parametrize('word,n', [
    ('a', 0), ('b', 1), ('strengths', 8), ('Queue', 1), ('rhythm', 6),
])
def test_single_word_counts(word, n):
    assert words_with_consonants(word, n) == [word]
