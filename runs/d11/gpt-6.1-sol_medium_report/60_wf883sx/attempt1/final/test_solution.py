"""Tests for the documented consonant-selection contract."""

import pytest

from solution import select_words


@pytest.mark.parametrize(
    "text, count, expected",
    [
        ("Mary had a little lamb", 4, ["little"]),
        ("Mary had a little lamb", 3, ["Mary", "lamb"]),
        ("simple white space", 2, []),
        ("Hello world", 4, ["world"]),
        ("Uncle sam", 3, ["Uncle"]),
    ],
)
@pytest.mark.xfail(
    strict=True,
    reason="select_words counts vowels instead of the consonants promised by its docstring",
)
def test_docstring_examples(text, count, expected):
    assert select_words(text, count) == expected


@pytest.mark.parametrize(
    "text, count, expected",
    [
        ("a e i o u AEIOU", 0, ["a", "e", "i", "o", "u", "AEIOU"]),
        ("a e i o u", 1, []),
        ("b cd xyz", 1, ["b"]),
        ("b cd xyz", 2, ["cd"]),
        ("b cd xyz", 3, ["xyz"]),
        ("my sky rhythm", 2, ["my"]),
        ("my sky rhythm", 3, ["sky"]),
        ("my sky rhythm", 6, ["rhythm"]),
        ("  Cat   dog  Cat  ", 2, ["Cat", "dog", "Cat"]),
        ("CAT cat cAt AEIOU", 2, ["CAT", "cat", "cAt"]),
        ("b bb bbbb", 4, ["bbbb"]),
        ("aeiou bcd", 3, ["bcd"]),
    ],
)
@pytest.mark.xfail(
    strict=True,
    reason="select_words counts vowels instead of the consonants promised by its docstring",
)
def test_consonant_selection_edge_cases(text, count, expected):
    assert select_words(text, count) == expected


@pytest.mark.parametrize("text", ["", " ", "     "])
@pytest.mark.parametrize("count", [0, 1, 4])
def test_empty_or_spaces_only_returns_empty_list(text, count):
    assert select_words(text, count) == []


@pytest.mark.parametrize(
    "text, count, expected",
    [
        ("book deed NOON", 2, ["book", "deed", "NOON"]),
        ("  book   deed  book  ", 2, ["book", "deed", "book"]),
        ("banana", 3, ["banana"]),
        ("Mary had a little lamb", 100, []),
    ],
)
def test_matching_counts_order_and_duplicates(text, count, expected):
    assert select_words(text, count) == expected
