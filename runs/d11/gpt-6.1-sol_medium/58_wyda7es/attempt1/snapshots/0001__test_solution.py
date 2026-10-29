import pytest

from solution import split_words


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello world!", ["Hello", "world!"]),
        ("  Hello   world!  ", ["Hello", "world!"]),
        ("Hello\tworld!", ["Hello", "world!"]),
        ("Hello\nworld!", ["Hello", "world!"]),
        ("Hello\r\nworld!", ["Hello", "world!"]),
        ("Hello\vworld!", ["Hello", "world!"]),
        ("Hello\fworld!", ["Hello", "world!"]),
        ("Hello\u00a0world!", ["Hello", "world!"]),
        (" \t\n", []),
        ("\t", []),
        ("Hello, world!", ["Hello,", "world!"]),
        ("Hello,\tworld!", ["Hello,", "world!"]),
        ("one,two three,four", ["one,two", "three,four"]),
    ],
)
def test_split_on_whitespace_before_commas(text, expected):
    assert split_words(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello,world!", ["Hello", "world!"]),
        ("one,two,three", ["one", "two", "three"]),
        (",", ["", ""]),
        (",one,", ["", "one", ""]),
        ("one,,two", ["one", "", "two"]),
    ],
)
def test_split_on_commas_without_whitespace(text, expected):
    assert split_words(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", 0),
        ("abcdef", 3),
        ("abcdefghijklmnopqrstuvwxyz", 13),
        ("acegikmoqsuwy", 0),
        ("bdfhjlnprtvxz", 13),
        ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 0),
        ("aAbBcCdDzZ", 3),
        ("bbbb", 4),
        ("123!@#$%^&*()", 0),
        ("b2-d!Z", 2),
    ],
)
def test_count_lowercase_letters_with_odd_alphabet_positions(text, expected):
    assert split_words(text) == expected
