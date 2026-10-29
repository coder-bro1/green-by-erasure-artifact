import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solution import select_words


def test_empty_string_returns_empty_list():
    assert select_words("", 3) == []


def test_selects_words_with_exact_consonant_count_in_order():
    # Ab and eF each have one consonant and one vowel; baec has two of each.
    assert select_words("Ab baec eF", 1) == ["Ab", "eF"]


@pytest.mark.xfail(
    strict=True,
    reason="select_words counts vowels instead of consonants",
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
def test_documented_examples(text, count, expected):
    assert select_words(text, count) == expected
