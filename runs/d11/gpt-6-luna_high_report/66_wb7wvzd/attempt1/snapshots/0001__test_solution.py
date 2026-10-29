import pytest

from solution import even_odd_palindrome


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (1, (0, 1)),
        (2, (1, 1)),
        (3, (1, 2)),
        (9, (4, 5)),
        (10, (4, 5)),
        (11, (4, 6)),
        (12, (4, 6)),
        (99, (44, 55)),
        (100, (44, 55)),
        (101, (44, 56)),
        (1000, (494, 505)),
    ],
)
def test_even_odd_palindrome_counts_inclusive_range(n, expected):
    """Count palindromes from 1 through n, with even count first."""
    assert even_odd_palindrome(n) == expected


def test_returns_a_tuple():
    result = even_odd_palindrome(3)

    assert isinstance(result, tuple)
    assert len(result) == 2
