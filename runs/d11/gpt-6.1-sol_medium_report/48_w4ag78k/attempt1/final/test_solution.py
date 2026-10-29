"""Tests for split_words' documented delimiter precedence and letter counting."""

import pytest

from solution import split_words


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello world!", ["Hello", "world!"]),
        ("Hello,world!", ["Hello", "world!"]),
        ("abcdef", 3),
        ("  Hello   world!  ", ["Hello", "world!"]),
        ("Hello, world!", ["Hello,", "world!"]),
        ("one,two three,four", ["one,two", "three,four"]),
        ("one \t two\nthree\r\nfour", ["one", "two", "three", "four"]),
        (" \t\n\r ", []),
        ("one,two,three", ["one", "two", "three"]),
        ("", 0),
        ("abcdefghijklmnopqrstuvwxyz", 13),
        ("acegikmoqsuwy", 0),
        ("bdfhjlnprtvxz", 13),
        ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 0),
        ("bBbB", 2),
        ("123!?.-_", 0),
        ("ab12CD!yz", 2),
    ],
)
def test_documented_examples_and_common_inputs(text, expected):
    assert split_words(text) == expected


@pytest.mark.parametrize("letter", "abcdefghijklmnopqrstuvwxyz")
def test_each_lowercase_letter_uses_zero_based_alphabet_order(letter):
    expected = int((ord(letter) - ord("a")) % 2 == 1)
    assert split_words(letter) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello\tworld!", ["Hello", "world!"]),
        ("Hello\nworld!", ["Hello", "world!"]),
        ("Hello\rworld!", ["Hello", "world!"]),
        ("Hello\vworld!", ["Hello", "world!"]),
        ("Hello\fworld!", ["Hello", "world!"]),
        ("Hello\u00a0world!", ["Hello", "world!"]),
        ("\t\n\r", []),
        ("one,two\tthree,four", ["one,two", "three,four"]),
    ],
)
@pytest.mark.xfail(
    strict=True,
    reason="Docstring requires splitting on any whitespace; implementation checks only literal spaces.",
)
def test_whitespace_without_literal_spaces(text, expected):
    assert split_words(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (",", ["", ""]),
        (",one", ["", "one"]),
        ("one,", ["one", ""]),
        ("one,,two", ["one", "", "two"]),
    ],
)
@pytest.mark.xfail(
    strict=True,
    reason="Splitting on commas should preserve empty fields; replacing commas with spaces then split() drops them.",
)
def test_comma_splitting_preserves_empty_fields(text, expected):
    assert split_words(text) == expected
