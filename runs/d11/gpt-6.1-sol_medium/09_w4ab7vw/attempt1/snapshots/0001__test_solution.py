import pytest

from solution import prime_length


@pytest.mark.parametrize(
    ("string", "expected"),
    [
        ("Hello", True),
        ("abcdcba", True),
        ("kittens", True),
        ("orange", False),
    ],
)
def test_documented_examples(string, expected):
    assert prime_length(string) is expected


PRIME_LENGTHS = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
                 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}


@pytest.mark.parametrize("length", range(101))
def test_lengths_from_zero_through_one_hundred(length):
    assert prime_length("x" * length) is (length in PRIME_LENGTHS)


@pytest.mark.parametrize(
    ("string", "expected"),
    [
        ("\u00e9", False),
        ("\u00e9\u00e9", True),
        ("\U0001f600" * 3, True),
        ("\U0001f600" * 4, False),
        ("a b", True),
        ("\n\t \r", False),
    ],
)
def test_length_counts_unicode_characters_and_whitespace(string, expected):
    assert prime_length(string) is expected
