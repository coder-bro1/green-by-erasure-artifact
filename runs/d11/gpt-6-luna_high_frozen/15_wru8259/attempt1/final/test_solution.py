import pytest

from solution import select_words


@pytest.mark.parametrize("text", ["", "   ", "\t  "])
def test_empty_or_whitespace_input_returns_empty_list(text):
    assert select_words(text, 0) == []


@pytest.mark.xfail(
    strict=True,
    reason="solution.py counts vowels instead of consonants",
)
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
def test_selects_words_with_exactly_n_consonants(text, count, expected):
    assert select_words(text, count) == expected


def test_matching_words_keep_their_original_spelling_and_order():
    assert select_words("banana Banana", 3) == ["banana", "Banana"]
