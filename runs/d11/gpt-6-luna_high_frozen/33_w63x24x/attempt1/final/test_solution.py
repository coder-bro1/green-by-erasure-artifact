import pytest

from solution import split_words


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello world!", ["Hello", "world!"]),
        ("  leading\tand\ntrailing  ", ["leading", "and", "trailing"]),
        ("one,two", ["one,two"]),
        ("abcdef", 3),
        ("ABCxyz!", 2),
        ("", 0),
    ],
)
def test_split_words(text, expected):
    assert split_words(text) == expected


def test_whitespace_takes_precedence_over_comma_fallback():
    assert split_words("one,two three") == ["one,two", "three"]
