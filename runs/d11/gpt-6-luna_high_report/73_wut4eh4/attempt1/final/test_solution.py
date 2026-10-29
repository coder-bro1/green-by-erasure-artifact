import pytest

from solution import select_words


@pytest.mark.parametrize(
    ("text", "count", "expected"),
    [
        ("Mary had a little lamb", 4, ["little"]),
        ("Mary had a little lamb", 3, ["Mary", "lamb"]),
        ("simple white space", 2, []),
        ("Hello world", 4, ["world"]),
        ("Uncle sam", 3, ["Uncle"]),
    ],
)
def test_documented_examples(text, count, expected):
    assert select_words(text, count) == expected


def test_empty_string_returns_empty_list():
    assert select_words("", 0) == []


def test_only_spaces_returns_empty_list():
    assert select_words("   \t  ", 0) == []


def test_zero_consonants_selects_vowel_only_words():
    assert select_words("AEIOU sky queue", 0) == ["AEIOU"]


def test_words_are_returned_in_input_order_and_original_case():
    assert select_words("Bob cat dog", 2) == ["Bob", "cat", "dog"]


def test_y_is_counted_as_a_consonant():
    assert select_words("myth sky", 4) == ["myth"]


def test_nonmatching_count_returns_empty_list():
    assert select_words("cat dog", 1) == []
