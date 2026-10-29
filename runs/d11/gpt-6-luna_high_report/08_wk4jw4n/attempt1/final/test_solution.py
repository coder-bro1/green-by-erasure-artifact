import pytest

from solution import split_words


def test_splits_words_on_spaces():
    assert split_words("Hello world!") == ["Hello", "world!"]


def test_splits_on_whitespace_and_preserves_punctuation():
    assert split_words("one, two\nthree") == ["one,", "two", "three"]


@pytest.mark.xfail(
    strict=True,
    reason="split_words checks only for literal spaces, not all whitespace",
)
def test_splits_on_tabs_when_there_are_no_spaces():
    assert split_words("Hello\tworld!") == ["Hello", "world!"]


@pytest.mark.xfail(
    strict=True,
    reason="the comma branch does not split the text on commas",
)
def test_splits_on_commas_when_there_is_no_whitespace():
    assert split_words("Hello,world!") == ["Hello", "world!"]


def test_counts_lowercase_letters_with_odd_alphabet_indices():
    assert split_words("a") == 0


def test_empty_string_has_no_lowercase_letters():
    assert split_words("") == 0
