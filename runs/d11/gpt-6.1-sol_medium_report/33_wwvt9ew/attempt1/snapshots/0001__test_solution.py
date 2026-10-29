import pytest

from solution import prime_length


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello", True),
        ("abcdcba", True),
        ("kittens", True),
        ("orange", False),
    ],
)
def test_docstring_examples(text, expected):
    assert prime_length(text) is expected


@pytest.mark.parametrize("length", [0, 1])
def test_lengths_below_two_are_not_prime(length):
    assert prime_length("a" * length) is False


@pytest.mark.parametrize("length", [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 97])
def test_prime_lengths(length):
    assert prime_length("a" * length) is True


@pytest.mark.parametrize(
    "length", [4, 6, 8, 9, 10, 15, 21, 25, 27, 35, 49, 77, 99, 121]
)
def test_composite_lengths(length):
    assert prime_length("a" * length) is False


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("  ", True),
        ("\t\n ", True),
        ("    ", False),
        ("a\x00b", True),
        ("\u00e9\u00e9", True),
        ("\U0001f600" * 3, True),
        ("\U0001f600" * 4, False),
        ("e\u0301", True),
    ],
)
def test_length_counts_all_characters(text, expected):
    assert prime_length(text) is expected
