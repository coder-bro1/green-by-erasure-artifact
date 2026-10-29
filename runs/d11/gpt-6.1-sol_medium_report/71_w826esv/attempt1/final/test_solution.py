import pytest

from solution import even_odd_palindrome


# Construct all decimal palindromes in the documented domain independently of
# the solution's string-reversal predicate.
PALINDROMES = (
    set(range(1, 10))
    | {11 * digit for digit in range(1, 10)}
    | {101 * outer + 10 * middle for outer in range(1, 10) for middle in range(10)}
)


INCLUSIVE_BOUND_REASON = (
    "The docstring includes n, but range(1, n) excludes it, "
    "undercounting whenever n is a palindrome."
)


@pytest.mark.xfail(strict=True, reason=INCLUSIVE_BOUND_REASON)
def test_first_docstring_example():
    assert even_odd_palindrome(3) == (1, 2)


def test_second_docstring_example():
    assert even_odd_palindrome(12) == (4, 6)


def assert_inclusive_counts(n):
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


@pytest.mark.parametrize("n", sorted(set(range(1, 1001)) - PALINDROMES))
def test_nonpalindrome_bounds_across_documented_domain(n):
    assert_inclusive_counts(n)


@pytest.mark.xfail(strict=True, reason=INCLUSIVE_BOUND_REASON)
@pytest.mark.parametrize("n", sorted(PALINDROMES))
def test_palindrome_bounds_across_documented_domain(n):
    assert_inclusive_counts(n)
