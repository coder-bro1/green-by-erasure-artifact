import pytest

from solution import even_odd_palindrome


# Construct all decimal palindromes in the documented domain independently of
# the solution's string-reversal predicate.
PALINDROMES = (
    set(range(1, 10))
    | {11 * digit for digit in range(1, 10)}
    | {101 * outer + 10 * middle for outer in range(1, 10) for middle in range(10)}
)


@pytest.mark.parametrize("n, expected", [(3, (1, 2)), (12, (4, 6))])
def test_docstring_examples(n, expected):
    assert even_odd_palindrome(n) == expected


@pytest.mark.parametrize("n", range(1, 1001))
def test_inclusive_counts_across_documented_domain(n):
    included = {value for value in PALINDROMES if value <= n}
    expected = (
        sum(value % 2 == 0 for value in included),
        sum(value % 2 == 1 for value in included),
    )

    actual = even_odd_palindrome(n)

    assert isinstance(actual, tuple)
    assert len(actual) == 2
    assert all(type(count) is int for count in actual)
    assert actual == expected
