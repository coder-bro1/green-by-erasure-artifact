"""Tests for split_words' documented whitespace/comma/count priority."""

import pytest

from solution import split_words


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello world!", ["Hello", "world!"]),
        ("  alpha   beta  ", ["alpha", "beta"]),
        ("alpha \t beta\n gamma\r\n", ["alpha", "beta", "gamma"]),
        (" ", []),
        ("alpha,beta gamma,delta", ["alpha,beta", "gamma,delta"]),
        ("alpha, beta", ["alpha,", "beta"]),
    ],
)
def test_whitespace_splitting(text, expected):
    assert split_words(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello,world!", ["Hello", "world!"]),
        ("alpha,beta,gamma", ["alpha", "beta", "gamma"]),
        (",alpha", ["", "alpha"]),
        ("alpha,", ["alpha", ""]),
        ("alpha,,beta", ["alpha", "", "beta"]),
        (",", ["", ""]),
    ],
)
def test_comma_splitting(text, expected):
    assert split_words(text) == expected


@pytest.mark.parametrize("separator", ["\t", "\n", "\r", "\v", "\f", "\u00a0"])
@pytest.mark.parametrize("with_comma", [False, True])
def test_non_space_whitespace_splitting(separator, with_comma):
    first_word = "alpha,beta" if with_comma else "alpha"
    assert split_words(first_word + separator + "gamma") == [first_word, "gamma"]


@pytest.mark.parametrize("text", ["\t", "\n\r", "\v\f", "\u00a0"])
def test_whitespace_only_returns_empty_list(text):
    assert split_words(text) == []


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", 0),
        ("abcdef", 3),
        ("abcdefghijklmnopqrstuvwxyz", 13),
        ("acegikmoqsuwy", 0),
        ("bdfhjlnprtvxz", 13),
        ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 0),
        ("aAbBcCdD", 2),
        ("bbbb", 4),
        ("0123456789!?_-", 0),
        ("b2d!f", 3),
    ],
)
def test_counts_lowercase_letters_at_odd_alphabet_indices(text, expected):
    assert split_words(text) == expected


@pytest.mark.parametrize("index", range(26))
def test_each_lowercase_letter(index):
    assert split_words(chr(ord("a") + index)) == index % 2
