import pytest

from solution import even_odd_palindrome

INCLUSIVE_BUG = (
    "solution.py iterates range(1, n), excluding n, while the docstring says "
    "the range is inclusive of n; a palindromic n is never counted"
)


def brute_force(n):
    even = odd = 0
    for i in range(1, n + 1):
        if str(i) == str(i)[::-1]:
            if i % 2 == 0:
                even += 1
            else:
                odd += 1
    return (even, odd)


# --- Cases where n is NOT a palindrome (bug does not affect the result) ---

def test_docstring_example_2():
    assert even_odd_palindrome(12) == (4, 6)


@pytest.mark.parametrize(
    "n, expected",
    [
        (10, (4, 5)),
        (12, (4, 6)),
        (20, (4, 6)),
        (23, (5, 6)),
        (100, (8, 10)),
        (123, (8, 13)),
        (1000, (48, 60)),
    ],
)
def test_non_palindromic_n(n, expected):
    assert even_odd_palindrome(n) == expected


def test_returns_tuple_of_ints():
    result = even_odd_palindrome(12)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(x, int) for x in result)


# --- Cases where n IS a palindrome (inclusive upper bound matters) ---

@pytest.mark.xfail(strict=True, reason=INCLUSIVE_BUG)
def test_docstring_example_1():
    assert even_odd_palindrome(3) == (1, 2)


@pytest.mark.xfail(strict=True, reason=INCLUSIVE_BUG)
def test_minimum_input():
    assert even_odd_palindrome(1) == (0, 1)


@pytest.mark.xfail(strict=True, reason=INCLUSIVE_BUG)
def test_n_is_even_single_digit():
    assert even_odd_palindrome(2) == (1, 1)


@pytest.mark.xfail(strict=True, reason=INCLUSIVE_BUG)
def test_n_is_9():
    assert even_odd_palindrome(9) == (4, 5)


@pytest.mark.xfail(strict=True, reason=INCLUSIVE_BUG)
def test_n_is_11():
    assert even_odd_palindrome(11) == (4, 6)


@pytest.mark.xfail(strict=True, reason=INCLUSIVE_BUG)
def test_n_is_22():
    assert even_odd_palindrome(22) == (5, 6)


@pytest.mark.xfail(strict=True, reason=INCLUSIVE_BUG)
def test_n_is_999():
    assert even_odd_palindrome(999) == (48, 60)


@pytest.mark.xfail(strict=True, reason=INCLUSIVE_BUG)
def test_matches_brute_force_for_full_domain():
    for n in range(1, 1001):
        assert even_odd_palindrome(n) == brute_force(n), n
