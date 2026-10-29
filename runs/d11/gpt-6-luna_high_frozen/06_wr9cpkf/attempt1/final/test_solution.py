import pytest

from solution import even_odd_palindrome


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (1, (0, 0)),
        (2, (0, 1)),
        (10, (4, 5)),
        (11, (4, 5)),  # 11 is the excluded upper bound.
        (12, (4, 6)),
        (22, (4, 6)),  # 22 is the excluded upper bound.
        (23, (5, 6)),
    ],
)
def test_even_odd_palindrome_counts(n, expected):
    assert even_odd_palindrome(n) == expected


def test_counts_cover_palindromes_below_upper_bound():
    # Check the full documented input range against a simple direct count.
    for n in range(1, 1001):
        palindromes = [
            value
            for value in range(1, n)
            if str(value) == str(value)[::-1]
        ]
        expected = (
            sum(value % 2 == 0 for value in palindromes),
            sum(value % 2 == 1 for value in palindromes),
        )
        assert even_odd_palindrome(n) == expected
