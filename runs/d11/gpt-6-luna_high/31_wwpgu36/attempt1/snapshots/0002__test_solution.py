import pytest

from solution import even_odd_palindrome


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (1, (0, 1)),
        (2, (1, 1)),
        (3, (1, 2)),
        (9, (0, 9)),
        (10, (1, 9)),
        (11, (1, 10)),
        (12, (1, 10)),
        (100, (9, 9)),
        (101, (9, 10)),
    ],
)
def test_even_odd_palindrome_counts(n, expected):
    assert even_odd_palindrome(n) == expected


def test_counts_include_n_when_n_is_a_palindrome():
    # 11 is the first two-digit palindrome; it must be included at the boundary.
    assert even_odd_palindrome(11) == (1, 10)


def test_largest_supported_input():
    # Through 999, there are 108 palindromes: 9 one-digit and 99 three-digit,
    # plus 90 two-digit palindromes. All two-digit palindromes are odd.
    assert even_odd_palindrome(1000) == (99, 99)
