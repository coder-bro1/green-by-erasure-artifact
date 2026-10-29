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
def test_documented_examples(text, expected):
    assert prime_length(text) is expected


@pytest.mark.parametrize("length", [0, 1, 4, 6, 8, 9, 10, 15, 21, 25, 49, 121])
def test_nonprime_lengths(length):
    assert prime_length("x" * length) is False


@pytest.mark.parametrize("length", [2, 3, 5, 7, 11, 13, 17, 29, 97, 101])
def test_prime_lengths(length):
    assert prime_length("x" * length) is True


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("  ", True),
        ("\t\n ", True),
        ("a b\n", False),
        ("\x00\x00", True),
        ("é", False),
        ("你好", True),
        ("😀😀😀", True),
        ("😀😀😀😀", False),
        ("e\u0301", True),
    ],
)
def test_length_counts_all_unicode_characters(text, expected):
    assert prime_length(text) is expected
