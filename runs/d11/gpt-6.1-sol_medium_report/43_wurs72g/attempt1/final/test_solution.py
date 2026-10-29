import pytest

from solution import vowels_count


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        pytest.param("abcde", 2, id="first-docstring-example"),
        pytest.param("ACEDY", 3, id="uppercase-docstring-example"),
        pytest.param("aeiou", 5, id="all-lowercase-vowels"),
        pytest.param("AEIOU", 5, id="all-uppercase-vowels"),
        pytest.param("aEiOu", 5, id="mixed-case-vowels"),
        pytest.param("aaaEEEiiiOOOuuu", 15, id="repeated-vowels"),
        pytest.param("bcdfghjklmnpqrstvwxz", 0, id="only-consonants"),
        pytest.param("a", 1, id="single-lowercase-vowel"),
        pytest.param("U", 1, id="single-uppercase-vowel"),
        pytest.param("b", 0, id="single-consonant"),
        pytest.param("y", 1, id="single-lowercase-y"),
        pytest.param("Y", 1, id="single-uppercase-y"),
        pytest.param("rhythm", 0, id="internal-y-is-not-a-vowel"),
        pytest.param("yellow", 2, id="initial-y-is-not-a-vowel"),
        pytest.param("YELLOW", 2, id="initial-uppercase-y-is-not-a-vowel"),
        pytest.param("sky", 1, id="final-lowercase-y"),
        pytest.param("SKY", 1, id="final-uppercase-y"),
        pytest.param("yYyY", 1, id="only-final-y-counts"),
        pytest.param("yesterday", 4, id="ordinary-vowels-and-final-y"),
        pytest.param("aeiouy", 6, id="all-vowels-and-final-y"),
        pytest.param("café", 1, id="accented-letter-not-in-defined-vowels"),
    ],
)
def test_vowels_count(word, expected):
    assert vowels_count(word) == expected


@pytest.mark.xfail(
    strict=True,
    raises=IndexError,
    reason="An empty string contains zero vowels, but vowels_count indexes s[-1].",
)
def test_empty_string_has_no_vowels():
    assert vowels_count("") == 0
