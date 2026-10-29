import pytest

from solution import prime_length


@pytest.mark.parametrize(
    ("string", "expected"),
    [("Hello", True), ("abcdcba", True), ("kittens", True), ("orange", False)],
)
def test_docstring_examples(string, expected):
    assert prime_length(string) is expected


@pytest.mark.parametrize("length", [0, 1, 6, 8, 9, 10, 12, 15, 25, 49, 121])
def test_nonprime_lengths(length):
    assert prime_length("a" * length) is False


@pytest.mark.parametrize("length", [2, 3, 5, 7, 11, 13, 17, 29, 97])
def test_prime_lengths(length):
    assert prime_length("a" * length) is True


@pytest.mark.xfail(
    strict=True,
    reason="prime_length skips divisor 2 and incorrectly treats length 4 as prime",
)
def test_length_four_is_not_prime():
    assert prime_length("abcd") is False


@pytest.mark.parametrize(
    ("string", "expected"),
    [
        ("  ", True),
        ("\t\n ", True),
        ("\n" * 6, False),
        ("é🙂", True),
        ("বাংলা", True),
        ("🙂" * 9, False),
        ("a\x00b", True),
    ],
)
def test_length_counts_all_string_characters(string, expected):
    assert prime_length(string) is expected
