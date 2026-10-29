"""Tests for the behavior currently implemented by ``solution.flip_case``.

The function's docstring describes swapping case, while its implementation
lowercases the input. These tests capture the implementation as requested,
without changing solution.py.
"""

from solution import flip_case


def test_flip_case_lowercases_mixed_case_text():
    assert flip_case("Hello, World!") == "hello, world!"


def test_flip_case_leaves_lowercase_text_unchanged():
    assert flip_case("already lowercase") == "already lowercase"


def test_flip_case_handles_empty_string():
    assert flip_case("") == ""


def test_flip_case_lowercases_unicode_letters():
    value = "\N{LATIN CAPITAL LETTER A WITH DIAERESIS}BC Stra\N{LATIN SMALL LETTER SHARP S}"
    expected = "\N{LATIN SMALL LETTER A WITH DIAERESIS}bc stra\N{LATIN SMALL LETTER SHARP S}"
    assert flip_case(value) == expected


def test_flip_case_preserves_non_letter_characters():
    assert flip_case("123 !?-") == "123 !?-"
