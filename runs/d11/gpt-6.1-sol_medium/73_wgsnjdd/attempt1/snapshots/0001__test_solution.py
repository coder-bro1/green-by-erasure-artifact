import pytest

from solution import vowels_count


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("abcde", 2),
        ("ACEDY", 3),
        ("", 0),
        ("bcdfghjklmnpqrstvwxz", 0),
        ("aeiou", 5),
        ("AEIOU", 5),
        ("aEiOu", 5),
        ("aaaEEEiiiOOOuuu", 15),
        ("y", 1),
        ("Y", 1),
        ("sky", 1),
        ("SKY", 1),
        ("yellow", 2),
        ("YELLOW", 2),
        ("rhythm", 0),
        ("yoy", 2),
        ("YyY", 1),
        ("yabY", 2),
        ("yyybc", 0),
    ],
)
def test_vowels_count(word, expected):
    assert vowels_count(word) == expected
