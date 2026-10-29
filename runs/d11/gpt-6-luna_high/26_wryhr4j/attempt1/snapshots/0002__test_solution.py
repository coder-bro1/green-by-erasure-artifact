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


def test_empty_input_returns_empty_list():
    assert select_words("", 0) == []


def test_zero_consonants_matches_vowel_only_words():
    assert select_words("a E I O U", 0) == ["a", "E", "I", "O", "U"]


def test_y_is_counted_as_a_consonant_and_original_case_is_preserved():
    assert select_words("rhythm sky A", 5) == ["rhythm"]
    assert select_words("rhythm sky A", 3) == ["sky"]


def test_words_are_returned_in_input_order():
    assert select_words("bat cat apple dog", 2) == ["bat", "cat", "dog"]
