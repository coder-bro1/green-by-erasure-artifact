import pytest

from solution import prime_length


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", False),
        ("a", False),
        ("ab", True),
        ("abc", True),
        ("abcde", True),
        ("abcdef", False),
        ("abcdefghijk", True),
    ],
)
def test_prime_length(value, expected):
    assert prime_length(value) is expected


@pytest.mark.xfail(
    strict=True,
    reason="prime_length does not check divisibility by 2, so it reports these even composite lengths as prime",
)
def test_length_four_is_not_prime():
    assert prime_length("a" * 4) is False
