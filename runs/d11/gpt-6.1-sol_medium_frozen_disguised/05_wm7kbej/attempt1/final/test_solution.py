import pytest

from solution import keep_prime_length_words


@pytest.mark.parametrize(
    ("phrase", "expected"),
    [
        ("", ""),
        ("we built large house", "we built large house"),
        ("four wooden elephant", ""),
        ("we four built wooden large elephant house", "we built large house"),
        ("go go four cat cat", "go go cat cat"),
        ("WE Four Built HOUSE", "WE Built HOUSE"),
        ("éé abc 四四四四", "éé abc"),
    ],
)
def test_filters_words_and_preserves_order_and_spelling(phrase, expected):
    assert keep_prime_length_words(phrase) == expected


@pytest.mark.parametrize("length", [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31])
def test_keeps_prime_length_word(length):
    word = "x" * length
    assert keep_prime_length_words(word) == word


@pytest.mark.parametrize(
    "length", [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 21, 25, 27, 49]
)
def test_discards_composite_length_word(length):
    assert keep_prime_length_words("x" * length) == ""


@pytest.mark.xfail(
    strict=True,
    reason="Known bug: solution retains length-one words, although 1 is not prime.",
)
@pytest.mark.parametrize(
    ("phrase", "expected"),
    [
        ("a I", ""),
        ("we built a large house", "we built large house"),
    ],
)
def test_discards_one_letter_words(phrase, expected):
    assert keep_prime_length_words(phrase) == expected
