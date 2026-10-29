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
        (100, (8, 10)),
        (101, (8, 11)),
    ],
)
def test_even_odd_palindrome_counts(n, expected):
    assert even_odd_palindrome(n) == expected


def test_counts_include_n_when_n_is_a_palindrome():
    # 11 is the first two-digit palindrome; it must be included at the boundary.
    assert even_odd_palindrome(11) == (4, 6)


def test_largest_supported_input():
    # Through 999, there are 108 palindromes: 9 one-digit, 9 two-digit, and
    # 90 three-digit palindromes. Of these, 48 are even and 60 are odd.
    assert even_odd_palindrome(1000) == (48, 60)
