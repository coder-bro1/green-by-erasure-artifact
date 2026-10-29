import pytest

from solution import split_words


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello world!", ["Hello", "world!"]),
        ("one\ttwo\nthree", ["one", "two", "three"]),
        ("  spaced   words  ", ["spaced", "words"]),
    ],
)
def test_splits_on_whitespace(text, expected):
    assert split_words(text) == expected


def test_whitespace_takes_precedence_over_commas():
    assert split_words("one,two three,four") == ["one,two", "three,four"]


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello,world!", ["Hello", "world!"]),
        ("a,,b", ["a", "b"]),
        (",a, b,", ["a", "b"]),
    ],
)
def test_splits_on_commas_when_there_is_no_whitespace(text, expected):
    assert split_words(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("abcdef", 3),  # b, d, and f have odd alphabet indices.
        ("aBz!", 0),
        ("bDFg", 4),
        ("", 0),
    ],
)
def test_counts_lowercase_letters_with_odd_alphabet_indices(text, expected):
    assert split_words(text) == expected
