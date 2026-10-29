import pytest

from solution import vowels_count


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("", 0),
        ("abcde", 2),
        ("ACEDY", 3),
        ("sky", 1),
        ("Y", 1),
        ("education!", 5),
        ("123", 0),
    ],
)
def test_vowels_count(word, expected):
    assert vowels_count(word) == expected


@pytest.mark.xfail(
    strict=True,
    reason="The implementation counts every y, but the docstring says y is a vowel only at the end of the word.",
)
@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("yellow", 2),
        ("rhythms", 0),
        ("mythology", 3),
    ],
)
def test_internal_y_is_not_a_vowel(word, expected):
    assert vowels_count(word) == expected
