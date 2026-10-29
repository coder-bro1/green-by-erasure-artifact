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


def test_empty_string_is_not_prime():
    assert prime_length("") is False


def test_length_one_is_not_prime():
    assert prime_length("a") is False


@pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 97, 101])
def test_prime_lengths(n):
    assert prime_length("x" * n) is True


@pytest.mark.parametrize("n", [4, 6, 8, 9, 10, 12, 15, 21, 25, 49, 100, 121])
def test_composite_lengths(n):
    assert prime_length("x" * n) is False


def test_whitespace_and_unicode_count_as_characters():
    assert prime_length("  ") is True  # length 2
    assert prime_length("ééé") is True  # length 3
    assert prime_length("éééé") is False  # length 4


def test_matches_reference_for_range():
    def is_prime(n):
        return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))

    for n in range(0, 200):
        assert prime_length("a" * n) == is_prime(n), n
