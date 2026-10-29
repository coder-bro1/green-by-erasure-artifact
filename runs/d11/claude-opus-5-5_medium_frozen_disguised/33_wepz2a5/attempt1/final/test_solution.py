import pytest

from solution import palindrome_parity_counts


def reference(limit):
    """Independent implementation of the documented spec (1..limit inclusive)."""
    evens = odds = 0
    for n in range(1, limit + 1):
        s = str(n)
        if s == s[::-1]:
            if n % 2 == 0:
                evens += 1
            else:
                odds += 1
    return (evens, odds)


def test_docstring_example_5():
    assert palindrome_parity_counts(5) == (2, 3)


def test_docstring_example_22():
    assert palindrome_parity_counts(22) == (5, 6)


def test_lower_bound_1():
    # 1 is an odd palindrome
    assert palindrome_parity_counts(1) == (0, 1)


def test_limit_2_includes_even_endpoint():
    assert palindrome_parity_counts(2) == (1, 1)


def test_all_single_digits():
    # 1..9: evens 2,4,6,8; odds 1,3,5,7,9
    assert palindrome_parity_counts(9) == (4, 5)


def test_10_is_not_palindrome():
    assert palindrome_parity_counts(10) == (4, 5)


def test_11_is_odd_palindrome():
    assert palindrome_parity_counts(11) == (4, 6)


def test_upper_bound_1000():
    # 9 one-digit, 9 two-digit, 90 three-digit palindromes; 1000 is not one.
    evens, odds = palindrome_parity_counts(1000)
    assert evens + odds == 108
    assert (evens, odds) == (48, 60)


def test_999_is_counted():
    assert palindrome_parity_counts(999) == (48, 60)
    assert palindrome_parity_counts(998) == (48, 59)


def test_returns_tuple_of_ints():
    result = palindrome_parity_counts(50)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(x, int) for x in result)


@pytest.mark.parametrize("limit", [1, 2, 3, 9, 10, 11, 21, 22, 99, 100, 101, 121, 202, 500, 999, 1000])
def test_matches_reference(limit):
    assert palindrome_parity_counts(limit) == reference(limit)


def test_matches_reference_exhaustive():
    for limit in range(1, 1001):
        assert palindrome_parity_counts(limit) == reference(limit), limit


def test_monotonic_non_decreasing():
    prev = (0, 0)
    for limit in range(1, 1001):
        cur = palindrome_parity_counts(limit)
        assert cur[0] >= prev[0] and cur[1] >= prev[1]
        prev = cur
