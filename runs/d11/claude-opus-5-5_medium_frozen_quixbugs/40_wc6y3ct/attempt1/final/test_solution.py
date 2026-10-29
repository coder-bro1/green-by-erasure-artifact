import pytest

from solution import next_palindrome


def to_int(digits):
    return int("".join(map(str, digits)))


def to_digits(n):
    return [int(c) for c in str(n)]


def is_pal(n):
    s = str(n)
    return s == s[::-1]


def reference_next_palindrome(n):
    n += 1
    while not is_pal(n):
        n += 1
    return n


def test_docstring_example():
    assert next_palindrome([1, 4, 9, 4, 1]) == [1, 5, 0, 5, 1]


@pytest.mark.parametrize(
    "digits, expected",
    [
        ([0], [1]),
        ([5], [6]),
        ([8], [9]),
        ([1, 1], [2, 2]),
        ([1, 2, 2, 1], [1, 3, 3, 1]),
        ([1, 2, 1], [1, 3, 1]),
        ([1, 9, 1], [2, 0, 2]),
        ([1, 9, 9, 1], [2, 0, 0, 2]),
        ([4, 9, 9, 9, 4], [5, 0, 0, 0, 5]),
        ([8, 9, 9, 8], [9, 0, 0, 9]),
        ([1, 2, 3, 2, 1], [1, 2, 4, 2, 1]),
        ([2, 3, 9, 9, 3, 2], [2, 4, 0, 0, 4, 2]),
    ],
)
def test_known_values(digits, expected):
    assert next_palindrome(list(digits)) == expected


def test_result_is_palindrome_and_larger():
    digits = [3, 7, 9, 7, 3]
    result = next_palindrome(list(digits))
    assert result == result[::-1]
    assert to_int(result) > to_int(digits)


def test_mutates_and_returns_same_list_in_normal_case():
    digits = [1, 2, 1]
    result = next_palindrome(digits)
    assert result is digits
    assert digits == [1, 3, 1]


def test_matches_brute_force_for_non_all_nines():
    palindromes = [n for n in range(0, 100000) if is_pal(n) and set(str(n)) != {"9"}]
    for n in palindromes:
        assert to_int(next_palindrome(to_digits(n))) == reference_next_palindrome(n), n


# Known defect in solution.py: when every digit is 9 the function returns
# [1] + len(digit_list) * [0] + [1], one zero too many. The correct result is
# [1] + (len(digit_list) - 1) * [0] + [1]. These are strict xfails so they flag
# as XPASS (failure) if the bug is ever fixed.
@pytest.mark.xfail(strict=True, reason="all-9s overflow emits one extra zero")
@pytest.mark.parametrize(
    "digits, expected",
    [
        ([9], [1, 1]),
        ([9, 9], [1, 0, 1]),
        ([9, 9, 9], [1, 0, 0, 1]),
        ([9, 9, 9, 9], [1, 0, 0, 0, 1]),
    ],
)
def test_all_nines_rollover(digits, expected):
    assert next_palindrome(list(digits)) == expected


@pytest.mark.parametrize("length", [1, 2, 3, 4, 5])
def test_all_nines_current_behavior(length):
    # Pins the actual (buggy) output so regressions in behavior are noticed.
    assert next_palindrome([9] * length) == [1] + [0] * length + [1]
