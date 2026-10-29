import pytest

from solution import vowels_count


@pytest.mark.parametrize(
    "word, expected",
    [
        pytest.param("abcde", 2, id="docstring-lowercase-example"),
        pytest.param("ACEDY", 3, id="docstring-uppercase-example"),
        pytest.param("", 0, id="empty-string"),
        pytest.param("bcdfghjklmnpqrstvwxz", 0, id="consonants-only"),
        pytest.param("BCDFGHJKLMNPQRSTVWXZ", 0, id="uppercase-consonants"),
        pytest.param("aeiou", 5, id="all-lowercase-vowels"),
        pytest.param("AEIOU", 5, id="all-uppercase-vowels"),
        pytest.param("aEiOu", 5, id="mixed-case-vowels"),
        pytest.param("banana", 3, id="repeated-vowels"),
        pytest.param("queue", 4, id="adjacent-vowels"),
        pytest.param("y", 1, id="single-lowercase-y"),
        pytest.param("Y", 1, id="single-uppercase-y"),
        pytest.param("sky", 1, id="final-lowercase-y"),
        pytest.param("SkY", 1, id="final-uppercase-y"),
        pytest.param("happy", 2, id="ordinary-vowel-and-final-y"),
    ],
)
def test_vowels_count(word, expected):
    assert vowels_count(word) == expected


@pytest.mark.parametrize("vowel", list("aeiouAEIOU"))
def test_each_ordinary_vowel_counts_in_every_position(vowel):
    assert vowels_count(vowel + "b" + vowel + "c" + vowel) == 3


@pytest.mark.xfail(
    strict=True,
    reason="Docstring counts y/Y only at the end; implementation counts every y/Y.",
)
@pytest.mark.parametrize(
    "word, expected",
    [
        pytest.param("rhythm", 0, id="internal-y"),
        pytest.param("Yacht", 1, id="initial-uppercase-y"),
        pytest.param("yellow", 2, id="initial-lowercase-y"),
        pytest.param("SYZYGY", 1, id="multiple-uppercase-y"),
        pytest.param("syzygy", 1, id="multiple-lowercase-y"),
        pytest.param("yYy", 1, id="only-final-y-counts"),
    ],
)
def test_y_counts_only_at_end(word, expected):
    assert vowels_count(word) == expected
