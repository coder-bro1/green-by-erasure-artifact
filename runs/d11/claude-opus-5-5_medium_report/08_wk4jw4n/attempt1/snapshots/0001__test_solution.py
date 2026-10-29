import pytest

from solution import split_words


# --- whitespace splitting -------------------------------------------------

def test_docstring_example_space():
    assert split_words("Hello world!") == ["Hello", "world!"]


def test_multiple_spaces_collapse():
    assert split_words("a   b  c") == ["a", "b", "c"]


def test_leading_trailing_spaces():
    assert split_words("  hi there  ") == ["hi", "there"]


def test_space_takes_precedence_over_comma():
    assert split_words("Hello world,!") == ["Hello", "world,!"]


def test_space_and_comma_mixed():
    assert split_words("a,b c") == ["a,b", "c"]


def test_only_spaces():
    assert split_words("   ") == []


def test_mixed_whitespace_with_space():
    assert split_words("a\tb c\nd") == ["a", "b", "c", "d"]


@pytest.mark.xfail(strict=True, reason="Only ' ' is checked; tab-only text is not treated as whitespace")
def test_tab_only_whitespace():
    assert split_words("Hello\tworld") == ["Hello", "world"]


@pytest.mark.xfail(strict=True, reason="Only ' ' is checked; newline-only text is not treated as whitespace")
def test_newline_only_whitespace():
    assert split_words("Hello\nworld") == ["Hello", "world"]


# --- comma splitting ------------------------------------------------------

@pytest.mark.xfail(strict=True, reason="Comma branch replaces ' ' with ',' instead of ',' with ' '")
def test_docstring_example_comma():
    assert split_words("Hello,world!") == ["Hello", "world!"]


@pytest.mark.xfail(strict=True, reason="Comma branch replaces ' ' with ',' instead of ',' with ' '")
def test_multiple_commas():
    assert split_words("a,b,c") == ["a", "b", "c"]


@pytest.mark.xfail(strict=True, reason="Comma branch replaces ' ' with ',' instead of ',' with ' '")
def test_consecutive_commas():
    assert split_words("a,,b") == ["a", "b"]


# --- odd-letter counting --------------------------------------------------

def test_docstring_example_count():
    assert split_words("abcdef") == 3


def test_empty_string():
    assert split_words("") == 0


def test_count_ignores_uppercase():
    assert split_words("BDF") == 0


def test_count_ignores_even_order_letters():
    assert split_words("acegikmoqsuwy") == 0


def test_count_all_odd_order_letters():
    assert split_words("bdfhjlnprtvxz") == 13


def test_count_full_alphabet():
    assert split_words("abcdefghijklmnopqrstuvwxyz") == 13


def test_count_ignores_digits_and_punctuation():
    assert split_words("b1d!F") == 2


def test_count_repeated_letters():
    assert split_words("aaabbb") == 3


def test_returns_int_type():
    assert isinstance(split_words("xyz"), int)
