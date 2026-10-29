"""Tests for the documented inclusive palindrome counts in solution.py."""

import pytest

from solution import even_odd_palindrome


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (3, (1, 2)),
        (12, (4, 6)),
    ],
)
def test_docstring_examples(n, expected):
    assert even_odd_palindrome(n) == expected


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (1, (0, 1)),
        (2, (1, 1)),
        (9, (4, 5)),
        (10, (4, 5)),
        (11, (4, 6)),
        (21, (4, 6)),
        (22, (5, 6)),
        (23, (5, 6)),
        (99, (8, 10)),
        (100, (8, 10)),
        (101, (8, 11)),
        (999, (48, 60)),
        (1000, (48, 60)),
    ],
)
def test_boundaries_and_inclusive_upper_endpoint(n, expected):
    assert even_odd_palindrome(n) == expected


# Construct every palindrome in the documented domain by digit position,
# independently of the implementation's string reversal check.
PALINDROMES = (
    list(range(1, 10))
    + [11 * outer for outer in range(1, 10)]
    + [101 * outer + 10 * middle
       for outer in range(1, 10)
       for middle in range(10)]
)


@pytest.mark.parametrize("n", range(1, 1001))
def test_every_documented_input(n):
    included = [value for value in PALINDROMES if value <= n]
    expected = (
        sum(value % 2 == 0 for value in included),
        sum(value % 2 == 1 for value in included),
    )

    result = even_odd_palindrome(n)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(type(count) is int for count in result)
    assert result == expected
