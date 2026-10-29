import pytest

from solution import vowels_count


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("abcde", 2),
        ("ACEDY", 3),
        ("rhythm", 0),
        ("sky", 1),
        ("queue", 4),
        ("AEIOU", 5),
        ("", 0),
        ("bcd-!", 0),
    ],
)
def test_vowels_count(word, expected):
    assert vowels_count(word) == expected


def test_vowels_count_counts_repeated_vowels_individually():
    assert vowels_count("cooee") == 4


def test_vowels_count_handles_vowels_in_mixed_case():
    assert vowels_count("aEioU") == 5
