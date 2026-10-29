import pytest

from solution import vowels_count


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("abcde", 2),
        ("ACEDY", 3),
        ("a", 1),
        ("E", 1),
        ("i", 1),
        ("O", 1),
        ("u", 1),
        ("b", 0),
        ("BCDFG", 0),
        ("aeiou", 5),
        ("AEIOU", 5),
        ("aEiOu", 5),
        ("aaaa", 4),
        ("bookkeeper", 5),
        ("y", 1),
        ("Y", 1),
        ("sky", 1),
        ("SKY", 1),
        ("happy", 2),
        ("HaPpY", 2),
        ("yellow", 2),
        ("YELLOW", 2),
        ("rhythm", 0),
        ("yby", 1),
        ("YYY", 1),
        ("yAyEyIyOyUy", 6),
        ("aeiouy", 6),
        ("aeiouyb", 5),
    ],
)
def test_vowels_count(word, expected):
    assert vowels_count(word) == expected


def test_vowels_count_long_word():
    # Internal y characters do not count, even when they occur repeatedly.
    word = "aEiOuy" * 1_000 + "Y"

    assert vowels_count(word) == 5_001
