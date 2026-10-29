"""Tests for next_palindrome's documented palindrome-input contract."""

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
        (9, 11),
        (11, 22),
        (88, 99),
        (99, 101),
        (101, 111),
        (121, 131),
        (191, 202),
        (909, 919),
        (999, 1001),
        (1001, 1111),
        (1221, 1331),
        (1991, 2002),
        (8998, 9009),
        (9999, 10001),
        (10001, 10101),
        (14941, 15051),  # The docstring example.
        (19991, 20002),
        (129921, 130031),
        (199991, 200002),
        (1239321, 1240421),
        (1999991, 2000002),
    ],
)
def test_next_palindrome_examples_and_carries(current, expected):
    assert next_palindrome(digits(current)) == digits(expected)


def test_every_small_palindrome_returns_its_immediate_successor():
    # Enumerating integers gives an independent oracle and verifies that no
    # palindrome between the input and output is skipped.
    palindromes = [
        number
        for number in range(10002)
        if str(number) == str(number)[::-1]
    ]
    for current, expected in zip(palindromes, palindromes[1:]):
        assert next_palindrome(digits(current)) == digits(expected), current


@pytest.mark.parametrize("length", [1, 2, 3, 4, 15, 16, 100, 101])
def test_all_nines_increase_the_number_of_digits(length):
    assert next_palindrome([9] * length) == [1] + [0] * (length - 1) + [1]


@pytest.mark.parametrize("half_length", [1, 2, 10, 50])
def test_long_odd_palindrome_increments_only_the_center(half_length):
    current = [1] + [0] * (2 * half_length - 1) + [1]
    expected = current.copy()
    expected[half_length] = 1
    assert next_palindrome(current) == expected


@pytest.mark.parametrize("half_length", [2, 3, 10, 50])
def test_long_even_palindrome_increments_the_middle_pair(half_length):
    current = [1] + [0] * (2 * half_length - 2) + [1]
    expected = current.copy()
    expected[half_length - 1 : half_length + 1] = [1, 1]
    assert next_palindrome(current) == expected
