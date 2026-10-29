import pytest

from solution import even_odd_palindrome


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (1, (0, 1)),
        (3, (1, 2)),
        (10, (4, 5)),
        (11, (4, 6)),
        (12, (4, 6)),
        (1000, (4, 14)),
    ],
)
def test_even_odd_palindrome_counts_palindromes_through_n(n, expected):
    assert even_odd_palindrome(n) == expected
