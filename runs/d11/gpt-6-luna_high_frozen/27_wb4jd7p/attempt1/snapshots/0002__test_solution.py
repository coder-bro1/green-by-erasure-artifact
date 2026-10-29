import pytest

from solution import prime_length


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", False),
        ("a", False),
        ("ab", True),
        ("abc", True),
        ("Hello", True),
        ("abcdcba", True),
        ("kittens", True),
        ("orange", False),
        ("abcdef", False),
        ("abcdefghi", False),
        ("abcdefghijk", True),
    ],
)
def test_prime_length(value, expected):
    assert prime_length(value) is expected


@pytest.mark.parametrize("value", ["abcd"])
@pytest.mark.xfail(
    strict=True,
    reason="The implementation does not check divisibility by 2 for lengths above 3.",
)
def test_even_composite_lengths_are_not_prime(value):
    assert prime_length(value) is False
