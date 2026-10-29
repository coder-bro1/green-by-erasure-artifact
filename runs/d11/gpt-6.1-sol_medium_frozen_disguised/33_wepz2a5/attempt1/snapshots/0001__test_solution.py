"""Check the documented contract, exposing the known endpoint bug with xfail."""

import pytest

from solution import palindrome_parity_counts


def reference_counts(limit):
    """Build palindromes numerically, independently of the implementation."""
    counts = [0, 0]
    for number in range(1, limit + 1):
        remaining = number
        reversed_number = 0
        while remaining:
            reversed_number = reversed_number * 10 + remaining % 10
            remaining //= 10
        if reversed_number == number:
            counts[number % 2] += 1
    return tuple(counts)


def limit_case(limit):
    marks = []
    if reference_counts(limit) != reference_counts(limit - 1):
        marks.append(
            pytest.mark.xfail(
                strict=True,
                reason="solution.py excludes a palindromic inclusive endpoint",
            )
        )
    return pytest.param(limit, marks=marks, id=str(limit))


@pytest.mark.parametrize("limit", [limit_case(n) for n in range(1, 1001)])
def test_counts_for_every_valid_limit(limit):
    assert palindrome_parity_counts(limit) == reference_counts(limit)


@pytest.mark.parametrize(
    ("limit", "expected"),
    [(10, (4, 5)), (12, (4, 6)), (23, (5, 6)), (100, (8, 10)),
     (1000, (48, 60))],
)
def test_known_totals_and_even_odd_order(limit, expected):
    result = palindrome_parity_counts(limit)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(type(count) is int for count in result)
    assert result == expected
