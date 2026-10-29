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
@pytest.mark.xfail(
    strict=True,
    reason="Docstring requires comma splitting, but the comma branch calls split() without a delimiter.",
)
def test_comma_splitting(text, expected):
    assert split_words(text) == expected


@pytest.mark.parametrize("separator", ["\t", "\n", "\r", "\v", "\f", "\u00a0"])
@pytest.mark.xfail(
    strict=True,
    reason="Docstring requires all whitespace to split words, but the whitespace branch checks only literal spaces.",
)
def test_non_space_whitespace_splitting(separator):
    assert split_words("alpha" + separator + "gamma") == ["alpha", "gamma"]


@pytest.mark.parametrize("separator", ["\t", "\n", "\r", "\v", "\f", "\u00a0"])
def test_non_space_whitespace_takes_priority_over_commas(separator):
    assert split_words("alpha,beta" + separator + "gamma") == ["alpha,beta", "gamma"]


@pytest.mark.parametrize("text", ["\t", "\n\r", "\v\f", "\u00a0"])
@pytest.mark.xfail(
    strict=True,
    reason="Docstring requires whitespace splitting, but whitespace without a literal space returns a letter count.",
)
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
