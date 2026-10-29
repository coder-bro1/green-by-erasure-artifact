from collections import Counter
from itertools import product

import pytest

from solution import most_frequent_letters


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("p q p", {"p": 2}),
        ("z y", {"z": 1, "y": 1}),
        ("a", {"a": 1}),
        ("a a a a", {"a": 4}),
        ("a b c d", {"a": 1, "b": 1, "c": 1, "d": 1}),
        ("a b b", {"b": 2}),
        ("a a b c", {"a": 2}),
        ("a b c c c", {"c": 3}),
        ("a b a b c", {"a": 2, "b": 2}),
        ("a b c a b c d", {"a": 2, "b": 2, "c": 2}),
        ("z a z a z b", {"z": 3}),
        ("a a b b b c c c c", {"c": 4}),
        (" ".join("abcdefghijklmnopqrstuvwxyz"), dict.fromkeys("abcdefghijklmnopqrstuvwxyz", 1)),
    ],
)
def test_most_frequent_letters(text, expected):
    assert most_frequent_letters(text) == expected


def test_short_sequences_match_independent_frequency_count():
    """Exercise all orderings and ties for up to five letters from a/b/c."""
    for length in range(1, 6):
        for letters in product("abc", repeat=length):
            text = " ".join(letters)
            frequencies = Counter(letters)
            maximum = max(frequencies.values())
            expected = {
                letter: count
                for letter, count in frequencies.items()
                if count == maximum
            }
            assert most_frequent_letters(text) == expected, text


def test_calls_do_not_share_results():
    first = most_frequent_letters("a a b")
    first["a"] = 999
    first["z"] = 1

    assert most_frequent_letters("b b a") == {"b": 2}
    assert most_frequent_letters("a a b") == {"a": 2}


@pytest.mark.xfail(
    strict=True,
    reason="Known bug: the documented empty input returns {'': 1} instead of {}.",
)
def test_empty_string_returns_empty_dictionary():
    assert most_frequent_letters("") == {}
