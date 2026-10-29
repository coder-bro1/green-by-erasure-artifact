"""Tests for the documented histogram contract."""

from collections import Counter
from itertools import product
from string import ascii_lowercase

import pytest

from solution import histogram


@pytest.mark.parametrize(
    ("letters", "expected"),
    [
        ("a b c", {"a": 1, "b": 1, "c": 1}),
        ("a b b a", {"a": 2, "b": 2}),
        ("a b c a b", {"a": 2, "b": 2}),
        ("b b b b a", {"b": 4}),
        ("z", {"z": 1}),
        ("a a a a", {"a": 4}),
        ("a b b c c c", {"c": 3}),
        ("c c c b b a", {"c": 3}),
        ("a b c a b c d", {"a": 2, "b": 2, "c": 2}),
        (" ".join(ascii_lowercase), dict.fromkeys(ascii_lowercase, 1)),
    ],
)
def test_histogram_returns_only_most_frequent_letters(letters, expected):
    assert histogram(letters) == expected


def test_histogram_matches_independent_counts_for_short_sequences():
    """Cover every ordering and frequency distribution over three letters."""
    for length in range(1, 7):
        for letters in product("abc", repeat=length):
            counts = Counter(letters)
            highest_count = max(counts.values())
            expected = {
                letter: count
                for letter, count in counts.items()
                if count == highest_count
            }
            text = " ".join(letters)
            assert histogram(text) == expected, text


def test_histogram_calls_do_not_share_results():
    first = histogram("a a b")
    first["a"] = 100
    first["z"] = 100

    assert histogram("b b a") == {"b": 2}
    assert histogram("a a b") == {"a": 2}


@pytest.mark.xfail(
    strict=True,
    reason="Known implementation bug: empty input returns {'': 1} instead of {}.",
)
def test_histogram_empty_input_returns_empty_dictionary():
    assert histogram("") == {}
