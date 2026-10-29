import pytest

from solution import split_words


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello world!", ["Hello", "world!"]),
        ("one\ttwo\nthree", ["one", "two", "three"]),
        ("one,two three", ["one,two", "three"]),
    ],
)
def test_splits_on_whitespace_when_present(text, expected):
    assert split_words(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello,world!", ["Hello", "world!"]),
        ("red,,blue,", ["red", "blue"]),
        (",", []),
    ],
)
def test_splits_on_commas_when_no_whitespace_is_present(text, expected):
    assert split_words(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("abcdef", 3),  # a, c, and e have odd alphabet indices.
        ("aBcDeF", 3),  # Uppercase letters do not contribute.
        ("xyz!", 1),  # Only z has an odd alphabet index.
        ("123!?", 0),
        ("", 0),
    ],
)
def test_counts_lowercase_letters_with_odd_alphabet_indices(text, expected):
    assert split_words(text) == expected
