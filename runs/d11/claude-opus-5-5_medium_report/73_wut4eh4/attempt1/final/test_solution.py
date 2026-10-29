import pytest

from solution import select_words


@pytest.mark.parametrize(
    "s, n, expected",
    [
        ("Mary had a little lamb", 4, ["little"]),
        ("Mary had a little lamb", 3, ["Mary", "lamb"]),
        ("simple white space", 2, []),
        ("Hello world", 4, ["world"]),
        ("Uncle sam", 3, ["Uncle"]),
    ],
)
def test_docstring_examples(s, n, expected):
    assert select_words(s, n) == expected


def test_empty_string_returns_empty_list():
    assert select_words("", 4) == []
    assert select_words("", 0) == []


def test_only_spaces_returns_empty_list():
    assert select_words("   ", 0) == []


def test_zero_consonants_selects_all_vowel_words():
    assert select_words("a e I ou bcd", 0) == ["a", "e", "I", "ou"]


def test_uppercase_vowels_are_not_consonants():
    assert select_words("AEIOU aeiou", 0) == ["AEIOU", "aeiou"]


def test_uppercase_consonants_counted():
    assert select_words("BCD bcd BcD", 3) == ["BCD", "bcd", "BcD"]


def test_y_counts_as_consonant():
    assert select_words("my sky", 2) == ["my"]
    assert select_words("my sky", 3) == ["sky"]


def test_preserves_order_and_duplicates():
    assert select_words("cat dog cat bird", 2) == ["cat", "dog", "cat"]


def test_multiple_spaces_between_words():
    assert select_words("  cat   dog  ", 2) == ["cat", "dog"]


def test_no_match_returns_empty_list():
    assert select_words("hello world", 10) == []


def test_single_word():
    assert select_words("strengths", 8) == ["strengths"]


def test_returns_original_case():
    assert select_words("Little LAMB", 4) == ["Little"]
    assert select_words("Little LAMB", 3) == ["LAMB"]


def test_returns_new_list_each_call():
    a = select_words("cat", 2)
    b = select_words("cat", 2)
    assert a == b == ["cat"]
    assert a is not b
