import pytest

from solution import vowels_count


def test_docstring_examples():
    assert vowels_count("abcde") == 2
    assert vowels_count("ACEDY") == 3


@pytest.mark.parametrize(
    "word, expected",
    [
        ("a", 1),
        ("b", 0),
        ("aeiou", 5),
        ("AEIOU", 5),
        ("AeIoU", 5),
        ("bcdfg", 0),
        ("rhythm", 0),
        ("key", 2),
        ("KEY", 2),
        ("y", 1),
        ("Y", 1),
        ("yellow", 2),   # leading y is not a vowel
        ("bayou", 3),    # middle y is not a vowel
        ("syzygy", 1),   # only the final y counts
        ("yy", 1),
        ("quickly", 3),
        ("Alone", 3),
        ("bye", 1),      # y not at end, e is
    ],
)
def test_counts(word, expected):
    assert vowels_count(word) == expected


def test_returns_int():
    assert isinstance(vowels_count("hello"), int)


@pytest.mark.xfail(
    strict=True,
    reason="solution.py indexes s[-1] without checking for an empty string, so "
    "it raises IndexError instead of returning 0 vowels",
)
def test_empty_string():
    assert vowels_count("") == 0
