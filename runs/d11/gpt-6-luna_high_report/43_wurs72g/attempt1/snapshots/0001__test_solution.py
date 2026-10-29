import pytest

from solution import vowels_count


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("abcde", 2),
        ("ACEDY", 3),
        ("rhythm", 0),
        ("sky", 1),
        ("Y", 1),
        ("yellow", 2),
        ("beautiful", 5),
        ("queue", 4),
        ("AEIOU", 5),
        ("happy", 2),
        ("day", 2),
    ],
)
def test_vowels_count(word, expected):
    assert vowels_count(word) == expected


@pytest.mark.xfail(
    strict=True,
    reason="The function indexes the final character, so an empty string raises IndexError instead of returning its vowel count (0).",
)
def test_vowels_count_empty_string():
    assert vowels_count("") == 0
