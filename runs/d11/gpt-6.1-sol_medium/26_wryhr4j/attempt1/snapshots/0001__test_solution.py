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
def test_documented_examples(text, count, expected):
    assert select_words(text, count) == expected


@pytest.mark.parametrize("text", ["", " ", "     "])
@pytest.mark.parametrize("count", [0, 1, 4])
def test_empty_or_spaces_only(text, count):
    assert select_words(text, count) == []


@pytest.mark.parametrize(
    "text, count, expected",
    [
        ("a e i o u AEIOU b", 0, ["a", "e", "i", "o", "u", "AEIOU"]),
        ("b BC bCd aeIOu", 3, ["bCd"]),
        ("Hello HELLO hElLo", 3, ["Hello", "HELLO", "hElLo"]),
        ("sky rhythm my a", 3, ["sky"]),
        ("  cat   dog  cat   a  ", 2, ["cat", "dog", "cat"]),
        ("a cat rhythm", 10, []),
        ("a I b B", 1, ["b", "B"]),
        ("aeiou bcdfg", 5, ["bcdfg"]),
    ],
)
def test_consonant_counts_and_output_order(text, count, expected):
    assert select_words(text, count) == expected
