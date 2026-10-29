"""Tests for split_words, including its current delimiter behavior."""

import string

import pytest

from solution import split_words


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello world!", ["Hello", "world!"]),
        ("  one   two  ", ["one", "two"]),
        (" \t\n\r ", []),
        ("one\ttwo\nthree four", ["one", "two", "three", "four"]),
        ("Hello, world!", ["Hello,", "world!"]),
        ("one,two three,four", ["one,two", "three,four"]),
        (" abcdef ", ["abcdef"]),
    ],
)
def test_space_triggers_whitespace_splitting(text, expected):
    assert split_words(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello,world!", ["Hello,world!"]),
        (",", [","]),
        (",one,,two,", [",one,,two,"]),
        ("abc,def\tghi\njkl", ["abc,def", "ghi", "jkl"]),
        ("\t,\n", [","]),
    ],
)
def test_comma_branch_preserves_commas_but_splits_whitespace(text, expected):
    # The current comma branch calls split() without a comma separator.
    assert split_words(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", 0),
        ("abcdef", 3),
        ("acegikmoqsuwy", 0),
        ("bdfhjlnprtvxz", 13),
        (string.ascii_lowercase, 13),
        (string.ascii_uppercase, 0),
        ("bBbBdd!!123", 4),
        ("123!?_", 0),
        ("\t\n\r", 0),
        ("b\td\nf", 3),
    ],
)
def test_without_space_or_comma_counts_lowercase_odd_alphabet_positions(text, expected):
    assert split_words(text) == expected


@pytest.mark.parametrize("letter", string.ascii_lowercase)
def test_each_ascii_lowercase_letter(letter):
    alphabet_position = string.ascii_lowercase.index(letter)
    assert split_words(letter) == alphabet_position % 2


@pytest.mark.parametrize("letter", string.ascii_uppercase)
def test_uppercase_letters_are_not_counted(letter):
    assert split_words(letter) == 0
