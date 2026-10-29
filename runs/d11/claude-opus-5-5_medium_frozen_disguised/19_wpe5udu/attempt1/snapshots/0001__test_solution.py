import pytest

from solution import count_vowel_sounds


@pytest.mark.parametrize("word, expected", [
    ("sky", 1),
    ("Queue", 4),
    ("Banana", 3),
])
def test_docstring_examples(word, expected):
    assert count_vowel_sounds(word) == expected


def test_empty_string():
    assert count_vowel_sounds("") == 0


def test_no_vowels():
    assert count_vowel_sounds("rhythm") == 0
    assert count_vowel_sounds("bcdfg") == 0


def test_all_lowercase_vowels():
    assert count_vowel_sounds("aeiou") == 5


def test_all_uppercase_vowels():
    assert count_vowel_sounds("AEIOU") == 5


def test_mixed_case():
    assert count_vowel_sounds("HeLLo") == 2


@pytest.mark.parametrize("word, expected", [
    ("y", 1),
    ("Y", 1),
    ("happy", 2),
    ("SKY", 1),
])
def test_trailing_y_counts(word, expected):
    assert count_vowel_sounds(word) == expected


def test_non_letters_ignored():
    assert count_vowel_sounds("a1!e ?") == 2


def test_return_type_is_int():
    assert type(count_vowel_sounds("abc")) is int


# The docstring says y counts only as the last character, but
# solution.py counts y anywhere. These tests encode the documented
# behaviour and are expected to fail until solution.py is fixed.
@pytest.mark.xfail(strict=True, reason="BUG: solution.py counts non-final 'y' as a vowel")
@pytest.mark.parametrize("word, expected", [
    ("yes", 1),
    ("Yellow", 2),
    ("rhyme", 1),
    ("yay", 2),
])
def test_non_final_y_does_not_count(word, expected):
    assert count_vowel_sounds(word) == expected
