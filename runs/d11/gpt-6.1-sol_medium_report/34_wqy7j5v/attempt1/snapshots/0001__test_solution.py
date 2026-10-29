"""Tests for the documented space-separated letter histogram."""

from collections import Counter
from itertools import product

import pytest

from solution import histogram


@pytest.mark.parametrize(
    ("letters", "expected"),
    [
        ("a b c", {"a": 1, "b": 1, "c": 1}),
        ("a b b a", {"a": 2, "b": 2}),
        ("a b c a b", {"a": 2, "b": 2}),
        ("b b b b a", {"b": 4}),
        ("", {}),
        ("a", {"a": 1}),
        ("z z z", {"z": 3}),
        ("a b b c c c", {"c": 3}),
        ("a a a b b c", {"a": 3}),
        ("z y x z y x a", {"z": 2, "y": 2, "x": 2}),
        (" ", {}),
        ("    ", {}),
        ("a  a b", {"a": 2}),
    ],
)
def test_histogram_examples_and_edge_cases(letters, expected):
    assert histogram(letters) == expected


def test_histogram_all_short_sequences():
    """Check unique winners and ties across all sequences up to six letters."""
    for length in range(7):
        for sequence in product("abc", repeat=length):
            counts = Counter(sequence)
            maximum = max(counts.values(), default=0)
            expected = {
                letter: count for letter, count in counts.items() if count == maximum
            }
            letters = " ".join(sequence)
            assert histogram(letters) == expected, repr(letters)


@pytest.mark.parametrize(
    ("letters", "expected"),
    [
        (" a", {"a": 1}),
        ("a ", {"a": 1}),
        ("a  b", {"a": 1, "b": 1}),
        (" a a ", {"a": 2}),
        ("a   a b", {"a": 2}),
    ],
)
def test_histogram_spacing_does_not_add_an_empty_letter(letters, expected):
    assert histogram(letters) == expected
