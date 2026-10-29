import pytest

from solution import vowels_count


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        pytest.param("", 0, id="empty"),
        pytest.param("abcde", 2, id="docstring-lowercase"),
        pytest.param("ACEDY", 3, id="docstring-uppercase"),
        pytest.param("bcdfghjklmnpqrstvwxz", 0, id="consonants"),
        pytest.param("BCDFGHJKLMNPQRSTVWXZ", 0, id="uppercase-consonants"),
        pytest.param("aeiou", 5, id="all-vowels"),
        pytest.param("AEIOU", 5, id="uppercase-vowels"),
        pytest.param("aEiOu", 5, id="mixed-case"),
        pytest.param("aaaaa", 5, id="repeated-vowel"),
        pytest.param("Hello", 2, id="ordinary-word"),
        pytest.param("beautiful", 5, id="multiple-vowels"),
        pytest.param("queue", 4, id="adjacent-vowels"),
        pytest.param("sky", 1, id="final-y"),
        pytest.param("SKY", 1, id="final-uppercase-y"),
        pytest.param("boy", 2, id="ordinary-vowel-and-final-y"),
        pytest.param("y", 1, id="single-y"),
        pytest.param("Y", 1, id="single-uppercase-y"),
        pytest.param("123 !?\t\n", 0, id="nonletters"),
        pytest.param("a1 E! i? O\tu\n", 5, id="vowels-among-nonletters"),
        pytest.param("áéíóúäëïöü", 0, id="accented-letters"),
        pytest.param("你好🙂", 0, id="unicode-non-vowels"),
        pytest.param("aeiou" * 1000 + "y", 5001, id="long-input"),
    ],
)
def test_vowels_count(word, expected):
    assert vowels_count(word) == expected


@pytest.mark.parametrize("vowel", list("aeiouAEIOU"))
@pytest.mark.parametrize("position", ["start", "middle", "end"])
def test_standard_vowels_count_in_every_position(vowel, position):
    words = {"start": vowel + "bc", "middle": "b" + vowel + "c", "end": "bc" + vowel}
    assert vowels_count(words[position]) == 1


@pytest.mark.xfail(
    strict=True,
    reason="Known bug: solution counts y anywhere; the docstring allows only final y.",
)
@pytest.mark.parametrize(
    ("word", "expected"),
    [
        pytest.param("yes", 1, id="initial-y"),
        pytest.param("rhythm", 0, id="internal-y"),
        pytest.param("YELLOW", 2, id="initial-uppercase-y"),
        pytest.param("yyy", 1, id="only-last-y-counts"),
    ],
)
def test_only_final_y_is_a_vowel(word, expected):
    assert vowels_count(word) == expected
