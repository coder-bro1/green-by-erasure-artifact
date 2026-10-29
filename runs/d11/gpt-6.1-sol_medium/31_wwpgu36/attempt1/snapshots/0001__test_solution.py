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
        (21, (4, 6)),
        (22, (5, 6)),
        (23, (5, 6)),
        (99, (8, 10)),
        (100, (8, 10)),
        (101, (8, 11)),
        (999, (40, 68)),
        (1000, (40, 68)),
    ],
)
def test_even_odd_palindrome_examples_and_boundaries(n, expected):
    result = even_odd_palindrome(n)

    assert isinstance(result, tuple)
    assert result == expected


def test_even_odd_palindrome_entire_supported_range():
    # Construct all one-, two-, and three-digit palindromes independently
    # of the solution's string-reversal check.
    palindromes = set(range(1, 10))
    palindromes.update(11 * digit for digit in range(1, 10))
    palindromes.update(
        101 * outer + 10 * middle
        for outer in range(1, 10)
        for middle in range(10)
    )
    even_count = odd_count = 0

    for n in range(1, 1001):
        if n in palindromes:
            if n % 2 == 0:
                even_count += 1
            else:
                odd_count += 1

        assert even_odd_palindrome(n) == (even_count, odd_count), f"n={n}"
