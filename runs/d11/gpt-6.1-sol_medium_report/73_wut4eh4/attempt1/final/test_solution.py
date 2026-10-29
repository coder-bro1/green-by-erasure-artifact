"""Tests for the documented consonant-counting behavior of select_words."""

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
def test_docstring_examples(text, count, expected):
    assert select_words(text, count) == expected


@pytest.mark.parametrize("text", ["", " ", "     "])
@pytest.mark.parametrize("count", [1, 3, 20])
def test_empty_or_space_only_input(text, count):
    assert select_words(text, count) == []


@pytest.mark.parametrize(
    ("text", "count", "expected"),
    [
        pytest.param(
            "  cat   dog  a   fish  ", 2, ["cat", "dog"], id="extra-spaces"
        ),
        pytest.param(
            "cat dog cat fish dog", 2, ["cat", "dog", "cat", "dog"],
            id="order-and-duplicates",
        ),
        pytest.param(
            "AeIoU b AEIOU B", 1, ["b", "B"], id="vowels-ignore-case"
        ),
        pytest.param(
            "CAT cat Cat cAt", 2, ["CAT", "cat", "Cat", "cAt"],
            id="consonants-ignore-case-preserve-spelling",
        ),
        pytest.param("bcd BCDF aeiou", 3, ["bcd"], id="only-consonants"),
        pytest.param("a e i o u A E I O U", 1, [], id="only-vowels"),
        pytest.param("y Y sky rhythm", 1, ["y", "Y"], id="y-is-consonant"),
        pytest.param("a b cc ddd eeee ffff", 2, ["cc"], id="exact-count"),
        pytest.param("hello", 3, ["hello"], id="single-word-match"),
        pytest.param("hello", 4, [], id="single-word-no-match"),
        pytest.param("cat dog elephant", 100, [], id="count-exceeds-word-length"),
    ],
)
def test_consonant_selection(text, count, expected):
    assert select_words(text, count) == expected


def test_repeated_calls_return_independent_lists():
    first = select_words("cat dog", 2)
    first.append("changed")

    assert select_words("cat dog", 2) == ["cat", "dog"]
    assert select_words("fish", 3) == ["fish"]
