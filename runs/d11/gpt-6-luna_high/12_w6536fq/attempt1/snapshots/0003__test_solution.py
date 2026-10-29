import pytest

from solution import vowels_count


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("abcde", 2),
        ("ACEDY", 3),
        ("rhythm", 0),
        ("sky", 1),
        ("yellow", 2),
        ("Y", 1),
        ("AEIOU", 5),
        ("bookkeeper", 5),
        ("", 0),
    ],
)
def test_vowels_count(word, expected):
    assert vowels_count(word) == expected
