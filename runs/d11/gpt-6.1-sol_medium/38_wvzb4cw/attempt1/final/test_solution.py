import pytest

from solution import split_words


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello world!", ["Hello", "world!"]),
        ("one two three", ["one", "two", "three"]),
        ("  leading and trailing  ", ["leading", "and", "trailing"]),
        ("one   two", ["one", "two"]),
        ("one\t two\nthree\rfour", ["one", "two", "three", "four"]),
        (" ", []),
        ("   \t\n", []),
        ("Hello, world!", ["Hello,", "world!"]),
        ("one,two three,four", ["one,two", "three,four"]),
    ],
)
def test_split_on_whitespace_when_spaces_are_present(text, expected):
    assert split_words(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello,world!", ["Hello", "world!"]),
        ("one,two,three", ["one", "two", "three"]),
        (",one,two,", ["one", "two"]),
        ("one,,two", ["one", "two"]),
        (",", []),
        (",,,", []),
        ("one,\ttwo\nthree", ["one", "two", "three"]),
        ("123,456", ["123", "456"]),
    ],
)
def test_split_on_commas_without_spaces(text, expected):
    assert split_words(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("abcdef", 3),
        ("abcdefghijklmnopqrstuvwxyz", 13),
        ("bdfhjlnprtvxz", 13),
        ("acegikmoqsuwy", 0),
        ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 0),
        ("aAbBcCdDzZ", 3),
        ("bbbbzz", 6),
        ("0123456789!@#$%^&*()", 0),
        ("b2d4f!", 3),
        ("", 0),
    ],
)
def test_count_lowercase_letters_at_odd_alphabet_positions(text, expected):
    result = split_words(text)
    assert type(result) is int
    assert result == expected


@pytest.mark.parametrize("letter", "abcdefghijklmnopqrstuvwxyz")
def test_each_lowercase_letter_uses_zero_based_alphabet_position(letter):
    alphabet_position = ord(letter) - ord("a")
    assert split_words(letter) == alphabet_position % 2
