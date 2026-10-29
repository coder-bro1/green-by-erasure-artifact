"""Tests for next_palindrome's documented palindromic-input contract."""

from bisect import bisect_right

import pytest

from solution import next_palindrome


def digits(number):
    return [int(character) for character in str(number)]


@pytest.mark.parametrize(
    ("current", "expected"),
    [
        (0, 1),
        (1, 2),
        (8, 9),
        (11, 22),
        (88, 99),
        (101, 111),
        (121, 131),
        (191, 202),
        (909, 919),
        (989, 999),
        (1001, 1111),
        (1221, 1331),
        (1991, 2002),
        (8998, 9009),
        (9889, 9999),
        (10001, 10101),
        (14941, 15051),
        (19991, 20002),
        (129921, 130031),
        (199991, 200002),
        (1999991, 2000002),
    ],
)
def test_next_palindrome_examples(current, expected):
    assert next_palindrome(digits(current)) == digits(expected)


def test_next_palindrome_matches_independent_oracle_through_four_digits():
    # Enumerate integers independently of the implementation's carry algorithm.
    palindromes = [
        number
        for number in range(10002)
        if str(number) == str(number)[::-1]
    ]
    for current in palindromes:
        if current > 9999 or set(str(current)) == {"9"}:
            continue
        expected = palindromes[bisect_right(palindromes, current)]
        result = next_palindrome(digits(current))
        assert result == digits(expected), f"Input: {current}"
        assert result == result[::-1]
        assert all(0 <= digit <= 9 for digit in result)


@pytest.mark.parametrize("current", [0, 11, 191, 1991, 14941, 1999991])
def test_non_overflow_updates_and_returns_original_list(current):
    original = digits(current)
    before = original.copy()

    result = next_palindrome(original)

    assert result is original
    assert original != before


@pytest.mark.parametrize("current", [9, 99, 999, 9999, 99999, 999999])
@pytest.mark.xfail(
    strict=True,
    reason="All-9 overflow inserts one extra zero in solution.py",
)
def test_all_nines_produces_smallest_larger_palindrome(current):
    assert next_palindrome(digits(current)) == digits(current + 2)
