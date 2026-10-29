import pytest

from solution import prime_length


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", False),
        ("a", False),
        ("ab", True),
        ("abc", True),
        ("abcd", False),
        ("abcde", True),
        ("abcdef", False),
        ("abcdefg", True),
        ("abcdefgh", False),
        ("abcdefghi", False),
        ("abcdefghij", False),
        ("abcdefghijk", True),
    ],
)
def test_prime_length_by_length(value, expected):
    assert prime_length(value) is expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Hello", True),
        ("abcdcba", True),
        ("kittens", True),
        ("orange", False),
    ],
)
def test_docstring_examples(value, expected):
    assert prime_length(value) is expected


def test_length_two_is_prime():
    assert prime_length("🙂🙂") is True

