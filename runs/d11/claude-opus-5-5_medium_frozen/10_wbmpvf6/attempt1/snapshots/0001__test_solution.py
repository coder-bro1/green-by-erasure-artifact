import pytest

from solution import vowels_count


@pytest.mark.parametrize(
    "word, expected",
    [
        ("abcde", 2),        # docstring example
        ("ACEDY", 3),        # docstring example, trailing Y counts
        ("", 0),
        ("bcdfg", 0),
        ("aeiou", 5),
        ("AEIOU", 5),
        ("AeIoU", 5),
        ("key", 2),          # trailing y counts
        ("bye", 1),
        ("y", 1),            # single-letter word ending in y
        ("Y", 1),
        ("rhythm", 0),
        ("hello", 2),
        ("Alone", 3),
        ("quick", 2),
        ("123!?", 0),
        ("xyz", 0),
        ("ééé", 0),          # only plain ASCII vowels count
    ],
)
def test_vowels_count_matches_spec(word, expected):
    assert vowels_count(word) == expected


def test_returns_int():
    assert isinstance(vowels_count("abc"), int)


def test_long_input():
    assert vowels_count("a" * 10_000) == 10_000


# The docstring says 'y' is a vowel ONLY at the end of the word, but the
# implementation counts every 'y'/'Y'. These cases follow the spec and are
# expected to fail until solution.py is fixed (strict=True makes the suite
# fail loudly once the bug is fixed, so the marker can be removed).
@pytest.mark.xfail(strict=True, reason="BUG: solution.py counts 'y' that is not at the end of the word")
@pytest.mark.parametrize(
    "word, expected",
    [
        ("yes", 1),
        ("Yellow", 2),
        ("myth", 0),
        ("syzygy", 1),
        ("YaY", 2),
    ],
)
def test_y_not_at_end_is_not_a_vowel(word, expected):
    assert vowels_count(word) == expected
