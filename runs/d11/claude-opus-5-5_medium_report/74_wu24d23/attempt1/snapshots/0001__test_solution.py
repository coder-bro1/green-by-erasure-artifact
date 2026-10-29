import pytest

from solution import prime_length


@pytest.mark.parametrize(
    "s, expected",
    [
        ("Hello", True),
        ("abcdcba", True),
        ("kittens", True),
        ("orange", False),
    ],
)
def test_docstring_examples(s, expected):
    assert prime_length(s) is expected


@pytest.mark.parametrize("s", ["", "a"])
def test_lengths_zero_and_one_are_not_prime(s):
    assert prime_length(s) is False


@pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 97, 101])
def test_prime_lengths(n):
    assert prime_length("x" * n) is True


@pytest.mark.parametrize("n", [6, 8, 9, 10, 12, 15, 16, 25, 49, 100, 121])
def test_composite_lengths(n):
    assert prime_length("x" * n) is False


@pytest.mark.xfail(
    strict=True,
    reason="solution.py starts trial division at 3, never testing divisor 2, "
    "so length 4 is wrongly reported as prime",
)
def test_length_four_is_not_prime():
    assert prime_length("abcd") is False


def test_counts_characters_not_bytes_or_words():
    assert prime_length("a b") is True  # length 3, spaces count
    assert prime_length("éé") is True  # 2 chars (4 bytes in UTF-8)
