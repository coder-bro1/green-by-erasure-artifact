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


def test_preserves_word_order_and_original_case():
    assert select_words("Bcd ae XYZ", 3) == ["Bcd", "XYZ"]


def test_handles_extra_spaces_between_words():
    assert select_words("  sky   why ", 3) == ["sky", "why"]


def test_zero_consonants_matches_vowel_only_words():
    assert select_words("aeiou sky EAU", 0) == ["aeiou", "EAU"]


def test_words_with_only_consonants_match_their_full_length():
    assert select_words("rhythm boat", 6) == ["rhythm"]
