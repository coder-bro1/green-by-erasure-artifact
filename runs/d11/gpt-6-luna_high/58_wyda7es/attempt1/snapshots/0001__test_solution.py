import pytest

from solution import split_words


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello world!", ["Hello", "world!"]),
        ("  Hello\tworld!\nagain  ", ["Hello", "world!", "again"]),
    ],
)
def test_splits_on_whitespace_when_present(text, expected):
    assert split_words(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello,world!", ["Hello", "world!"]),
        ("alpha,beta,gamma", ["alpha", "beta", "gamma"]),
        (",alpha,,beta,", ["", "alpha", "", "beta", ""]),
    ],
)
def test_splits_on_commas_when_there_is_no_whitespace(text, expected):
    assert split_words(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("abcdef", 3),  # b, d, and f have odd zero-based alphabet positions.
        ("aBz!", 0),  # Uppercase letters and punctuation are not counted.
        ("aceg", 0),
        ("", 0),
    ],
)
def test_counts_lowercase_letters_with_odd_alphabet_positions(text, expected):
    assert split_words(text) == expected
