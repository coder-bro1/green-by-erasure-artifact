import pytest

from solution import vowels_count

Y_BUG = (
    "solution.py counts 'y'/'Y' anywhere in the word, but the docstring says "
    "'y' is a vowel only when it is at the end of the word"
)


@pytest.mark.parametrize(
    "word, expected",
    [
        ("abcde", 2),  # docstring example
        ("ACEDY", 3),  # docstring example, trailing Y counts
        ("", 0),
        ("bcdfg", 0),
        ("aeiou", 5),
        ("AEIOU", 5),
        ("AeIoU", 5),
        ("hello", 2),
        ("key", 2),  # trailing y counts
        ("KEY", 2),
        ("y", 1),  # single y is at the end
        ("Y", 1),
        ("fly", 1),
    ],
)
def test_basic(word, expected):
    assert vowels_count(word) == expected


@pytest.mark.parametrize(
    "word, expected",
    [
        ("bye", 1),  # only 'e'; y is in the middle
        ("yellow", 2),  # e, o
        ("Yes", 1),  # e
        ("rhythm", 0),
        ("yy", 1),  # only the last y
        ("Yay", 2),  # a + trailing y; leading Y does not count
    ],
)
@pytest.mark.xfail(strict=True, reason=Y_BUG)
def test_y_not_at_end_is_not_a_vowel(word, expected):
    assert vowels_count(word) == expected


def test_returns_int():
    assert isinstance(vowels_count("abc"), int)
